# Forex Discord Bot 📈

An automated bot that extracts daily forex events from Forex Factory and posts them to Discord with color-coded impact levels.

## Features ✨

- 🔴 **High Impact Events** - Major market movers
- 🟡 **Medium Impact Events** - Moderate market influence  
- 🟢 **Low Impact Events** - Minor market impact
- 📅 **Daily Automation** - Runs every day at 8:00 AM EST
- 📊 **Professional Formatting** - Clean table format with all event details
- ⏰ **Smart Timestamps** - Handles missing timestamps by using previous event time

## Setup 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/forex-discord-bot.git
cd forex-discord-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Discord Webhook
Update the `webhook_url` in `forex_discord_bot.py` with your Discord webhook URL:
```python
webhook_url = "YOUR_DISCORD_WEBHOOK_URL_HERE"
```

### 4. Run the Bot
```bash
python forex_discord_bot.py
```

## Deployment Options 🌐

### Railway (Recommended)
1. Connect your GitHub repo to Railway
2. Add your Discord webhook URL as an environment variable
3. Set up a cron job to run daily at 8:00 AM EST
4. Deploy!

### DigitalOcean Droplet
1. Create a $4/month droplet
2. Install Python and dependencies
3. Set up a cron job:
   ```bash
   0 8 * * * /usr/bin/python3 /path/to/forex_discord_bot.py
   ```

### Google Cloud Functions
1. Convert to Cloud Function format
2. Set up Cloud Scheduler trigger
3. Deploy via gcloud CLI

## File Structure 📁

```
forex-discord-bot/
├── forex_discord_bot.py      # Main bot script
├── forex_scraper.py          # Web scraping utilities
├── forex_daemon_scraper.py   # Daemon helper script
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore file
```

## Sample Output 📋

```
🔔 @everyone 🔔

📅 News Events: 09/23/2025

Time      Curr Imp Event                               Actual   Forecast Previous
─────────────────────────────────────────────────────────────────────────────────
12:15am   EUR  🟡  French Flash Manufacturing PMI      -        50.2     50.4    
12:15am   EUR  🟡  French Flash Services PMI           -        49.7     49.8    
12:30am   EUR  🔴  German Flash Manufacturing PMI      -        50.0     48.8    
12:30am   EUR  🔴  German Flash Services PMI           -        49.5     49.3    
9:35am    USD  🔴  Fed Chair Powell Speaks             -        -        -       

🔴 High Impact  🟡 Medium Impact  🟢 Low Impact
```

## Environment Variables 🔧

For deployment platforms, set these environment variables:

- `DISCORD_WEBHOOK_URL` - Your Discord webhook URL

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is open source and available under the [MIT License](LICENSE).

## Support 💬

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Happy Trading! 📈💰**