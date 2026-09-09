import os
import requests
import telebot

# BotFather থেকে পাওয়া টোকেন
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(TOKEN)

# লাইক দেওয়ার মূল কমান্ড /like <UID>
@bot.message_handler(commands=['like'])
def handle_like(message):
    try:
        # ইউজার মেসেজ থেকে UID আলাদা করা (যেমন: /like 1399637672)
        command_args = message.text.split()
        
        if len(command_args) < 2:
            bot.reply_to(message, "⚠️ **সঠিক নিয়ম:** `/like <UID>`\nযেমন: `/like 12345678`", parse_mode="Markdown")
            return

        uid = command_args[1]

        # প্রসেসিং মেসেজ
        processing_msg = bot.reply_to(message, f"⏳ **UID:** `{uid}`-এর জন্য প্রসেসিং করা হচ্ছে...", parse_mode="Markdown")

        # Free Fire Like API URL (আপনার কার্যকর API লিংকটি বসাবেন)
        api_url = f"https://free-fire-like-api.example.com/api?uid={uid}"
        
        # API রিকোয়েস্ট পাঠানো
        response = requests.get(api_url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # API রেসপন্স থেকে তথ্য নেয়া
            nickname = data.get('nickname', 'Unknown')
            likes_added = data.get('likes_added', '0')
            before_likes = data.get('before_likes', 'N/A')
            current_likes = data.get('current_likes', 'N/A')

            # মেম্বারদের জন্য সুন্দর রেসপন্স টেক্সট
            response_text = f"""
🎮 **Auto Like Success** 🎮
──────────────────────
👤 **Nickname:** `{nickname}`
🆔 **UID:** `{uid}`

🚀 **Likes Added:** `{likes_added}`
📈 **Before Likes:** `{before_likes}`
✅ **Current Likes:** `{current_likes}`
──────────────────────
🤖 **Bot Status:** Active
            """
            bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ **API সমস্যা:** গেম সার্ভার বা API থেকে রেসপন্স পাওয়া যায়নি।", chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, "❌ **ত্রুটি:** অনুগ্রহ করে সঠিক UID দিন অথবা কিছুক্ষণ পর চেষ্টা করুন।")

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
👋 **স্বাগতম!**
Free Fire অটো লাইক নিতে নিচের নিয়ম অনুসরণ করুন:

📌 **কমান্ড:** `/like <আপনার_UID>`
💡 **উদাহরণ:** `/like 12345678`
    """
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# বট রান করা
bot.infinity_polling()
