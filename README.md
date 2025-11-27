# Transfer Summary Bot

A Telegram bot that monitors ACLEDA and PayWay transaction notifications and provides organized summaries for different time periods.

## Features

- **Real-time Transaction Monitoring**: Monitors ACLEDA and PayWay by ABA Bank groups for transaction notifications
- **Multi-Currency Support**: Tracks both KHR (Cambodian Riel) and USD (US Dollar) transactions
- **Flexible Time Periods**: View summaries for:
  - Today
  - Yesterday
  - Last 7 days
  - Current month (last 10 days)
- **Detailed Summaries**: Shows transaction counts and totals per bank and combined totals
- **Private Access**: Admin-only access with user ID verification
- **Auto-Reconnect**: Built-in reconnection logic for stability

## Prerequisites

- Python 3.7 or higher
- A Telegram account
- Telegram API credentials (API ID and API Hash)
- A Telegram bot token from @BotFather
- Access to ACLEDA and PayWay notification groups

## Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your credentials:
     ```bash
     cp .env.example .env
     ```

4. **Get your Telegram credentials**:
   - **API ID & API Hash**: Visit https://my.telegram.org/apps
   - **Bot Token**: Chat with @BotFather on Telegram and create a new bot
   - **User ID**: Chat with @userinfobot to get your user ID
   - **Group IDs**: Add the bot to your groups and use the group info to get the IDs

## Configuration

Edit the `.env` file with your credentials:

```env
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=telegram_session_name
GROUP_ID=your_acleda_group_id
GROUP_ID_PAYWAY=your_payway_group_id
BOT_TOKEN=your_bot_token
ADMIN_USER_ID=your_telegram_user_id
```

## Usage

1. **Start the bot**:
   ```bash
   python telegram_bot.py
   ```

2. **First run**: You'll need to authenticate your user account (one-time setup)

3. **Available commands**:
   - `/start` - Show main menu with time period options
   - `/summary` - Quick summary for today
   - `/status` - Check if bot is online
   - `/cancel` - Cancel current operation
   - `/restart` - Show restart instructions
   - `/help` - Show help message

## How It Works

1. **Dual Client Architecture**:
   - Bot client handles user commands
   - User client reads messages from groups

2. **Transaction Detection**:
   - Scans messages for transaction patterns
   - Supports ACLEDA and PayWay message formats
   - Extracts amount and currency information

3. **Summary Generation**:
   - Groups transactions by date
   - Calculates totals per bank and currency
   - Provides combined summary across both accounts

## Supported Transaction Formats

### ACLEDA
- `Received [amount] KHR/USD`
- `[amount] រៀល` (Khmer for Riel)
- `[amount] ដុល្លារ` (Khmer for Dollar)

### PayWay by ABA
- `៛[amount] paid by`
- `$[amount] paid by`

## Deployment

### Local Deployment
Simply run the bot:
```bash
python telegram_bot.py
```

### Cloud Deployment (Render/Railway)
1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Add environment variables in the platform dashboard
3. Deploy and monitor logs

## Troubleshooting

- **Bot not responding**: Check if it's running with `/status`
- **No transactions found**: Verify group IDs are correct
- **Timeout errors**: Reduce message limit in code (currently 500)
- **Stuck processing**: Use `/cancel` to stop current operation

## Security Notes

- Never commit `.env` file to version control
- Keep your API credentials private
- Only share bot token with trusted services
- The bot is configured for single admin use only

## License

This project is open source and available for personal use.

## Support

For issues or questions, please check:
- Bot logs for error messages
- `.env` configuration
- Group permissions and IDs
- Internet connection stability
