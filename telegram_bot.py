import os
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta
import asyncio

# Load environment variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
session_name = os.getenv("SESSION_NAME", "user_session")
group_id_acleda = int(os.getenv("GROUP_ID"))
group_id_payway = int(os.getenv("GROUP_ID_PAYWAY"))
admin_user_id = int(os.getenv("ADMIN_USER_ID"))

# Initialize TWO clients:
# 1. Bot client for receiving commands
bot = TelegramClient(
    'bot_session', 
    api_id, 
    api_hash,
    connection_retries=5,
    retry_delay=1,
    timeout=30
).start(bot_token=bot_token)

# 2. User client for reading group messages
user_client = TelegramClient(
    session_name,
    api_id,
    api_hash,
    connection_retries=5,
    retry_delay=1,
    timeout=30
)

print("Bot is running...")

async def calculate_transfers(target_date, period_name, progress_callback=None):
    """Calculate transfers for a specific date with progress updates"""
    
    try:
        # Initialize combined totals
        total_khr = 0.0
        total_usd = 0.0
        count_khr = 0
        count_usd = 0
        
        # === Process ACLEDA Group ===
        if progress_callback:
            await progress_callback("📥 Fetching ACLEDA messages...")
        
        try:
            group_acleda = await asyncio.wait_for(
                user_client.get_entity(group_id_acleda), 
                timeout=10
            )
        except asyncio.TimeoutError:
            return "❌ Error: Timeout fetching ACLEDA group"
        except Exception as e:
            return f"❌ Error accessing ACLEDA group: {str(e)}"
        
        acleda_khr = 0.0
        acleda_usd = 0.0
        acleda_count_khr = 0
        acleda_count_usd = 0
        
        message_count = 0
        async for message in user_client.iter_messages(group_acleda, limit=500):
            message_count += 1
            
            # Progress update every 50 messages
            if progress_callback and message_count % 50 == 0:
                await progress_callback(f"📥 Processing ACLEDA: {message_count} messages...")
            
            if message.text:
                message_datetime = message.date
                if message_datetime.tzinfo is not None:
                    message_datetime = message_datetime.astimezone()
                message_date = message_datetime.date()
                
                if message_date != target_date:
                    continue
                
                text = message.text
                amount = None
                currency = None
                
                # ACLEDA Patterns
                match1 = re.search(r"Received\s+([\d,.]+)\s+(KHR|USD)", text, re.IGNORECASE)
                match2 = re.search(r"([\d,.]+)\s+រៀល", text)
                match3 = re.search(r"([\d,.]+)\s+ដុល្លារ", text)
                
                if match1:
                    amount = float(match1.group(1).replace(",", ""))
                    currency = match1.group(2).upper()
                elif match2:
                    amount = float(match2.group(1).replace(",", ""))
                    currency = "KHR"
                elif match3:
                    amount = float(match3.group(1).replace(",", ""))
                    currency = "USD"

                if amount and currency:
                    if currency == "KHR":
                        acleda_khr += amount
                        acleda_count_khr += 1
                    elif currency == "USD":
                        acleda_usd += amount
                        acleda_count_usd += 1
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(1)
        
        # === Process PayWay Group ===
        if progress_callback:
            await progress_callback("📥 Fetching PayWay messages...")
        
        try:
            group_payway = await asyncio.wait_for(
                user_client.get_entity(group_id_payway), 
                timeout=10
            )
        except asyncio.TimeoutError:
            return "❌ Error: Timeout fetching PayWay group"
        except Exception as e:
            return f"❌ Error accessing PayWay group: {str(e)}"
        
        payway_khr = 0.0
        payway_usd = 0.0
        payway_count_khr = 0
        payway_count_usd = 0
        
        message_count = 0
        async for message in user_client.iter_messages(group_payway, limit=500):
            message_count += 1
            
            # Progress update every 50 messages
            if progress_callback and message_count % 50 == 0:
                await progress_callback(f"📥 Processing PayWay: {message_count} messages...")
            
            if message.text:
                message_datetime = message.date
                if message_datetime.tzinfo is not None:
                    message_datetime = message_datetime.astimezone()
                message_date = message_datetime.date()
                
                if message_date != target_date:
                    continue
                
                text = message.text
                amount = None
                currency = None
                
                # PayWay Patterns
                match_khr = re.search(r"៛([\d,.]+)\s+paid by", text)
                match_usd = re.search(r"\$([\d,.]+)\s+paid by", text)
                
                if match_khr:
                    amount = float(match_khr.group(1).replace(",", ""))
                    currency = "KHR"
                elif match_usd:
                    amount = float(match_usd.group(1).replace(",", ""))
                    currency = "USD"

                if amount and currency:
                    if currency == "KHR":
                        payway_khr += amount
                        payway_count_khr += 1
                    elif currency == "USD":
                        payway_usd += amount
                        payway_count_usd += 1
        
        # Calculate combined totals
        total_khr = acleda_khr + payway_khr
        total_usd = acleda_usd + payway_usd
        count_khr = acleda_count_khr + payway_count_khr
        count_usd = acleda_count_usd + payway_count_usd

        # Format results
        result = f"""
🏦 **TRANSFER SUMMARY - {period_name.upper()}**
📅 Date: {target_date.strftime('%B %d, %Y')}
{'─' * 40}

**💳 ACLEDA**
៛ KHR: {acleda_khr:,.2f} ({acleda_count_khr} transactions)
💵 USD: ${acleda_usd:,.2f} ({acleda_count_usd} transactions)

**🏧 PayWay by ABA**
៛ KHR: {payway_khr:,.2f} ({payway_count_khr} transactions)
💵 USD: ${payway_usd:,.2f} ({payway_count_usd} transactions)

{'═' * 40}
**📊 TOTAL (BOTH ACCOUNTS)**
{'═' * 40}
៛ **KHR: {total_khr:,.2f}** ({count_khr} transactions)
💵 **USD: ${total_usd:,.2f}** ({count_usd} transactions)
"""
        
        return result
    
    except Exception as e:
        return f"❌ Error calculating transfers: {str(e)}"

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Handle /start command"""
    # Check if user is admin
    if event.sender_id != admin_user_id:
        await event.respond("❌ Sorry, this bot is private.")
        return
    
    buttons = [
        [Button.inline("📅 Today", b"today")],
        [Button.inline("📆 Yesterday", b"yesterday")],
        [Button.inline("📊 Last 7 Days", b"week")],
        [Button.inline("📈 This Month", b"month")]
    ]
    
    await event.respond(
        "👋 **Welcome to Transfer Summary Bot!**\n\n"
        "Select a time period to view your transaction summary:",
        buttons=buttons
    )

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    """Handle button clicks"""
    # Check if user is admin
    if event.sender_id != admin_user_id:
        await event.answer("❌ Unauthorized", alert=True)
        return
    
    data = event.data.decode('utf-8')
    
    # Skip "back" button here (handled separately)
    if data == "back":
        return
    
    # Show processing message
    await event.answer("⏳ Processing...", alert=False)
    
    now = datetime.now()
    result = ""  # Initialize result
    
    # Create progress callback
    async def update_progress(message):
        try:
            await event.edit(message)
        except Exception as e:
            print(f"Progress update error: {e}")
    
    try:
        if data == "today":
            await update_progress("⏳ Starting calculation for today...")
            target_date = now.date()
            period_name = "Today"
            result = await calculate_transfers(target_date, period_name, update_progress)
            
        elif data == "yesterday":
            await update_progress("⏳ Starting calculation for yesterday...")
            target_date = (now - timedelta(days=1)).date()
            period_name = "Yesterday"
            result = await calculate_transfers(target_date, period_name, update_progress)
            
        elif data == "week":
            # Calculate for last 7 days
            await update_progress("⏳ Calculating last 7 days (0/7)...")
            results = []
            for i in range(7):
                await update_progress(f"⏳ Calculating last 7 days ({i+1}/7)...")
                date = (now - timedelta(days=i)).date()
                day_result = await calculate_transfers(date, date.strftime('%b %d'), None)
                results.append(day_result)
                await asyncio.sleep(0.5)  # Small delay between days
            
            result = "\n\n".join(results)
            
        elif data == "month":
            # Calculate for current month (limit to 10 days to avoid timeout)
            await update_progress("⏳ Calculating this month...")
            first_day = now.replace(day=1).date()
            results = []
            current = now.date()
            days_processed = 0
            max_days = 10  # Limit to prevent timeout
            
            while current >= first_day and days_processed < max_days:
                await update_progress(f"⏳ Processing {current.strftime('%b %d')}...")
                day_result = await calculate_transfers(current, current.strftime('%b %d'), None)
                results.append(day_result)
                current -= timedelta(days=1)
                days_processed += 1
                await asyncio.sleep(0.5)
            
            result = "\n\n".join(results)
            if days_processed >= max_days:
                result += f"\n\n⚠️ Showing last {max_days} days only"
        else:
            result = "❌ Unknown option"
        
        # Add back button
        buttons = [[Button.inline("« Back to Menu", b"back")]]
        
        # Split message if too long
        if len(result) > 4000:
            chunks = [result[i:i+4000] for i in range(0, len(result), 4000)]
            await event.edit(chunks[0], buttons=buttons)
            for chunk in chunks[1:]:
                await event.respond(chunk)
        else:
            await event.edit(result, buttons=buttons)
            
    except Exception as e:
        error_msg = f"❌ **Error occurred:**\n{str(e)}\n\nPlease try again or use /cancel"
        buttons = [[Button.inline("« Back to Menu", b"back")]]
        try:
            await event.edit(error_msg, buttons=buttons)
        except:
            await event.respond(error_msg, buttons=buttons)

@bot.on(events.CallbackQuery(data=b"back"))
async def back_handler(event):
    """Handle back button"""
    buttons = [
        [Button.inline("📅 Today", b"today")],
        [Button.inline("📆 Yesterday", b"yesterday")],
        [Button.inline("📊 Last 7 Days", b"week")],
        [Button.inline("📈 This Month", b"month")]
    ]
    
    await event.edit(
        "👋 **Welcome to Transfer Summary Bot!**\n\n"
        "Select a time period to view your transaction summary:",
        buttons=buttons
    )

@bot.on(events.NewMessage(pattern='/summary'))
async def summary_handler(event):
    """Quick command for today's summary"""
    if event.sender_id != admin_user_id:
        await event.respond("❌ Sorry, this bot is private.")
        return
    
    msg = await event.respond("⏳ Fetching today's transactions...")
    
    now = datetime.now()
    
    async def update_progress(message):
        try:
            await msg.edit(message)
        except Exception:
            pass
    
    result = await calculate_transfers(now.date(), "Today", update_progress)
    
    buttons = [[Button.inline("« Back to Menu", b"back")]]
    await msg.edit(result, buttons=buttons)

