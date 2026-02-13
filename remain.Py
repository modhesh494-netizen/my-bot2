import telebot
import time
import json
import os
from threading import Thread
from telebot.apihelper import ApiTelegramException

# --- الإعدادات ---
TOKEN = '8445157524:AAF8oTwxP9MLk6hf4h5YzghwvREjCreSuy4'
ADMIN_ID = 5971999624  # 👈 تم تحديث المعرف الخاص بك هنا
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'database.json'

# دالة لتحميل البيانات من ملف
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

# دالة لحفظ البيانات
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(active_chats, f)

active_chats = load_data()

# --- لوحة التحكم ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📊 الإحصائيات", "📢 إذاعة رسالة")
        bot.reply_to(message, "🛠 **أهلاً يا مالك البوت.. لوحة التحكم جاهزة:**", reply_markup=markup)
    else:
        bot.reply_to(message, "❌ هذا الأمر للمالك فقط.")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text == "📊 الإحصائيات")
def stats(message):
    bot.reply_to(message, f"👥 عدد الشاتات النشطة حالياً: {len(active_chats)}")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text == "📢 إذاعة رسالة")
def broadcast_prompt(message):
    msg = bot.send_message(message.chat.id, "💬 أرسل الرسالة التي تريد إذاعتها للجميع:")
    bot.register_next_step_handler(msg, perform_broadcast)

def perform_broadcast(message):
    count = 0
    for chat_id in list(active_chats.keys()):
        try:
            bot.send_message(chat_id, f"📢 **رسالة من الإدارة:**\n\n{message.text}")
            count += 1
            time.sleep(0.2)
        except:
            pass
    bot.reply_to(message, f"✅ تمت الإذاعة بنجاح لـ {count} مستخدم/جروب.")

# --- الأوامر الأساسية ---
@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.reply_to(message, "قم بتحديد وقت ارسال الرسائل ( الحد الادني 1 دقيقه و الاقصي 3 ساعات)")
    bot.register_next_step_handler(msg, set_timer)

def set_timer(message):
    try:
        minutes = int(message.text)
        if 1 <= minutes <= 180:
            active_chats[str(message.chat.id)] = {'interval': minutes * 60, 'last_sent': time.time()}
            save_data()
            bot.reply_to(message, f"✅ تم الضبط بنجاح! سأقوم بالتذكير كل {minutes} دقيقة ﷺ.")
        else:
            bot.reply_to(message, "⚠️ خطأ: يجب أن يكون الوقت بين 1 و 180 دقيقة.")
    except:
        bot.reply_to(message, "❌ يرجى إرسال أرقام فقط (مثلاً: 5).")

@bot.message_handler(commands=['stop'])
def stop(message):
    if str(message.chat.id) in active_chats:
        del active_chats[str(message.chat.id)]
        save_data()
        bot.reply_to(message, "🛑 تم إيقاف التذكير.")
    else:
        bot.reply_to(message, "البوت غير مفعل هنا.")

# --- منطق التذكير المستقر ---
def remind_logic():
    while True:
        current_time = time.time()
        for chat_id, data in list(active_chats.items()):
            if current_time - data['last_sent'] >= data['interval']:
                try:
                    bot.send_message(chat_id, "صلي علي النبي ﷺ مش شرط تكتب صلي ف سرك")
                    active_chats[chat_id]['last_sent'] = current_time
                    save_data()
                except ApiTelegramException as e:
                    if e.error_code in [403, 400]:
                        if chat_id in active_chats:
                            del active_chats[chat_id]
                            save_data()
                except:
                    pass
        time.sleep(15)

Thread(target=remind_logic, daemon=True).start()

# تشغيل البوت مع نظام حماية من التوقف
print("البوت يعمل الآن...")
while True:
    try:
        bot.polling(none_stop=True, interval=2, timeout=20)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
