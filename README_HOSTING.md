# @Mouselucky_bot - HOSTING READY 24/7 VERSION

## OPTION 1: RENDER.COM (Recommended - 100% Free, 2 minutes)

### Step 1: Put code on GitHub
1. Go to github.com -> New Repository -> name: my-personal-bot -> Public
2. Upload all files from this folder (drag & drop). DO NOT upload .env file!
3. Click Commit

### Step 2: Deploy on Render
1. Go to render.com -> Sign up with GitHub (free)
2. Click "New +" -> "Background Worker"
3. Connect your my-personal-bot repository
4. Settings:
   - Name: mouselucky-bot
   - Build Command: pip install -r requirements.txt
   - Start Command: python bot.py
5. Click "Advanced" -> Add Environment Variable
   - Key: TELEGRAM_TOKEN
   - Value: paste your NEW token from @BotFather (after revoking)
6. Click "Create Background Worker"
7. Wait 2 minutes -> Logs will show "Bot @Mouselucky_bot is running!"

DONE! Now you can close your laptop. Bot runs 24/7.

---

## OPTION 2: REPLIT.COM (Easiest for beginners)

1. Go to replit.com -> Sign up
2. Click "Create Repl" -> "Import from GitHub" or Upload Zip
3. After import, click "Secrets" (lock icon on left)
   - Key: TELEGRAM_TOKEN, Value: your token
4. Click "Run" button
5. Click "Deploy" -> Enable "Always On" (needs Replit Hacker for true 24/7, but free will run while tab open)

---

## OPTION 3: RAILWAY.APP (Free $5 credit monthly)

1. railway.app -> Sign up with GitHub
2. New Project -> Deploy from GitHub -> select repo
3. Variables -> Add TELEGRAM_TOKEN
4. Settings -> Start Command: python bot.py
5. Deploy

---

## IMPORTANT SECURITY
- Before pushing to GitHub, make sure .env is NOT included (it's in .gitignore already)
- Revoke your old token first: @BotFather -> /mybots -> @Mouselucky_bot -> API Token -> Revoke
- Use NEW token in Render/Railway environment variables, not in code

## Data persistence note
On free hosting, data.json resets when you redeploy. For permanent memory, we can later add Google Sheets or Firebase - tell me if you want that.

Need help? Send screenshot of Render logs.