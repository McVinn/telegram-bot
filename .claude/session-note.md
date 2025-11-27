# Telegram Transfer Summary Bot - Session Note

## Project Overview
**Status**: Development - Working on Features
**Repository**: https://github.com/McVinn/telegram-bot
**Location**: D:\telegram-bot

### What This Bot Does
A Telegram bot that monitors ACLEDA and PayWay transaction notifications from group chats and provides organized summaries across different time periods (today, yesterday, last 7 days, current month). Supports both KHR and USD currencies.

**Key Components**:
- Dual client architecture (bot client for commands + user client for reading groups)
- Pattern matching for transaction detection
- Admin-only access with user ID verification
- Auto-reconnect functionality for stability

---

## Current Development Goal
**PRIMARY FOCUS**: Research and implement hosting solution

**Problem**: Bot currently requires laptop to stay on 24/7 to run
**Goal**: Find and implement a hosting solution for continuous operation

---

## TODOs & Planned Features

### Hosting Research & Implementation (Current Priority)
- [ ] Research free hosting options (Render, Railway, Fly.io, PythonAnywhere, etc.)
- [ ] Research paid hosting options (Heroku, DigitalOcean, AWS, VPS)
- [ ] Compare pros/cons of each platform (cost, uptime, limitations)
- [ ] Understand session file handling for hosted environments
- [ ] Test deployment on chosen platform
- [ ] Set up environment variables on hosting platform
- [ ] Configure auto-restart and monitoring
- [ ] Document deployment process

### Future Improvements
- [ ] Add logging system for debugging
- [ ] Improve error handling and user feedback
- [ ] Add more banks/payment platforms
- [ ] Implement database for transaction history
- [ ] Add export functionality (CSV, Excel)
- [ ] Create admin dashboard for statistics

---

## Important Reminders

### Security Notes
- ⚠️ **NEVER commit .env file** - Contains sensitive API credentials
- ⚠️ **NEVER share BOT_TOKEN publicly** - Anyone can control your bot
- ⚠️ **Session files are sensitive** - They contain authentication data
- ⚠️ Keep API_ID and API_HASH private
- ⚠️ `.gitignore` is configured to protect sensitive files

### Session Files
- Bot creates session files (`.session`) for authentication
- These files must be preserved when moving to hosting
- Session files are gitignored for security

### Environment Variables
```
API_ID, API_HASH, BOT_TOKEN, SESSION_NAME
GROUP_ID, GROUP_ID_PAYWAY, ADMIN_USER_ID
```

---

## Common Commands & Workflows

### Running the Bot Locally
```bash
cd D:\telegram-bot
python telegram_bot.py
```

### Git Workflow
```bash
# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Testing the Bot
1. Start the bot locally
2. Send `/start` to the bot on Telegram
3. Test each time period option
4. Verify transaction parsing
5. Check error handling

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Updating Dependencies
```bash
pip freeze > requirements.txt
```

---

## Bot Commands Reference
- `/start` - Main menu with time period buttons
- `/summary` - Quick summary for today
- `/status` - Check if bot is online
- `/cancel` - Cancel current operation
- `/restart` - Show restart instructions
- `/help` - Show help message

---

## Project Structure
```
telegram-bot/
├── telegram_bot.py      # Main bot code
├── requirements.txt     # Dependencies (telethon, python-dotenv)
├── .env                # Environment variables (GITIGNORED)
├── .env.example        # Template for env vars
├── .gitignore          # Protects sensitive files
├── README.md           # Documentation
└── .claude/            # Claude Code configuration
    └── session-note.md # This file
```

---

## Next Steps
1. Research hosting platform options
2. Compare features, pricing, and limitations
3. Choose the best platform for this bot's needs
4. Test deployment
5. Monitor and optimize

---

**Last Updated**: 2025-11-27
**Working Directory**: D:\telegram-bot
