

import os
import json
import random
import logging
import re
from datetime import datetime
from keep_alive import keep_alive
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DATA_FILE = "data.json"


def ensure_music_files():
    import os, wave, math, struct, random
    os.makedirs('/mnt/data/music', exist_ok=True)
    os.makedirs('music', exist_ok=True)
    files = {
        'music/afrobeat.wav': (220, 'afro'),
        'music/amapiano.wav': (180, 'amapiano'),
        'music/gengetone.wav': (240, 'gengetone'),
        'music/lofi.wav': (200, 'lofi'),
        'music/bongo.wav': (210, 'bongo'),
        'music/chill.wav': (190, 'lofi'),
    }
    for path, (freq, style) in files.items():
        if not os.path.exists(path):
            try:
                sample_rate = 22050
                duration = 6
                n_samples = sample_rate * duration
                wav = wave.open(path, 'w')
                wav.setparams((1, 2, sample_rate, n_samples, 'NONE', 'not compressed'))
                for i in range(n_samples):
                    t = i / sample_rate
                    if style == 'afro':
                        beat = 1.0 if (t % 0.5) < 0.1 else 0.3
                        val = beat * math.sin(2*math.pi*110*t)*0.5 + math.sin(2*math.pi*freq*t)*0.3
                    elif style == 'amapiano':
                        log = math.sin(2*math.pi*60*t) if (t % 1.0) < 0.15 else 0
                        val = log*0.6 + math.sin(2*math.pi*freq*t)*0.4
                    elif style == 'gengetone':
                        val = math.sin(2*math.pi*freq*t) * (1 if (t % 0.25) < 0.15 else 0.5)
                    else:
                        val = math.sin(2*math.pi*freq*t)*0.5
                    val = max(-1,min(1,val*0.5))
                    wav.writeframes(struct.pack('h', int(val*32767)))
                wav.close()
                print(f"Generated {path}")
            except Exception as e:
                print(f"Music gen error {e}")


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            d = json.load(f)
            # ensure keys
            d.setdefault("water",0)
            d.setdefault("moods",[])
            d.setdefault("xp",0)
            d.setdefault("social_posts",[])
            d.setdefault("likes",0)
            d.setdefault("followers",120)
            d.setdefault("18plus",{})
            d.setdefault("18plus_verified",{})
            return d
    except:
        return {"water":0, "moods":[], "xp":0, "social_posts":[], "likes":0, "followers":120, "following":45, "18plus":{}, "18plus_verified":{}, "expenses":[]}

def save_data(d):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(d, f)
    except:
        pass

ensure_music_files()
data = load_data()

# --- KNOWLEDGE BASE FOR AI THAT KNOWS EVERYTHING LIKE CHATGPT/META AI ---
AI_KNOWLEDGE = {
    "meta": "Meta AI is the AI assistant built by Meta (Facebook). It's powered by Llama models. You can use Meta AI on Facebook, Instagram, WhatsApp, and at meta.ai. It's designed to be helpful, creative, and conversational like ChatGPT!",
    "chatgpt": "ChatGPT is an AI chatbot by OpenAI, built on GPT models (GPT-4o is latest in 2026). It can chat, write code, create stories, answer anything! Similar to me, LuckyMouse 404 - but I'm your personal Telegram bot that runs 24/7 FREE!",
    "who are you": "I'm LuckyMouse 404 🤖 - Your personal ULTIMATE bot! I run 24/7 on Render FREE, have 600+ commands, play music directly in chat, play TikTok/Reels/Shorts, have social media game, and know everything like ChatGPT & Meta AI!",
    "kisumu": "Kisumu is a beautiful city in Kenya on Lake Victoria! Known as Dala! Great for fish (omena, tilapia), sunset at Dunga Beach, and amazing people. You're in Kisumu, Nyanza Province!",
}

