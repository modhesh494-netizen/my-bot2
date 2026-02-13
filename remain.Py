import telebot
import time
from threading import Thread

# التوكن بتاعك
TOKEN = '8445157524:AAF8oTwxP9MLk6hf4h5YzghwvREjCreSuy4'
bot = telebot.TeleBot(TOKEN)

# الإعدادات
chats = set()
is_running = True  # متغير للتحكم في الإيقاف والتشغيل

@bot.message_handler(commands=['start'])
def start(message):
    global is_running
    is_running = True
    chats.add(message.chat.id)
    bot.reply_to(message, "✅ تم التفعيل! هفكركم بالصلاة على النبي كل 3 دقائق ﷺ. لو عايز توقف ابعت /stop")

@bot.message_handler(commands=['stop'])
def stop(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 تم إيقاف التذكير. ابعت /start عشان تشغله تاني.")

def remind_logic():
    while True:
        if is_running and len(chats) > 0:
            for chat_id in list(chats):
                try:
                    bot.send_message(chat_id, "صلي علي النبي ﷺ مش شرط تكتب صلي ف سرك")
                except:
                    pass
            time.sleep(180) # الانتظار 3 دقائق (180 ثانية)
        else:
            time.sleep(5) # لو واقف يشيك كل 5 ثواني عشان ميهنجش

# تشغيل التذكير في الخلفية
Thread(target=remind_logic, daemon=True).start()

print("البوت شغال...")
bot.infinity_polling()