@bot.on(events.NewMessage(pattern='/cancel'))
async def cancel_handler(event):
    """Cancel current operation"""
    if event.sender_id != admin_user_id:
        await event.respond("❌ Sorry, this bot is private.")
        return
    
    buttons = [
        [Button.inline("📅 Today", b"today")],
        [Button.inline("📆 Yesterday", b"yesterday")],
        [Button.inline("📊 Last 7 Days", b"week")],
        [Button.inline("📈 This Month", b"month")]
    ]
    
    await event.respond(
        "✅ **Operation Cancelled**\n\n"
        "Select a new time period:",
        buttons=buttons
    )

@bot.on(events.NewMessage(pattern='/restart'))
async def restart_handler(event):
    """Restart bot (requires manual restart on server)"""
    if event.sender_id != admin_user_id:
        await event.respond("❌ Sorry, this bot is private.")
        return
    
    await event.respond(
        "🔄 **Bot Restart Requested**\n\n"
        "To fully restart the bot:\n"
        "• **Local:** Stop the terminal (Ctrl+C) and run again\n"
        "• **Render:** Dashboard → Manual Deploy\n"
        "• **Railway:** Dashboard → Restart button\n\n"
        "Or just use /cancel to stop current task and start fresh!"
    )

@bot.on(events.NewMessage(pattern='/status'))
async def status_handler(event):
    """Check bot status"""
    if event.sender_id != admin_user_id:
        await event.respond("❌ Sorry, this bot is private.")
        return
    
    uptime = datetime.now()
    await event.respond(
        f"✅ **Bot Status: Online**\n\n"
        f"🕐 Current Time: {uptime.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"👤 Admin ID: {admin_user_id}\n\n"
        f"Use /start to see the menu"
    )