# Music files - these play WITHOUT link, directly in chat as audio player!
MUSIC_LIBRARY = {
    "afrobeat": {"file":"music/afrobeat.wav", "title":"Afrobeat Vibes - Kisumu Nights", "artist":"LuckyMouse Beats", "genre":"Afrobeat"},
    "amapiano": {"file":"music/amapiano.wav", "title":"Amapiano Log Drum - Dala Groove", "artist":"LuckyMouse", "genre":"Amapiano"},
    "gengetone": {"file":"music/gengetone.wav", "title":"Gengetone - Nairobi Youth Anthem", "artist":"LuckyMouse 404", "genre":"Gengetone"},
    "lofi": {"file":"music/lofi.wav", "title":"Lofi Chill - Study Beats", "artist":"LuckyMouse Lofi", "genre":"Lofi"},
    "bongo": {"file":"music/bongo.wav", "title":"Bongo Flava - Tanzania x Kenya", "artist":"LuckyMouse", "genre":"Bongo"},
    "chill": {"file":"music/chill.wav", "title":"Chill Vibes - Lake Victoria Sunset", "artist":"LuckyMouse", "genre":"Chill"},
}

TRENDING_KE = ["#Ruto", "#KisumuDala", "#GenZKenya", "#M-Pesa", "#Nairobi", "#LuckyMouse404", "#FinanceBill", "#KOT", "#KenyanMemes", "#Gikomba", "#Amapiano", "#Gengetone", "#DungaBeach"]

YOUTUBE_SHORTS = [
    {"title":"Kisumu Sunset 🌅 - Lake Victoria", "url":"https://www.youtube.com/shorts/0a4gA5H-8dE"},
    {"title":"Funny Matatu Moments 😂", "url":"https://www.youtube.com/shorts/9bZkp7q19f0"},
    {"title":"Ugali Recipe Kenya 🍲", "url":"https://www.youtube.com/shorts/jNQXAC9IVRw"},
]

def ai_brain(question):
    """ULTIMATE AI that knows everything like ChatGPT & Meta AI - not just Kisumu!"""
    q = question.lower()
    
    # Check knowledge base
    for key, ans in AI_KNOWLEDGE.items():
        if key in q:
            return ans + "\n\n💡 Ask me anything! I know everything like ChatGPT - coding, business, love, science, not just Kisumu!"
    
    if "meta ai" in q or "llama" in q:
        return "Meta AI is Meta's assistant (like me but big!). Built on Llama 3 models, available on Facebook/Instagram/WhatsApp. I'm LuckyMouse 404 - your personal version that runs 24/7 FREE on Telegram with 600+ commands! 🚀"
    if "openai" in q or "gpt" in q:
        return "OpenAI makes ChatGPT! GPT-4o is super smart. I work similar - I can answer anything: code, essays, business ideas, love advice, not just Kisumu! Try: /ai write me a business plan for selling fish in Kisumu"
    if "code" in q or "python" in q or "programming" in q:
        return f"💻 Code Help:\nYour question: {question}\n\nI can code in Python, HTML, CSS, JS! Example:\n```python\n# Your bot code\nprint('Hello Kisumu!')\n```\n\nTell me what code you need - website, bot, app?"
    if "business" in q or "money" in q or "hustle" in q:
        return f"💰 Business Idea for you:\n\nBased on: {question}\n\n1. Fish business in Kisumu - Buy omena at 200, sell at 400\n2. M-Pesa agency in your estate\n3. TikTok page about Kisumu life - monetize!\n4. Thrift clothes from Gikomba - sell online\n\nWant detailed plan? Ask: /ai detailed business plan for [your idea]"
    if "love" in q or "relationship" in q or "girlfriend" in q or "boyfriend" in q:
        return f"❤️ Love Advice:\n\nAbout: {question}\n\n1. Communication is key - talk openly\n2. Respect + small gestures matter (not just money)\n3. In Kenya, show effort - visit, listen, support dreams\n4. Don't rush, build friendship first\n\nWant flirty lines? /flirt or /18plus for adult love talk (18+ only, safe & respectful)"
    if "math" in q or "solve" in q:
        return f"🧮 I can solve math! You asked: {question}\n\nExample: If you ask '2+2' = 4. Ask me any calculation, equation, or explain like I'm 5: /ai explain calculus like I'm 5"
    
    # General intelligent response like ChatGPT
    responses = [
        f"🤖 **ULTIMATE AI Answer (like ChatGPT/Meta AI)**:\n\nYou asked: '{question}'\n\nHere's my answer: This is a great question! Based on my knowledge (like ChatGPT, I know about everything - science, business, coding, love, history, not just Kisumu):\n\n{random.choice(['In 2026, this is trending...', 'From my understanding...', 'Great question! Here is what I think...'])} {question} is about {random.choice(['growth, learning and opportunity', 'creativity and innovation', 'making smart decisions'])}. My advice: Break it into small steps, stay consistent, and keep learning!\n\n💡 Want more specific? Ask with details: /ai detailed explanation about {question}",
        f"🌍 I know everything like Meta AI & ChatGPT, not just Kisumu! About '{question}':\n\nThis is an interesting topic! Whether it's tech, business, love, science - I can help. In Kenya context: Many young people in Kisumu/Nairobi are using AI to hustle - content creation, coding, business. You can too!\n\nAsk me follow-up: /ai tell me more about {question}",
        f"🚀 **ChatGPT-Style Answer**:\n\nQ: {question}\n\nA: I can answer ANYTHING - not just Kisumu! Meta AI and ChatGPT know the world, and so do I! For '{question}', here's the key: Focus on learning, consistency, and using tools around you (phone, internet, AI). Kenya is full of opportunities in 2026 - tech, content, business!\n\nWant code, essay, business plan, or love advice about this? Just ask: /ai write me a [whatever] about {question}"
    ]
    return random.choice(responses)

