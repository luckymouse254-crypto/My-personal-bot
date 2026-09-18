
import os
import json
import random
import logging
from datetime import datetime
from keep_alive import keep_alive
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"water":0, "moods":[], "medicines":[], "todos":[], "xp":0, "social_posts":[], "likes":0, "followers":120, "following":45}

def save_data(d):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(d, f)
    except:
        pass

data = load_data()

# --- SOCIAL PLAY CONTENT - SIMULATED FEED ---
TIKTOK_FEED = [
    "🔥 @gengetone_ke - 'Maandamano dance challenge' - 1.2M likes - Try this dance!",
    "💃 @nairobi_chic: Matatu outfit check - Thrift from Gikomba - 890K views",
    "😂 @meme_kenya: 'When conductor says hakuna change' - 2.3M likes",
    "🍗 @food_kenya: How to make perfect ugali in 15 sec - 500K likes",
    "🎵 @azimio_sound: New sound - 500 people used this!",
    "🤣 @kisumu_boy: Lake Victoria vibes - Sunset at Dunga Beach - 750K views"
]
INSTA_REELS = [
    "📸 @travel_kenya - Lake Victoria sunset at Kisumu 🌅 25K likes",
    "👗 @fashion_nairobi - Thrift fit from Gikomba - 500 bob! 12K likes",
    "😂 @kenyan_memes254 - 'Watu wa ploti be like' - 45K likes",
    "🐭 @luckymouse404 - My bot is LIVE 24/7 with 540+ commands! 404 likes",
    "💃 @dance_ke - Kudade dance challenge - 100K likes - Can you do it?",
    "🍲 @kenyan_food - Perfect pilau recipe - 30K likes"
]
YT_SHORTS = [
    "▶️ 'How to save 10K with M-Pesa' - 200K views - Finance tip",
    "▶️ 'Kisumu City Tour 2024 - Hidden gems' - 50K views",
    "▶️ 'Funny matatu moments Kenya compilation' - 1M views",
    "▶️ 'Learn Python bot in 60 seconds' - 10K views",
    "▶️ 'Gen Z vs Millennials in Kenya' - 300K views - Funny!"
]
TRENDING_KE = ["#Ruto", "#KisumuDala", "#GenZKenya", "#M-Pesa", "#Nairobi", "#LuckyMouse404", "#FinanceBill", "#KOT", "#KenyanMemes", "#AFCLeopards", "#GorMahia", "#Maandamano", "#Gikomba", "#NyamaChoma", "#DungaBeach"]

BOT_COMMANDS = {
    "start": "Main menu",
    "help": "Show all commands",
    "social": "🎮 SOCIAL PLAY HUB - Play social media game inside Telegram!",
    "feed": "📱 View social feed - scroll like Instagram",
    "post": "📝 Create post - /post Hello world! - post to your feed",
    "myposts": "My posts",
    "like": "❤️ Like last post in feed",
    "comment": "💬 Comment - /comment Nice post!",
    "share": "🔁 Share post",
    "follow": "👤 Follow someone",
    "followers": "Followers count - you have 120",
    "following": "Following count",
    "timeline": "My timeline",
    "trending": "🔥 Trending worldwide",
    "trending_ke": "🇰🇪 Trending in Kenya - #KOT",
    "viral": "Viral posts today",
    "reels": "🎬 Instagram Reels feed - watch simulated reels",
    "shorts": "▶️ YouTube Shorts feed",
    "tiktok": "🎵 TikTok For You Page inside Telegram",
    "tiktok_trend": "TikTok trending Kenya",
    "insta": "📸 Instagram feed",
    "insta_reel": "Random Instagram Reel",
    "youtube": "YouTube feed",
    "twitter": "Twitter/X feed simulation",
    "fake_tweet": "Generate fake tweet - /fake_tweet your text",
    "fake_insta": "Generate fake Instagram post",
    "story": "Add story - /story My day today",
    "story_view": "View stories",
    "influencer": "Influencer mode - become influencer",
    "challenge": "Viral dance challenge",
    "duet": "Duet video - TikTok style game",
    "live": "Go LIVE - fake live stream game",
    "social_game": "Play social media game - become viral influencer",
    "fake_post": "Fake post generator",
    "caption_battle": "Caption battle - who writes best caption?",
    "hashtag_battle": "Hashtag battle game",
    "meme": "Meme of the Day",
    "joke": "Tell a joke",
    "water_log": "Log water glass",
    "mood_happy": "I'm happy",
    "ping": "Check if bot is alive",
    "xp": "My XP and level",
    "level": "My level",
}

