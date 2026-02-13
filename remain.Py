import telebot
import time
from threading import Thread

# التوكن بتاعك اللي شغال
TOKEN = '8445157524:AAF8oTwxP9MLk6hf4h5YzghwvREjCreSuy4'
bot = telebot.TeleBot(TOKEN)

# قائمة الجروبات اللي ضافوا البوت
chats = set()
running = True # متغير للتحكم في تشغيل التذكير

@bot.message_handler(commands=['start'])
def start(message):
    global running
    running = True
    chats.add(message.chat.id)
    bot.reply_to(message, "تم تفعيل البوت بنجاح. هفكركم بالصلاة على النبي كل 3 دقائق ﷺ")

@bot.message_handler(commands=['stop'])
def stop(message):
    global running
    running = False
    bot.reply_to(message, "تم إيقاف التذكير مؤقتاً. لو عايز تشغله تاني ابعت /start")

def remind_users():
    while True:
        if running and chats:
            message_text = "صلي علي النبي ﷺ مش شرط تكتب صلي ف سرك"
            for chat_id in list(chats):
                try:
                    bot.send_message(chat_id, message_text)
                except Exception as e:
                    print(f"فشل الإرسال لـ {chat_id}: {e}")
            
            # الانتظار لمدة 180 ثانية (3 دقائق)
            time.sleep(180) 
        else:
            # لو التذكير واقف، يشيك كل ثانية عشان ميهنجش
            time.sleep(1)

# تشغيل التذكير في الخلفية
reminder_thread = Thread(target=remind_users)
reminder_thread.daemon = True
reminder_thread.start()

print("البوت يعمل الآن...")
bot.infinity_polling()