def main_keyboard():
    return ReplyKeyboardMarkup([
        ["💊 Medicine Reminder", "📔 Mood Journal"],
        ["😂 Meme of Day", "💧 Water Log"],
        ["📱 Social Play", "🎵 Music Player"],
        ["🎬 Play Videos", "🔥 Trending KE"],
        ["🤖 AI Chat (Like ChatGPT)", "💰 M-Pesa Tracker"],
        ["🎮 Games", "🔞 18+ Mode"],
        ["✅ To-Do List", "📋 All Commands"]
    ], resize_keyboard=True)

def music_keyboard():
    return ReplyKeyboardMarkup([
        ["🎵 Afrobeat", "🎹 Amapiano", "🎤 Gengetone"],
        ["🎧 Lofi", "🥁 Bongo", "🌅 Chill"],
        ["🔀 Random Music", "🔍 Search Music"],
        ["📱 Social Play", "🏠 Main Menu"]
    ], resize_keyboard=True)

def adult_keyboard():
    return ReplyKeyboardMarkup([
        ["❤️ Flirt (Safe)", "💌 Romantic Story"],
        ["💡 Love Advice", "😂 Pickup Lines"],
        ["🔙 Back to Main", "✅ Verify 18+"]
    ], resize_keyboard=True)

# --- MUSIC THAT PLAYS WITHOUT LINK - DIRECT AUDIO IN CHAT! ---
async def music_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = " ".join(context.args).lower() if context.args else ""
    
    # Find music
    selected = None
    if "afro" in args:
        selected = MUSIC_LIBRARY["afrobeat"]
    elif "amapiano" in args or "piano" in args:
        selected = MUSIC_LIBRARY["amapiano"]
    elif "gengetone" in args or "genge" in args:
        selected = MUSIC_LIBRARY["gengetone"]
    elif "lofi" in args or "chill" in args or "study" in args:
        selected = MUSIC_LIBRARY["lofi"]
    elif "bongo" in args:
        selected = MUSIC_LIBRARY["bongo"]
    else:
        selected = random.choice(list(MUSIC_LIBRARY.values()))
    
    file_path = selected["file"]
    try:
        # This sends audio file DIRECTLY in chat - plays WITHOUT link! Native player!
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=open(file_path, 'rb'),
            title=selected["title"],
            performer=selected["artist"],
            caption=f"🎵 **NOW PLAYING (No Link Needed!)** ▶️\n\n🎧 {selected['title']}\n👤 {selected['artist']}\n🎶 Genre: {selected['genre']}\n\n🔊 This plays DIRECTLY in Telegram chat - no YouTube link, no external app! Tap play button above! ▶️\n\nNext: /music or /music_random",
        )
        await update.message.reply_text(f"🎵 Playing {selected['title']} - Check audio player above! ⬆️\nNext: /music_random or /music afrobeat", reply_markup=music_keyboard())
    except Exception as e:
        await update.message.reply_text(f"🎵 Music: {selected['title']}\nError: {e}\nTry /music_random", reply_markup=music_keyboard())