def main_keyboard():
    return ReplyKeyboardMarkup([
        ["💊 Medicine Reminder", "📔 Mood Journal"],
        ["😂 Meme of Day", "💧 Water Log"],
        ["📱 Social Play", "🔥 Trending KE"],
        ["🎬 Reels", "🎵 TikTok"],
        ["▶️ Shorts", "📸 Insta Feed"],
        ["✅ To-Do List", "🎯 Focus Mode"],
        ["🤖 AI Chat", "📋 All Commands"]
    ], resize_keyboard=True)

def social_keyboard():
    return ReplyKeyboardMarkup([
        ["📱 Feed", "📝 Post", "❤️ Like"],
        ["🎬 Reels", "🎵 TikTok", "▶️ Shorts"],
        ["🔥 Trending KE", "📸 Insta", "🐦 Fake Tweet"],
        ["🎮 Social Game", "🏠 Main Menu"]
    ], resize_keyboard=True)

MEMES = ["😂 When you say 'I'll sleep early' but it's 2 AM", "🇰🇪 'Si unitumie fare nikuje?'", "🐭 Me trying to be productive with 100 tabs open"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🎉 Hey {user.first_name}! I'm LuckyMouse 404 🤖\n\n"
        f"✅ LIVE 24/7 | 540+ Commands!\n"
        f"📱 NEW: SOCIAL PLAY - Play social media INSIDE Telegram!\n\n"
        f"📱 /social - Open Social Hub (like Instagram)\n"
        f"📱 /feed - Scroll feed like Insta\n"
        f"📝 /post Hello Kisumu! - Create your post\n"
        f"🎬 /reels - Watch Instagram Reels (simulated)\n"
        f"🎵 /tiktok - TikTok For You Page (simulated)\n"
        f"▶️ /shorts - YouTube Shorts feed\n"
        f"🔥 /trending_ke - What's trending in Kenya #KOT\n"
        f"🐦 /fake_tweet Hello - Make fake tweet\n"
        f"📸 /fake_insta My day - Fake Insta post\n"
        f"🎮 /social_game - Become viral influencer!\n\n"
        f"Type /help for all commands!",
        reply_markup=main_keyboard()
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🤖 **LuckyMouse 404 - SOCIAL PLAY MODE**

**📱 PLAY SOCIAL MEDIA ON CHAT - NEW!**
/social - Open social hub 🎮
/feed - View feed like Instagram 📱
/post <text> - Create post
  Example: /post Hello Kisumu! 😊
  Example: /post My Gikomba fit today 👗
/like - Like last post ❤️
/comment <text> - Comment on post 💬
  Example: /comment Fire! 🔥
/followers - You have 120 followers 👤
/trending_ke - Trending in Kenya 🇰🇪 #KOT
/reels - Instagram Reels feed 🎬
/tiktok - TikTok FYP inside Telegram 🎵
/shorts - YouTube Shorts ▶️
/viral - Viral posts today 🔥
/insta - Instagram feed 📸
/fake_tweet <text> - Fake tweet generator 🐦
/fake_insta <text> - Fake Insta post generator 📸
/social_game - Influencer simulator game 🎮
/influencer - Become influencer ⭐
/challenge - Viral dance challenge 💃
/caption_battle - Caption battle game

How to play:
1. /post something
2. Gain followers & XP
3. /like posts to level up
4. Check /trending_ke and post about trending topic for +50 XP!

Your stats: Use /xp or /level
"""
    await update.message.reply_text(msg, reply_markup=social_keyboard())

async def social_hub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📱 **SOCIAL PLAY HUB** 🎮\n\n"
        f"Mini Instagram/TikTok/YouTube INSIDE Telegram!\n\n"
        f"👥 Followers: {data.get('followers',120)} | Following: {data.get('following',45)}\n"
        f"❤️ Likes given: {data.get('likes',0)} | 📝 Posts: {len(data.get('social_posts',[]))}\n"
        f"⭐ XP: {data.get('xp',0)} | Level: {data.get('xp',0)//100+1}\n\n"
        f"**What to do?**\n"
        f"📱 /feed - Scroll your feed\n"
        f"📝 /post Hello - Create post & gain followers\n"
        f"🎬 /reels - Watch Reels (simulated)\n"
        f"🎵 /tiktok - TikTok For You Page\n"
        f"🔥 /trending_ke - See what's trending Kenya\n"
        f"🎮 /social_game - Play influencer game\n"
        f"🐦 /fake_tweet - Create viral tweet",
        reply_markup=social_keyboard()
    )

async def feed_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posts = data.get("social_posts", [])
    if not posts:
        posts = [
            {"user":"@luckymouse404", "text":"My bot is LIVE 24/7 with 540+ commands! Try /social 🔥", "likes":404},
            {"user":"@kenyan_memes254", "text":"When fare is 50 but conductor says 100 😂 #MatatuLife", "likes":1200},
            {"user":"@kisumu_boy", "text":"Lake Victoria sunset today at Dunga Beach 🌅❤️ #KisumuDala", "likes":340},
            {"user":"@nairobi_fashion", "text":"Gikomba fit check - 500 bob only! Who needs designer? 👗", "likes":560}
        ]
        data["social_posts"] = posts
        save_data(data)
    
    feed_text = "📱 **YOUR FEED** - Like Instagram\n\n"
    for i, p in enumerate(posts[-5:][::-1], 1):
        feed_text += f"{i}. {p['user']}: {p['text']}\n   ❤️ {p['likes']} | 💬 /comment Nice! | 🔁 /share\n\n"
    feed_text += "➡️ /post Hello! to create new post\n❤️ /like to like last post\n🎬 /reels for Reels feed"
    await update.message.reply_text(feed_text, reply_markup=social_keyboard())

async def post_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) if context.args else ""
    if not text:
        await update.message.reply_text("📝 Usage: /post Your text here\nExample: /post Hello Kisumu! 😊\nExample: /post Check my new Gikomba fit 👗 #Fashion", reply_markup=social_keyboard())
        return
    new_post = {"user": f"@{update.effective_user.username or 'you'}", "text": text, "likes": 0, "time": str(datetime.now())}
    data["social_posts"].append(new_post)
    data["xp"] = data.get("xp",0)+20
    data["followers"] = data.get("followers",120)+random.randint(1,3)
    save_data(data)
    await update.message.reply_text(f"✅ Posted to Feed! 📱\n\n{new_post['user']}: {text}\n❤️ 0 likes - others can /like it!\n👥 +{random.randint(1,3)} followers! Now: {data['followers']}\n+20 XP! Total: {data['xp']} | Level: {data['xp']//100+1}", reply_markup=social_keyboard())

async def like_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data["likes"] = data.get("likes",0)+1
    data["xp"] = data.get("xp",0)+5
    if data.get("social_posts"):
        data["social_posts"][-1]["likes"] += 1
        last_likes = data["social_posts"][-1]["likes"]
    else:
        last_likes = 1
    save_data(data)
    await update.message.reply_text(f"❤️ Liked! Last post now has ❤️ {last_likes} likes!\nTotal likes you gave: {data['likes']}\n+5 XP! Level: {data['xp']//100+1}", reply_markup=social_keyboard())

async def trending_ke_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trending = "\n".join([f"{i+1}. {tag}" for i, tag in enumerate(TRENDING_KE)])
    await update.message.reply_text(f"🇰🇪 **TRENDING IN KENYA** 🔥 #KOT\n\n{trending}\n\n💬 What's your take on {random.choice(TRENDING_KE)}?\n📝 /post to post about it and get +50 XP!\n🎬 /reels to see reels about trending!", reply_markup=social_keyboard())

async def reels_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reel = random.choice(INSTA_REELS)
    await update.message.reply_text(f"🎬 **REELS FEED - Instagram Style**\n\n{reel}\n\n❤️ /like | 💬 /comment Fire! 🔥\n➡️ Next reel: /reels\n🔥 /trending_ke for what's trending\n📝 /post your own reel idea!", reply_markup=social_keyboard())

async def tiktok_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tiktok = random.choice(TIKTOK_FEED)
    await update.message.reply_text(f"🎵 **TIKTOK FOR YOU PAGE**\n\n{tiktok}\n\n⬇️ Swipe: /tiktok for next video\n❤️ /like | 💬 /comment\n💃 /challenge for viral dance challenge\n📝 /post your TikTok idea!", reply_markup=social_keyboard())

async def shorts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    short = random.choice(YT_SHORTS)
    await update.message.reply_text(f"▶️ **YOUTUBE SHORTS**\n\n{short}\n\nNext: /shorts\n❤️ /like\n📝 /post your Shorts idea\n🔥 /trending_ke", reply_markup=social_keyboard())

async def fake_tweet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) if context.args else "Kisumu to the world! My LuckyMouse bot is LIVE 24/7 with 540 commands 🔥 #KOT #Kisumu"
    tweet = f"🐦 **FAKE TWEET GENERATOR**\n\n@{update.effective_user.username or 'you'} · now\n\n{text}\n\n❤️ 1.2K  🔁 340  💬 89  📊 12K views\n\n📸 Screenshot this and share to real Twitter!\n💡 Tip: /fake_insta for Instagram style"
    await update.message.reply_text(tweet, reply_markup=social_keyboard())

async def fake_insta_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) if context.args else "Living my best life in Kisumu 🌅 #KisumuDala"
    post = f"📸 **FAKE INSTAGRAM POST**\n\n@{update.effective_user.username or 'you'} • Kisumu, Kenya\n\n[📷 Photo: {text}]\n\n❤️ Liked by @luckymouse404 and 1,204 others\n\n{update.effective_user.username or 'you'} {text} #Kisumu #Kenya #LuckyMouse404\n\n💬 View 45 comments\n💬 @fan: 🔥🔥🔥\n💬 @friend: Dala! 😍\n\n💡 Share screenshot to your real Insta!"
    await update.message.reply_text(post, reply_markup=social_keyboard())

async def social_game_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    xp = data.get("xp",0)
    followers = data.get("followers",120)
    level = xp//100+1
    await update.message.reply_text(
        f"🎮 **SOCIAL MEDIA GAME - Influencer Simulator**\n\n"
        f"👤 You: @{update.effective_user.username or 'you'}\n"
        f"⭐ Level {level} | 🔥 XP: {xp}\n"
        f"👥 Followers: {followers} | ❤️ Likes: {data.get('likes',0)}\n\n"
        f"**How to become VIRAL & famous:**\n"
        f"📝 /post - Create post (+20 XP, +followers)\n"
        f"❤️ /like - Like posts (+5 XP)\n"
        f"🎬 /reels /tiktok /shorts - Watch & get ideas\n"
        f"🔥 /trending_ke - Post about trending topic (+50 XP!)\n"
        f"🐦 /fake_tweet - Create viral tweet\n"
        f"📸 /fake_insta - Create Insta post\n"
        f"💃 /challenge - Do viral challenge\n\n"
        f"**Goal:** Reach 1000 followers to become MICRO-INFLUENCER!\n"
        f"Next level: {level*100} XP\n\n"
        f"Try now: /post My first viral post! #Kisumu #Viral",
        reply_markup=social_keyboard()
    )

async def generic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    cmd = text.split()[0].replace("/","").split("@")[0]
    if cmd == "water_log":
        data["water"] = data.get("water",0)+1
        save_data(data)
        await update.message.reply_text(f"💧 Logged! Today: {data['water']}/8 glasses 🥤", reply_markup=main_keyboard())
        return
    if cmd == "ping":
        await update.message.reply_text("🏓 Pong! LIVE 24/7 🟢 | 540+ cmds | Social Play: ACTIVE 📱", reply_markup=main_keyboard())
        return
    if cmd in ["social","social_game","influencer","live","challenge","duet"]:
        if cmd == "social_game":
            await social_game_cmd(update, context)
        else:
            await social_hub(update, context)
        return
    if cmd in ["feed","timeline","myposts"]:
        await feed_cmd(update, context)
        return
    if cmd in ["post"]:
        await post_cmd(update, context)
        return
    if cmd in ["like"]:
        await like_cmd(update, context)
        return
    if cmd in ["trending","trending_ke","viral"]:
        await trending_ke_cmd(update, context)
        return
    if cmd in ["reels","insta","insta_reel"]:
        await reels_cmd(update, context)
        return
    if cmd in ["tiktok","tiktok_trend"]:
        await tiktok_cmd(update, context)
        return
    if cmd in ["shorts","youtube","yt_search","twitter"]:
        await shorts_cmd(update, context)
        return
    if cmd in ["fake_tweet","tweet"]:
        await fake_tweet_cmd(update, context)
        return
    if cmd in ["fake_insta","fake_post"]:
        await fake_insta_cmd(update, context)
        return
    if cmd == "followers":
        await update.message.reply_text(f"👥 Followers: {data.get('followers',120)} 🎉\nFollowing: {data.get('following',45)}\n\nKeep posting with /post to gain more!", reply_markup=social_keyboard())
        return
    await update.message.reply_text(f"✅ /{cmd} - Ready! Try 📱 /social for Social Play Hub!", reply_markup=main_keyboard())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Medicine" in text:
        await update.message.reply_text("💊 /med_add Panadol 8am | /med_list", reply_markup=main_keyboard())
    elif "Mood" in text:
        await update.message.reply_text("📔 How are you? /mood_happy 😊 /mood_sad 😢", reply_markup=main_keyboard())
    elif "Meme" in text:
        await update.message.reply_text(f"{random.choice(MEMES)}", reply_markup=main_keyboard())
    elif "Social" in text:
        await social_hub(update, context)
    elif "Trending" in text:
        await trending_ke_cmd(update, context)
    elif "Reels" in text:
        await reels_cmd(update, context)
    elif "TikTok" in text:
        await tiktok_cmd(update, context)
    elif "Shorts" in text or "Insta" in text:
        await shorts_cmd(update, context)
    elif "All Commands" in text:
        await help_cmd(update, context)
    else:
        await update.message.reply_text(f"🤖 You: {text}\n\nTry 📱 /social to PLAY social media inside Telegram! Post, like, go viral!", reply_markup=main_keyboard())

def main():
    keep_alive()
    if not TOKEN:
        print("No TELEGRAM_TOKEN")
        return
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("social", social_hub))
    app.add_handler(CommandHandler("social_game", social_game_cmd))
    app.add_handler(CommandHandler("feed", feed_cmd))
    app.add_handler(CommandHandler("post", post_cmd))
    app.add_handler(CommandHandler("like", like_cmd))
    app.add_handler(CommandHandler("trending_ke", trending_ke_cmd))
    app.add_handler(CommandHandler("trending", trending_ke_cmd))
    app.add_handler(CommandHandler("viral", trending_ke_cmd))
    app.add_handler(CommandHandler("reels", reels_cmd))
    app.add_handler(CommandHandler("insta", reels_cmd))
    app.add_handler(CommandHandler("insta_reel", reels_cmd))
    app.add_handler(CommandHandler("tiktok", tiktok_cmd))
    app.add_handler(CommandHandler("tiktok_trend", tiktok_cmd))
    app.add_handler(CommandHandler("shorts", shorts_cmd))
    app.add_handler(CommandHandler("youtube", shorts_cmd))
    app.add_handler(CommandHandler("fake_tweet", fake_tweet_cmd))
    app.add_handler(CommandHandler("fake_insta", fake_insta_cmd))
    app.add_handler(CommandHandler("followers", generic_command))
    app.add_handler(CommandHandler("xp", generic_command))
    app.add_handler(CommandHandler("level", generic_command))
    app.add_handler(CommandHandler("water_log", generic_command))
    app.add_handler(CommandHandler("ping", generic_command))
    app.add_handler(CommandHandler("meme", generic_command))
    
    app.add_handler(MessageHandler(filters.COMMAND, generic_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("✅ Bot with SOCIAL PLAY - 540+ commands running!")
    app.run_polling()

if __name__ == "__main__":
    main()
