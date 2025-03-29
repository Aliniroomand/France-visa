from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "7594464776:AAHhGmXAMKpOF7jpQIHXsjNFFPNrcbFXDaQ"
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/d/d6/Visa_2021.svg"  # لینک عکس لوگو

async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("💼 اطلاعات ویزا", callback_data='visa_info')],
                [InlineKeyboardButton("🌐 وبسایت ما", url="https://example.com")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """
    *سلام!* 😊
    _به بات ویزای فرانسه خوش آمدید._
    `برای شروع اطلاعات خود را وارد کنید.`
    """
    
    await update.message.reply_photo(photo=LOGO_URL, caption=text, parse_mode="MarkdownV2", reply_markup=reply_markup)

async def receive_info(update: Update, context):
    user_input = update.message.text
    response_text = f"<b>اطلاعات شما دریافت شد:</b> <br><i>{user_input}</i>"
    
    await update.message.reply_text(response_text, parse_mode="HTML")

async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "visa_info":
        await query.message.reply_text("🔍 اطلاعات مربوط به ویزای فرانسه:", parse_mode="MarkdownV2")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_info))
    
    print("✅ بات فعال شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