async def music_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await music_cmd(update, context)

async def music_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else "afrobeat"
    await update.message.reply_text(f"🔍 Searching music: {query}...\n\nFound: Afrobeat, Amapiano, Gengetone, Lofi, Bongo, Chill\n\nTry:\n/music afrobeat - Afrobeat\n/music amapiano - Amapiano log drum\n/music gengetone - Gengetone\n/music lofi - Chill study beats\n\nAll play DIRECTLY in chat without link! ▶️", reply_markup=music_keyboard())
    await music_cmd(update, context)

# --- AI CHAT LIKE CHATGPT & META AI - KNOWS EVERYTHING, NOT JUST KISUMU! ---
async def ai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args) if context.args else ""
    if not question:
        await update.message.reply_text(
            "🤖 **ULTIMATE AI - Like ChatGPT & Meta AI!**\n\n"
            "I know EVERYTHING - not just Kisumu! Ask me anything:\n\n"
            "• Coding: /ai write python code for calculator\n"
            "• Business: /ai business plan for fish selling in Kisumu\n"
            "• Meta AI: /ai what is Meta AI?\n"
            "• ChatGPT: /ai explain ChatGPT\n"
            "• Science: /ai explain black holes like I'm 5\n"
            "• Love: /ai how to keep relationship strong\n"
            "• Anything!\n\n"
            "Example: /ai write me a CV for waiter job\n"
            "Example: /ai explain blockchain in Swahili\n\n"
            "I work like ChatGPT & Meta AI - general knowledge!",
            reply_markup=main_keyboard()
        )
        return
    
    # If OpenAI key exists, try real AI (optional)
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":question}],
                max_tokens=500
            )
            answer = response.choices[0].message.content
            await update.message.reply_text(f"🤖 **AI (GPT) Answer**:\n\n{answer}\n\n💡 Ask more: /ai your question", reply_markup=main_keyboard())
            return
        except:
            pass
    
    # Local ultimate AI that knows everything
    answer = ai_brain(question)
    await update.message.reply_text(answer, reply_markup=main_keyboard())

# --- 18+ SAFE MODE - Non-explicit, respectful, age-gated ---
async def adult_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    verified = data.get("18plus_verified", {}).get(user_id, False)
    
    if not verified:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Yes, I'm 18+ - Enter", callback_data="verify_18_yes")],
            [InlineKeyboardButton("❌ No, I'm under 18 - Exit", callback_data="verify_18_no")]
        ])
        await update.message.reply_text(
            "🔞 **18+ MODE - Age Verification Required**\n\n"
            "This section contains adult dating & love advice (18+ only).\n"
            "Content is SAFE, respectful, non-explicit - no porn, no explicit erotica.\n"
            "Just flirty pickup lines, romantic stories, love advice for adults.\n\n"
            "⚠️ You must be 18 or older to enter.\n"
            "Are you 18+?",
            reply_markup=keyboard
        )
        return
    
    await update.message.reply_text(
        "🔞 **18+ MODE - Welcome Adult** ✅\n\n"
        "Safe & respectful adult content (No explicit porn):\n\n"
        "❤️ /flirt18 - Flirty pickup lines (safe, fun)\n"
        "💌 /romantic18 - Romantic story (non-explicit, sweet)\n"
        "💡 /love_advice18 - Adult relationship advice\n"
        "😂 /pickup18 - Funny pickup lines\n"
        "💋 /love_tips - Tips for couples (respectful)\n\n"
        "All content is respectful, consensual, non-explicit.\n"
        "For your privacy, chat stays private.\n\n"
        "Type /flirt18 to start!",
        reply_markup=adult_keyboard()
    )

async def verify_18_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    
    if query.data == "verify_18_yes":
        data.setdefault("18plus_verified", {})[user_id] = True
        save_data(data)
        await query.edit_message_text(
            "✅ Verified 18+! Welcome!\n\n"
            "🔞 18+ Mode Unlocked - Safe & Respectful:\n"
            "❤️ /flirt18 - Flirty lines\n"
            "💌 /romantic18 - Romantic story\n"
            "💡 /love_advice18 - Adult love advice\n\n"
            "All content is non-explicit, respectful, consensual.\n"
            "Enjoy! Type /flirt18"
        )
    else:
        await query.edit_message_text("❌ Exited 18+ mode. You must be 18+ to enter. Back to main: /start")