@bot.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    """Show help message"""
    if event.sender_id != admin_user_id:
        await event.respond("❌ Sorry, this bot is private.")
        return
    
    help_text = """
🤖 **Transfer Summary Bot Help**

**Commands:**
/start - Show main menu
/summary - Quick summary for today
/cancel - Cancel current operation
/status - Check if bot is online
/restart - Show restart instructions
/help - Show this help message

**Features:**
• View transactions for today
• View transactions for yesterday
• View last 7 days summary
• View last 10 days of current month

**Supported Platforms:**
• ACLEDA Bank
• PayWay by ABA Bank

**Currencies:**
• KHR (Cambodian Riel)
• USD (US Dollar)

**Note:** Processing may take 10-30 seconds depending on message volume.

**Stuck?** Use /cancel to stop and try again!
"""
    
    await event.respond(help_text)

# Run the bot with auto-reconnect
print("✅ Bot started successfully!")
print("Send /start to your bot to begin")

async def main():
    """Main function with reconnection logic"""
    # Start user client
    await user_client.start()
    print("✅ User client connected")
    
    while True:
        try:
            await bot.run_until_disconnected()
        except KeyboardInterrupt:
            print("\n⚠️ Bot stopped by user")
            break
        except Exception as e:
            print(f"❌ Connection error: {e}")
            print("🔄 Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
            continue

# Run with asyncio
try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    print("\n✅ Bot stopped gracefully")
finally:
    user_client.disconnect()