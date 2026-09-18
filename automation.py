from brain import get_chat_id

async def morning_briefing_task(bot):
    chat_id = get_chat_id()
    if not chat_id: return
    await bot.send_message(chat_id, "☀️ Good Morning!\n\n📍 Kisumu: 24°C partly cloudy\n📅 Check /start -> My Day\n💡 Discipline beats motivation")

async def water_reminder_task(bot):
    chat_id = get_chat_id()
    if not chat_id: return
    await bot.send_message(chat_id, "💧 Water check - have you drunk water? Tap /start -> Health -> Log Water")

async def night_recap_task(bot):
    chat_id = get_chat_id()
    if not chat_id: return
    await bot.send_message(chat_id, "🌙 Night Recap - How was your day? Send me a note for journal.")

async def expense_summary_task(bot):
    chat_id = get_chat_id()
    if not chat_id: return
    await bot.send_message(chat_id, "💰 Weekly Money Summary - Check /start -> My Money")

async def motivation_task(bot):
    chat_id = get_chat_id()
    if not chat_id: return
    await bot.send_message(chat_id, "🔥 You got this! What is your 1 focus task today?")
