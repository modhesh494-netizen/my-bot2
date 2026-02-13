import telebot
import time
from threading import Thread

# حط التوكن بتاعك هنا من BotFather
TOKEN = '8445157524:AAF8oTwxP9MLk6hf4h5YzghwvREjCreSuy4'
bot = telebot.TeleBot(TOKEN)

# قائمة الجروبات اللي ضافوا البوت
chats = set()

@bot.message_handler(commands=['start'])
def start(message):
    chats.add(message.chat.id)
    bot.reply_to(message, "تم تفعيل البوت بنجاح. هفكركم بالصلاة على النبي كل دقيقة.")

def remind_users():
    while True:
        # الرسالة اللي طلبتها
        message_text = "صلي علي النبي ﷺ مش شرط تكتب صلي ف سرك"
        
        for chat_id in list(chats):
            try:
                bot.send_message(chat_id, message_text)
            except Exception as e:
                print(f"فشل الإرسال لـ {chat_id}: {e}")
        
        # الانتظار لمدة 60 ثانية (دقيقة)
        time.sleep(60)

# تشغيل وظيفة التذكير في Background عشان البوت ميهنجش
reminder_thread = Thread(target=remind_users)
reminder_thread.daemon = True
reminder_thread.start()

print("البوت يعمل الآن...")
bot.infinity_polling()
