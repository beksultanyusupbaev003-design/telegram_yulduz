import os
import json
import asyncio
import datetime
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

TOKEN = os.environ.get("BOT_TOKEN", "8997822170:AAFXIeBOwH3l8Vx2aWke1v4L03LF4FDFhvQ")
USERS_FILE = "users.json"

# Conversation states
ASK_NAME, ASK_DATE, ASK_SIGN = range(3)

# Burjlar
ZODIAC_SIGNS = [
    "♈ Qo'y (Aries)", "♉ Buqa (Taurus)", "♊ Egizaklar (Gemini)",
    "♋ Qisqichbaqa (Cancer)", "♌ Arslon (Leo)", "♍ Boshoq (Virgo)",
    "♎ Tarozi (Libra)", "♏ Chayon (Scorpio)", "♐ Yoy (Sagittarius)",
    "♑ Tog' echkisi (Capricorn)", "♒ Qovg'a (Aquarius)", "♓ Baliq (Pisces)"
]

# Sanaga qarab burj aniqlash
def get_zodiac_by_date(day, month):
    if (month == 3 and day >= 21) or (month == 4 and day <= 19): return "♈ Qo'y (Aries)"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20): return "♉ Buqa (Taurus)"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20): return "♊ Egizaklar (Gemini)"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22): return "♋ Qisqichbaqa (Cancer)"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22): return "♌ Arslon (Leo)"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22): return "♍ Boshoq (Virgo)"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22): return "♎ Tarozi (Libra)"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21): return "♏ Chayon (Scorpio)"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21): return "♐ Yoy (Sagittarius)"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19): return "♑ Tog' echkisi (Capricorn)"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18): return "♒ Qovg'a (Aquarius)"
    else: return "♓ Baliq (Pisces)"

# Yil burji (Xitoy taqvimi)
def get_chinese_zodiac(year):
    animals = ["🐀 Sichqon", "🐂 Ho'kiz", "🐅 Yo'lbars", "🐇 Quyon",
               "🐉 Ajdaho", "🐍 Ilon", "🐎 Ot", "🐏 Qo'y",
               "🐒 Maymun", "🐓 Xo'roz", "🐕 It", "🐖 Cho'chqa"]
    return animals[(year - 4) % 12]

# Hafta kunlari
def get_day_name():
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    return days[datetime.datetime.now().weekday()]

# Bashorat generatsiya qilish
def generate_horoscope(name, zodiac, chinese_zodiac, day_name):
    today = datetime.datetime.now()

    love_messages = [
        "Bugun muhabbat hayotingizda yangi sahifa ochadi. Yaqinlaringizga e'tibor bering.",
        "Sevgiliningiz bilan samimiy suhbat bugun munosabatlarni mustahkamlaydi.",
        "Bugun yangi tanishuvlar sizga kutilmagan quvonch keltirishi mumkin.",
        "Oilaviy munosabatlar bugun alohida e'tibor talab qiladi.",
        "Bugun ko'ngilingiz bo'sh bo'lsa, eski do'stingizga qo'ng'iroq qiling.",
    ]

    money_messages = [
        "Moliyaviy jihatdan bugun ehtiyotkor bo'ling, katta xarajatlardan saqlaning.",
        "Bugun kutilmagan daromad manbayi paydo bo'lishi mumkin.",
        "Investitsiya va biznes qarorlarini bir necha kun kechiktiring.",
        "Bugun mehnatga yarasha mukofot olasiz.",
        "Tejamkorlik bugun sizning eng yaxshi do'stingiz.",
    ]

    health_messages = [
        "Bugun jismoniy faollikka e'tibor bering, biroz yuring.",
        "Dam olishni unutmang, sog'lig'ingiz bugun biroz nozik.",
        "Bugun energiyangiz yuqori — ishlarni amalga oshiring!",
        "Ovqatlanishga e'tibor bering, suv ko'proq iching.",
        "Bugun meditatsiya yoki nafas mashqlari foydali bo'ladi.",
    ]

    work_messages = [
        "Bugun ijodiy g'oyalaringiz atrofdagilarni hayratga soladi.",
        "Hamkorlar bilan muloqotda sabr-toqat ko'rsating.",
        "Yangi loyihaga kirishishga bugun qulay kun.",
        "Rahbariyat bugun sizning mehnatinggizni sezadi.",
        "Bugun muhim qaror qabul qilishdan oldin yaxshilab o'ylang.",
    ]

    lucky_numbers = random.sample(range(1, 50), 3)
    lucky_color_list = ["🔴 Qizil", "🔵 Ko'k", "🟢 Yashil", "🟡 Sariq", "🟣 Binafsha", "🟠 To'q sariq", "⚪ Oq"]
    lucky_color = random.choice(lucky_color_list)

    seed = today.strftime("%Y%m%d") + name + zodiac
    random.seed(hash(seed))

    love = random.choice(love_messages)
    money = random.choice(money_messages)
    health = random.choice(health_messages)
    work = random.choice(work_messages)

    random.seed()

    stars = random.randint(3, 5)
    star_str = "⭐" * stars

    horoscope = f"""
🌟 *Assalomu alaykum, {name}!*
📅 *{day_name}, {today.strftime('%d.%m.%Y')}*

{zodiac}
{chinese_zodiac} yilida tug'ilgansiz

━━━━━━━━━━━━━━━
✨ *Bugungi bashorat*
━━━━━━━━━━━━━━━

💕 *Muhabbat:*
{love}

💰 *Moliya:*
{money}

💪 *Sog'liq:*
{health}

💼 *Ish/O'qish:*
{work}

━━━━━━━━━━━━━━━
🍀 *Omad raqamlar:* {', '.join(map(str, lucky_numbers))}
🎨 *Omad rangi:* {lucky_color}
⭐ *Bugungi yulduz:* {star_str}
━━━━━━━━━━━━━━━

_Bugun ajoyib kun bo'lsin! 🌈_
"""
    return horoscope