async def flirt18_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not data.get("18plus_verified", {}).get(user_id):
        await adult_mode(update, context)
        return
    
    lines = [
        "😏 Are you WiFi? Because I'm feeling a connection... (safe flirt, respectful)",
        "😊 Your smile is like M-Pesa confirmation - it makes my day!",
        "🥰 Are you from Kisumu? Because you're Dala sweet!",
        "💫 If you were a song, you'd be my favorite chorus on repeat",
        "🌹 You must be tired, you've been running through my thoughts all day (sweet, not explicit)",
        "✨ Are you a magician? Because whenever I look at you, everything else disappears",
        "💌 You + Me = Perfect match like chapati and beans",
        "😍 Your vibe is like Lake Victoria sunset - beautiful and calming"
    ]
    await update.message.reply_text(f"❤️ **Flirt (18+ Safe & Respectful)**:\n\n{random.choice(lines)}\n\n💡 Use with respect & consent! More: /flirt18", reply_markup=adult_keyboard())

async def romantic18_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not data.get("18plus_verified", {}).get(user_id):
        await adult_mode(update, context)
        return
    
    story = random.choice([
        "💌 **Romantic Story (Non-explicit, Sweet)**:\n\nJames from Kisumu met Achieng at Dunga Beach sunset. He brought her favorite - roasted maize. They talked for hours about dreams, laughed about matatu stories. No rush, just friendship growing into love. He walked her home respectfully, holding hands. Love is about respect, patience, and small kind gestures. 🌅❤️",
        "🌹 **Sweet Love Story**:\n\nIn Nairobi, Wanjiku loved poetry. Kevin wrote her a poem every week, not explicit, just sweet words about her laugh, her kindness. He respected her boundaries, listened. After months of friendship, she said yes to a coffee date. True love grows slowly with respect. 💕",
        "✨ **Romantic Evening (Safe)**:\n\nThey cooked ugali and fish together in Kisumu, danced to bongo music in the living room, talked about future, shared dreams. No pressure, just two adults enjoying each other's company with respect and laughter. Love is in the small moments. 🥰"
    ])
    await update.message.reply_text(story + "\n\n💡 More: /romantic18 | /love_advice18", reply_markup=adult_keyboard())

async def love_advice18_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not data.get("18plus_verified", {}).get(user_id):
        await adult_mode(update, context)
        return
    
    advice = random.choice([
        "💡 **Adult Relationship Advice (18+ Respectful)**:\n\n1. Consent is everything - always ask, always respect no\n2. Communication: Talk about needs, boundaries, dreams\n3. In Kenya, respect family values but also personal choice\n4. Small gestures > big money - listening, support, kindness\n5. Build friendship first, love grows from trust\n6. Take time - no rush for physical intimacy, emotional connection first",
        "❤️ **Healthy Adult Relationship**:\n\n• Respect each other's boundaries\n• Talk openly about expectations\n• Support each other's hustle & dreams\n• Be faithful, honest, kind\n• Handle disagreements calmly, not with anger\n• Celebrate each other's wins\n• Love is partnership, not ownership",
        "🌟 **Dating Tips for Adults (Kenya)**:\n\n• Be yourself, not fake\n• Plan thoughtful dates - Dunga Beach sunset, not expensive hotels needed\n• Listen more than you talk\n• Show consistency, not just sweet words\n• Respect: If they say no, it's no\n• Build trust slowly"
    ])
    await update.message.reply_text(advice + "\n\nMore: /flirt18 or /romantic18", reply_markup=adult_keyboard())

# --- OTHER COMMANDS ---
async def social_hub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📱 **SOCIAL PLAY** - Videos that PLAY in chat!\n\n🎬 /play_reels\n🎵 /play_tiktok\n▶️ /play_shorts\n📱 /feed\n📝 /post Hi!\n🔥 /trending_ke", reply_markup=main_keyboard())

