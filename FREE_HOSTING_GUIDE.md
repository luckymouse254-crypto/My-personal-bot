FREE 24/7 HOSTING - $0 - NO CARD NEEDED

YOUR BEST OPTIONS (pick one):

=== OPTION A: KOYEB.COM (RECOMMENDED - TRUE 24/7 FREE, NO SLEEP) ===
1. Go to koyeb.com -> Sign up with GitHub (free)
2. Click "Create App" -> "Deploy from GitHub"
3. Select your repo: My-personal-bot
4. Builder: Dockerfile (or Python)
5. IMPORTANT Settings:
   - Instance type: Free / Nano (0.1 CPU, 512MB) - it's free
   - Start command: python bot.py
   - Port: 8000 (if asked)
6. Environment Variables -> Add:
   - TELEGRAM_TOKEN = your new token
7. Deploy -> Wait 2 mins -> Logs show "Bot is running!"
DONE - Never sleeps, truly 24/7 free.

=== OPTION B: RENDER FREE WEB SERVICE + UPTIMEROBOT (100% FREE) ===
Render free WEB SERVICE is free, but sleeps after 15 mins. We trick it to stay awake.

1. On Render.com, instead of Background Worker, choose "Web Service" (free)
   - Connect your My-personal-bot repo
   - Build: pip install -r requirements.txt
   - Start: python bot.py
   - Add env var TELEGRAM_TOKEN
   - Create Web Service (FREE)

2. After it deploys, copy your Render URL (like https://my-personal-bot-xxxx.onrender.com)

3. Go to uptimerobot.com -> Sign up free
   - Add New Monitor -> HTTP(s)
   - URL: paste your Render URL
   - Interval: 5 minutes
   - Create

UptimeRobot will ping your bot every 5 mins, keeping it awake 24/7 for free!

=== OPTION C: FLY.IO (FREE) ===
1. Install flyctl, run fly launch
2. Choose free tier
3. fly secrets set TELEGRAM_TOKEN=your_token
4. fly deploy

=== OPTION D: KEEP LAPTOP RUNNING FOR FREE ===
If you can't host now, just keep laptop version:
- Keep black window open
- Set Windows: Settings -> Power -> Never sleep when plugged in
- Bot runs while laptop is on - 100% free

No money needed!