# Foydalanuvchilarni yuklash/saqlash
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    user_id = str(update.effective_user.id)

    if user_id in users:
        user = users[user_id]
        horoscope = generate_horoscope(
            user["name"], user["zodiac"],
            user["chinese_zodiac"], get_day_name()
        )
        await update.message.reply_text(
            f"Qaytib keldingiz! 🌟\n{horoscope}",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "🌟 *Yulduzlar Bashorati Botiga Xush Kelibsiz!* 🌟\n\n"
        "Men sizga har kuni shaxsiy bashorat yuborib turaman.\n\n"
        "Avval tanishib olaylik! 😊\n\n"
        "*Ismingizni kiriting:*",
        parse_mode="Markdown"
    )
    return ASK_NAME

# Ism olish
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text.strip()
    await update.message.reply_text(
        f"Juda chiroyli ism! 😊\n\n"
        f"*{context.user_data['name']}*, tug'ilgan sanangizni kiriting:\n\n"
        f"📅 Format: *KK.OO.YYYY*\n"
        f"Masalan: *15.03.1995*",
        parse_mode="Markdown"
    )
    return ASK_DATE

# Sana olish
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        parts = text.split(".")
        if len(parts) != 3:
            raise ValueError
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2010):
            raise ValueError

        context.user_data["birthday"] = text
        context.user_data["day"] = day
        context.user_data["month"] = month
        context.user_data["year"] = year

        auto_zodiac = get_zodiac_by_date(day, month)
        chinese = get_chinese_zodiac(year)

        context.user_data["auto_zodiac"] = auto_zodiac
        context.user_data["chinese_zodiac"] = chinese

        keyboard = [[sign] for sign in ZODIAC_SIGNS]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        await update.message.reply_text(
            f"✨ Sanangizga ko'ra burjingiz: *{auto_zodiac}*\n"
            f"🐉 Xitoy burjingiz: *{chinese}*\n\n"
            f"Burjingizni tasdiqlang yoki o'zgartiring:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return ASK_SIGN

    except (ValueError, IndexError):
        await update.message.reply_text(
            "❌ Format noto'g'ri!\n\n"
            "Iltimos shu formatda yuboring:\n"
            "*KK.OO.YYYY*\nMasalan: *15.03.1995*",
            parse_mode="Markdown"
        )
        return ASK_DATE

# Burj olish
async def get_sign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    zodiac = update.message.text.strip()

    if zodiac not in ZODIAC_SIGNS:
        zodiac = context.user_data.get("auto_zodiac", ZODIAC_SIGNS[0])

    users = load_users()
    user_id = str(update.effective_user.id)
    users[user_id] = {
        "name": context.user_data["name"],
        "birthday": context.user_data["birthday"],
        "zodiac": zodiac,
        "chinese_zodiac": context.user_data["chinese_zodiac"],
        "telegram_id": update.effective_user.id,
        "registered": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    save_users(users)

    horoscope = generate_horoscope(
        context.user_data["name"], zodiac,
        context.user_data["chinese_zodiac"], get_day_name()
    )

    await update.message.reply_text(
        f"✅ Ro'yxatdan o'tdingiz!\n\nMana bugungi bashoratIngiz:{horoscope}",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# /bashorat komandasi
async def bashorat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    user_id = str(update.effective_user.id)

    if user_id not in users:
        await update.message.reply_text(
            "Siz hali ro'yxatdan o'tmagansiz!\n/start buyrug'ini yuboring."
        )
        return

    user = users[user_id]
    horoscope = generate_horoscope(
        user["name"], user["zodiac"],
        user["chinese_zodiac"], get_day_name()
    )
    await update.message.reply_text(horoscope, parse_mode="Markdown")

# Har kuni ertalab 08:00 da bashorat yuborish
async def send_daily_horoscope(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    day_name = get_day_name()

    for user_id, user in users.items():
        try:
            horoscope = generate_horoscope(
                user["name"], user["zodiac"],
                user["chinese_zodiac"], day_name
            )
            await context.bot.send_message(
                chat_id=int(user_id),
                text=f"🌅 *Ertalabki bashorat!*\n{horoscope}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Xatolik {user_id}: {e}")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 *Bot buyruqlari:*\n\n"
        "/start — Botni boshlash\n"
        "/bashorat — Bugungi bashoratni ko'rish\n"
        "/help — Yordam\n\n"
        "Har kuni ertalab soat 08:00 da avtomatik bashorat keladi! ✨",
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            ASK_SIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sign)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("bashorat", bashorat))
    app.add_handler(CommandHandler("help", help_command))

    # Har kuni soat 08:00 da yuborish
    app.job_queue.run_daily(
        send_daily_horoscope,
        time=datetime.time(hour=8, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=5)))
    )

    print("Bot ishga tushdi! ✅")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