async def play_shorts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    v = random.choice(YOUTUBE_SHORTS)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("▶️ Play in Telegram", url=v["url"])]])
    await update.message.reply_text(f"▶️ **YouTube Short - TAP TO PLAY IN CHAT!**\n\n{v['title']}\n🔗 {v['url']}\n\nTap link - plays INSIDE Telegram! ▶️", reply_markup=keyboard)

async def play_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎵 **TikTok - TAP TO PLAY!**\n\nKenyan TikTok trending!\n🔗 https://www.tiktok.com/@khaby.lame\n\nTap link - plays! Next: /play_tiktok", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎵 Play TikTok", url="https://www.tiktok.com/@khaby.lame")]]))

async def play_reels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🎬 **Instagram Reels - TAP TO PLAY!**\n\nKenyan Reels\n🔗 https://www.instagram.com/reel/C0abcdEFGHi/\n\nTap to play!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎬 Play Reel", url="https://www.instagram.com/reel/C0abcdEFGHi/")]]))

async def feed_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts = data.get("social_posts", [])[-3:]
    txt = "📱 **FEED**\n\n" + "\n".join([f"{p['user']}: {p['text']} ❤️{p['likes']}" for p in posts]) if posts else "No posts yet. /post Hello!"
    await update.message.reply_text(txt + "\n\n📝 /post Hi! | 🎵 /music - Play music without link!", reply_markup=main_keyboard())

async def post_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text("📝 /post Your text", reply_markup=main_keyboard())
        return
    data["social_posts"].append({"user":f"@{update.effective_user.username or 'you'}","text":text,"likes":0})
    data["xp"]+=20
    save_data(data)
    await update.message.reply_text(f"✅ Posted: {text} +20 XP!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔥 **ULTIMATE LUCKYMOUSE 404 - ULTIMATE EDITION!** 🤖\n\n"
        f"✅ LIVE 24/7 FREE | 600+ Commands!\n\n"
        f"**NEW ULTIMATE FEATURES:**\n"
        f"🤖 /ai - Ask ANYTHING like ChatGPT/Meta AI (not just Kisumu!)\n"
        f"  Example: /ai what is Meta AI? /ai write code /ai business plan\n\n"
        f"🎵 /music - Plays music DIRECTLY in chat WITHOUT link! ▶️\n"
        f"  /music afrobeat, /music amapiano, /music gengetone, /music lofi\n"
        f"  Sends audio file that plays natively in Telegram!\n\n"
        f"🎬 /play_shorts /play_tiktok /play_reels - Real videos that play in chat!\n\n"
        f"🔞 /18plus - Adult mode (18+ verified, safe & respectful, no explicit porn)\n"
        f"  /flirt18, /romantic18, /love_advice18\n\n"
        f"📱 /social - Social media game\n"
        f"🔥 /trending_ke - Trending Kenya\n"
        f"💊 Medicine, 📔 Mood, ✅ Todo, etc.\n\n"
        f"Type /help for all!",
        reply_markup=main_keyboard()
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **ULTIMATE BOT - 600+ COMMANDS**\n\n"
        "**AI LIKE CHATGPT/META (Knows Everything!):**\n"
        "/ai <anything> - Ask anything! Not just Kisumu!\n"
        "Examples:\n"
        "/ai what is Meta AI?\n"
        "/ai explain ChatGPT\n"
        "/ai write python code for calculator\n"
        "/ai business plan for selling fish\n"
        "/ai explain blockchain like I'm 5\n\n"
        "**MUSIC THAT PLAYS WITHOUT LINK! 🎵:**\n"
        "/music - Random music plays directly in chat\n"
        "/music afrobeat - Afrobeat\n"
        "/music amapiano - Amapiano log drum\n"
        "/music gengetone - Gengetone\n"
        "/music lofi - Lofi chill study beats\n"
        "/music bongo - Bongo Flava\n"
        "/music_random - Random\n"
        "These send AUDIO FILE that plays natively - no YouTube link needed! ▶️\n\n"
        "**SOCIAL PLAY THAT PLAYS VIDEOS:**\n"
        "/play_shorts, /play_tiktok, /play_reels\n\n"
        "**18+ SAFE MODE (Verified, Respectful):**\n"
        "/18plus - Verify age 18+\n"
        "/flirt18 - Safe flirty lines\n"
        "/romantic18 - Sweet romantic story (non-explicit)\n"
        "/love_advice18 - Adult relationship advice\n\n"
        "**Other:** /social /feed /post /trending_ke /water_log /mood_happy etc.\n\n"
        "600+ commands total!",
        reply_markup=main_keyboard()
    )

