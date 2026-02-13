import telebot
import time
from threading import Thread

# --- الإعدادات الأساسية ---
TOKEN = '8445157524:AAF8oTwxP9MLk6hf4h5YzghwvREjCreSuy4'
ADMIN_ID = 123456789  # 👈 ضع ID حسابك الحقيقي هنا
bot = telebot.TeleBot(TOKEN)

# تخزين البيانات {chat_id: {interval: seconds, last_sent: timestamp}}
active_chats = {}

# --- لوحة التحكم (للمالك فقط) ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📊 الإحصائيات", "📢 إذاعة رسالة")
        bot.reply_to(message, "🛠 **لوحة تحكم المالك**", reply_markup=markup)
    else:
        bot.reply_to(message, "❌ هذا الأمر مخصص للمالك فقط.")

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and message.text in ["📊 الإحصائيات", "📢 إذاعة رسالة"])
def handle_admin(message):
    if message.text == "📊 الإحصائيات":
        bot.reply_to(message, f"👥 عدد الشاتات النشطة: {len(active_chats)}")
    elif message.text == "📢 إذاعة رسالة":
        msg = bot.send_message(message.chat.id, "💬 أرسل نص الإذاعة الآن:")
        bot.register_next_step_handler(msg, perform_broadcast)

def perform_broadcast(message):
    count = 0
    for chat_id in list(active_chats.keys()):
        try:
            bot.send_message(chat_id, f"📢 **تنبيه عام:**\n\n{message.text}")
            count += 1
        except: pass
    bot.reply_to(message, f"✅ تم الإرسال إلى {count} شات.")

# --- أمر التشغيل الأساسي ---
@bot.message_handler(commands=['start'])
def start(message):
    # الرسالة المطلوبة تماماً
    msg = bot.reply_to(message, "قم بتحديد وقت ارسال الرسائل ( الحد الادني 1 دقيقه و الاقصي 3 ساعات)")
    bot.register_next_step_handler(msg, set_timer)

def set_timer(message):
    try:
        minutes = int(message.text)
        
        # التحقق من الحد الأدنى والحد الأقصى (3 ساعات = 180 دقيقة)
        if minutes < 1:
            bot.reply_to(message, "⚠️ خطأ: الحد الأدنى هو 1 دقيقة. أرسل /start للمحاولة مرة أخرى.")
            return
        if minutes > 180:
            bot.reply_to(message, "⚠️ خطأ: الحد الأقصى هو 3 ساعات (180 دقيقة). أرسل /start للمحاولة مرة أخرى.")
            return
        
        active_chats[message.chat.id] = {
            'interval': minutes * 60,
            'last_sent': time.time()
        }
        bot.reply_to(message, f"✅ تم تحديد الوقت بنجاح كل {minutes} دقيقة ﷺ.\nلإيقاف التذكير أرسل /stop")
        
    except ValueError:
        bot.reply_to(message, "❌ يرجى إرسال أرقام فقط. أرسل /start للمحاولة.")

# --- أمر الإيقاف ---
@bot.message_handler(commands=['stop'])
def stop(message):
    if message.chat.id in active_chats:
        del active_chats[message.chat.id]
        bot.reply_to(message, "🛑 تم إيقاف التذكير بنجاح.")
    else:
        bot.reply_to(message, "البوت غير مفعل لديك.")

# --- منطق التذكير ---
def remind_logic():
    while True:
        current_time = time.time()
        for chat_id in list(active_chats.keys()):
            data = active_chats[chat_id]
            if current_time - data['last_sent'] >= data['interval']:
                try:
                    bot.send_message(chat_id, "صلي علي النبي ﷺ مش شرط تكتب صلي ف سرك")
                    active_chats[chat_id]['last_sent'] = current_time
                except:
                    if chat_id in active_chats: del active_chats[chat_id]
        time.sleep(10)

Thread(target=remind_logic, daemon=True).start()

print("البوت شغال...")
bot.infinity_polling()
