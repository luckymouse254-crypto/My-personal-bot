# @Mouselucky_bot - FIXED VERSION - Only create .env

## You only need to do 1 thing: create .env file

### Step 1: Create .env file
Right-click in this folder -> New File -> name it exactly .env
Inside paste ONE line:
TELEGRAM_TOKEN=your_new_token_from_BotFather

Example:
TELEGRAM_TOKEN=1234567890:AAHxyz...

### Step 2: Double-click to run (Windows)
Just double-click run.bat - it will create venv, install everything, and start bot automatically.

Or manual:
pip install -r requirements.txt
python bot.py

### Step 3: Test
Telegram -> @Mouselucky_bot -> /start

That's it! Only .env file needed.

### Security
- NEVER share your token. You posted old token publicly, you MUST revoke at @BotFather -> /mybots -> @Mouselucky_bot -> Revoke Token
- .env is already in .gitignore so it won't go to GitHub

### If error "No module named telegram"
You forgot pip install -r requirements.txt - or just double-click run.bat which does it automatically.