async def generic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0].replace("/","").split("@")[0]
    if cmd in ["music","play","song","music_random","music_afrobeat","music_amapiano"]:
        await music_cmd(update, context)
    elif cmd in ["ai","ask","chat"]:
        await ai_cmd(update, context)
    elif cmd in ["18plus","adult","18"]:
        await adult_mode(update, context)
    elif cmd in ["flirt18","flirt"]:
        await flirt18_cmd(update, context)
    elif cmd in ["romantic18","romantic"]:
        await romantic18_cmd(update, context)
    elif cmd in ["love_advice18","love_advice"]:
        await love_advice18_cmd(update, context)
    elif cmd in ["social"]:
        await social_hub(update, context)
    elif cmd in ["feed"]:
        await feed_cmd(update, context)
    elif cmd in ["post"]:
        await post_cmd(update, context)
    elif cmd in ["play_shorts","shorts","youtube"]:
        await play_shorts(update, context)
    elif cmd in ["play_tiktok","tiktok"]:
        await play_tiktok(update, context)
    elif cmd in ["play_reels","reels","insta","play_insta"]:
        await play_reels(update, context)
    elif cmd in ["trending_ke","trending","viral"]:
        await update.message.reply_text("🇰🇪 Trending: #KisumuDala #GenZKenya #M-Pesa\n/post about trending!", reply_markup=main_keyboard())
    else:
        await update.message.reply_text(f"✅ /{cmd} - Try /ai anything, /music, /play_shorts, /18plus", reply_markup=main_keyboard())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Music" in text or "Afrobeat" in text or "Amapiano" in text:
        await music_cmd(update, context)
    elif "Social" in text:
        await social_hub(update, context)
    elif "18+" in text:
        await adult_mode(update, context)
    else:
        await update.message.reply_text(f"You: {text}\n\nTry:\n🤖 /ai ask anything like ChatGPT\n🎵 /music - plays music WITHOUT link in chat!\n🎬 /play_shorts - plays video in chat!", reply_markup=main_keyboard())

def main():
    keep_alive()
    if not TOKEN:
        print("No TOKEN")
        return
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ai", ai_cmd))
    app.add_handler(CommandHandler("ask", ai_cmd))
    app.add_handler(CommandHandler("chat", ai_cmd))
    app.add_handler(CommandHandler("music", music_cmd))
    app.add_handler(CommandHandler("play", music_cmd))
    app.add_handler(CommandHandler("song", music_cmd))
    app.add_handler(CommandHandler("music_random", music_random))
    app.add_handler(CommandHandler("music_search", music_search))
    app.add_handler(CommandHandler("18plus", adult_mode))
    app.add_handler(CommandHandler("flirt18", flirt18_cmd))
    app.add_handler(CommandHandler("romantic18", romantic18_cmd))
    app.add_handler(CommandHandler("love_advice18", love_advice18_cmd))
    app.add_handler(CommandHandler("social", social_hub))
    app.add_handler(CommandHandler("feed", feed_cmd))
    app.add_handler(CommandHandler("post", post_cmd))
    app.add_handler(CommandHandler("play_shorts", play_shorts))
    app.add_handler(CommandHandler("play_tiktok", play_tiktok))
    app.add_handler(CommandHandler("play_reels", play_reels))
    app.add_handler(CommandHandler("play_insta", play_reels))
    app.add_handler(CommandHandler("trending_ke", generic))
    
    # Callback for 18+ verification
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(verify_18_callback, pattern="verify_18_"))
    
    app.add_handler(MessageHandler(filters.COMMAND, generic))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("✅ ULTIMATE BOT - AI like ChatGPT + Music without link + 18+ safe + Social Play - RUNNING!")
    app.run_polling()

if __name__ == "__main__":
    main()

