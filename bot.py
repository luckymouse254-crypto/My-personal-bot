import os, sys
print("Checking setup...")

# Check if telegram library exists, give friendly error
try:
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
except ModuleNotFoundError:
    print("\n❌ ERROR: 'telegram' module not found.")
    print("You forgot to install requirements.")
    print("Run: pip install -r requirements.txt")
    print("Or double-click run.bat (Windows) or run.sh (Mac)")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    print("\n❌ ERROR: 'python-dotenv' not found. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ModuleNotFoundError:
    print("\n❌ ERROR: 'apscheduler' not found. Run: pip install -r requirements.txt")
    sys.exit(1)

from brain import save_chat_id, log_expense, log_note, get_chat_id
import automation

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN or "PUT_YOUR" in TOKEN or len(TOKEN) < 20:
    print("\n❌ ERROR: TELEGRAM_TOKEN not found in .env file!")
    print("You need to create a file named .env (not .env.example)")
    print("Inside .env paste ONE line:")
    print("TELEGRAM_TOKEN=your_new_token_from_BotFather")
    print("\nCurrent .env content:", os.getenv("TELEGRAM_TOKEN"))
    sys.exit(1)

print(f"✅ Token found for @Mouselucky_bot - starting bot...")

MAIN_MENU = [
    [InlineKeyboardButton("📅 My Day", callback_data="menu_day"),
     InlineKeyboardButton("✅ Productivity", callback_data="menu_prod")],
    [InlineKeyboardButton("❤️ Health", callback_data="menu_health"),
     InlineKeyboardButton("💰 My Money", callback_data="menu_money")],
    [InlineKeyboardButton("🎓 Learn", callback_data="menu_learn"),
     InlineKeyboardButton("🎮 Fun", callback_data="menu_fun")],
    [InlineKeyboardButton("👨‍👩‍👧 People", callback_data="menu_people"),
     InlineKeyboardButton("🤖 Automation Hub", callback_data="menu_auto")],
]

SUB_MENUS = {
    "menu_day": ["Morning Briefing", "Weather Kisumu", "To-Do List", "Mood Tracker", "End of Day Recap", "Sleep Log", "Affirmation", "Quote of Day"],
    "menu_prod": ["Quick Note", "Set Reminder", "Pomodoro 25min", "Voice to Text", "Add to Calendar", "Focus Mode", "Deadline Countdown", "Scan to PDF"],
    "menu_health": ["Log Water", "Log Meal", "Log Workout", "Sleep Tracker", "Stretch Reminder", "Meditation 5min", "Medicine Reminder", "Mood Journal"],
    "menu_money": ["Log Expense", "M-Pesa Log", "How Much Left", "Bill Reminder", "Savings Goal", "Monthly Report", "Debt Tracker", "Budget Check"],
    "menu_learn": ["Word of Day", "5-Min Lesson", "Summarize YouTube", "Book Summary", "Flashcard Quiz", "Practice Swahili", "News Digest"],
    "menu_fun": ["Meme of Day", "Joke", "Movie Recommender", "Music Finder", "Trivia Game", "Remove BG", "Make Sticker", "Random Fact"],
    "menu_people": ["Birthday Reminder", "Save Contact", "Gift Idea", "SOS Location", "Thank You Writer", "Gratitude Note", "Family Broadcast"],
    "menu_auto": ["Auto Morning 6am ON", "Auto Water Every 2h ON", "Auto Night Recap 10pm ON", "Auto Weekly Money Sun 8pm ON", "Auto Motivation 5:30am ON", "Auto Forward Telegram->WhatsApp", "Auto Save Photos", "Auto Transcribe Voice", "Auto Summarize Links", "Auto Backup Weekly", "Auto KPLC Reminder", "Auto Birthday Wisher", "Auto M-Pesa Logger", "Auto Weather Alert", "Auto Journal 9pm"]
}

def get_main_markup():
    return InlineKeyboardMarkup(MAIN_MENU)

def get_sub_markup(menu_key):
    items = SUB_MENUS.get(menu_key, [])
    keyboard = [[InlineKeyboardButton(text, callback_data=f"action::{menu_key}::{text}")] for text in items]
    keyboard.append([InlineKeyboardButton("⬅️ Back to Main", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)

async def start(update, context):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("🤖 @Mouselucky_bot is LIVE!\n\nI saved your chat ID for automation.\nChoose:", reply_markup=get_main_markup())

async def day_cmd(update, context):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("📅 My Day:", reply_markup=get_sub_markup("menu_day"))

async def money_cmd(update, context):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("💰 My Money:", reply_markup=get_sub_markup("menu_money"))

async def auto_cmd(update, context):
    save_chat_id(update.effective_chat.id)
    await update.message.reply_text("🤖 Automation Hub:", reply_markup=get_sub_markup("menu_auto"))

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "back_main":
        await query.edit_message_text("Main Menu:", reply_markup=get_main_markup())
        return
    if data.startswith("menu_"):
        await query.edit_message_text(f"{data} - Select:", reply_markup=get_sub_markup(data))
        return
    if data.startswith("action::"):
        _, menu_key, action_text = data.split("::", 2)
        response = f"✅ {action_text} selected\n\n"
        if "Log Expense" in action_text:
            response += "Send: spent 250 lunch"
        elif "Log Water" in action_text:
            from brain import log_water
            count = log_water()
            response += f"💧 Logged! Today: {count} times"
        elif "Quick Note" in action_text:
            response += "Send me any text, I will save it"
        elif "Auto Morning" in action_text:
            response += "Enabled! 6am Nairobi daily"
        elif "Auto Water" in action_text:
            response += "Enabled! Every 2h reminder"
        elif "Weather" in action_text:
            response += "Kisumu: 24C partly cloudy"
        elif "To-Do" in action_text:
            response += "Send: todo buy tomatoes"
        else:
            response += "Ready! Logic in bot.py -> button_handler"
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data=menu_key)], [InlineKeyboardButton("🏠 Main", callback_data="back_main")]]
        await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))

