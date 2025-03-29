from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

TOKEN = "7594464776:AAHhGmXAMKpOF7jpQIHXsjNFFPNrcbFXDaQ"

# مراحل دریافت اطلاعات
AGE, EDUCATION, INSURANCE, MARITAL = range(4)

# ذخیره اطلاعات کاربران
user_data = {}

async def start(update: Update, context):
    await update.message.reply_text("سلام! لطفاً سن خود را وارد کنید:")
    return AGE

async def age(update: Update, context):
    user_data["age"] = int(update.message.text)
    reply_keyboard = [["دیپلم", "کارشناسی", "کارشناسی ارشد", "دکترا"]]
    await update.message.reply_text(
        "میزان تحصیلات خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return EDUCATION

async def education(update: Update, context):
    user_data["education"] = update.message.text
    await update.message.reply_text("چند سال سابقه بیمه دارید؟")
    return INSURANCE

async def insurance(update: Update, context):
    user_data["insurance"] = int(update.message.text)
    reply_keyboard = [["مجرد", "متاهل"]]
    await update.message.reply_text(
        "وضعیت تأهل خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return MARITAL

async def marital(update: Update, context):
    user_data["marital"] = update.message.text
    score = calculate_visa_chance(user_data)
    await update.message.reply_text(f"شانس دریافت ویزای شما: {score}%")
    return ConversationHandler.END

def calculate_visa_chance(data):
    score = 50
    if 25 <= data["age"] <= 40:
        score += 10
    elif data["age"] < 25 or data["age"] > 50:
        score -= 10
    if data["education"] in ["کارشناسی ارشد", "دکترا"]:
        score += 15
    if data["insurance"] >= 5:
        score += 10
    if data["marital"] == "متاهل":
        score += 5
    return min(score, 100)

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, education)],
            INSURANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, insurance)],
            MARITAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, marital)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("بات فعال شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