async def text_handler(update, context):
    text = update.message.text
    save_chat_id(update.effective_chat.id)
    low = text.lower()
    if "spent" in low or ("kes" in low and any(c.isdigit() for c in low)):
        try:
            import re
            nums = re.findall(r"\d+", text)
            if nums:
                amount = int(nums[0])
                expenses = log_expense(amount, text)
                total = sum(e["amount"] for e in expenses[-7:])
                await update.message.reply_text(f"💰 Logged {amount} KES. Last 7 total: {total} KES", reply_markup=get_main_markup())
                return
        except Exception as e:
            print(e)
    log_note(text)
    await update.message.reply_text(f"📝 Saved: {text[:100]}", reply_markup=get_main_markup())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("day", day_cmd))
    app.add_handler(CommandHandler("money", money_cmd))
    app.add_handler(CommandHandler("automation", auto_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    scheduler = AsyncIOScheduler(timezone="Africa/Nairobi")
    scheduler.add_job(automation.morning_briefing_task, 'cron', hour=6, minute=0, args=[app.bot])
    scheduler.add_job(automation.water_reminder_task, 'interval', hours=2, args=[app.bot])
    scheduler.add_job(automation.night_recap_task, 'cron', hour=22, minute=0, args=[app.bot])
    scheduler.add_job(automation.expense_summary_task, 'cron', day_of_week='sun', hour=20, minute=0, args=[app.bot])
    scheduler.add_job(automation.motivation_task, 'cron', hour=5, minute=30, args=[app.bot])
    scheduler.start()

    print("\n✅ Bot @Mouselucky_bot is running!")
    print("Go to Telegram and send /start")
    print("Press Ctrl+C to stop\n")
    app.run_polling()

if __name__ == "__main__":
    main()
