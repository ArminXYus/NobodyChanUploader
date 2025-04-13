import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# فرمان /start
async def start(update: Update, context: CallbackContext):
    # ارسال پیامی به ادمین بعد از شروع ربات
    await update.message.reply_text("سلام! لطفاً فایل خود را ارسال کنید.")

# فرمان برای دریافت فایل
async def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_id = file.file_id
    file_name = file.file_name

    # دانلود فایل از تلگرام
    new_file = await context.bot.get_file(file_id)

    # لینک استارت به شکل صحیح برای دریافت فایل
    start_link = f"https://t.me/{context.bot.username}?start=get_{file_id}"
    
    # ارسال لینک استارت به کاربر
    await update.message.reply_text(f"فایل شما با موفقیت ذخیره شد!\nبرای دریافت فایل از لینک استارت زیر استفاده کنید:\n{start_link}")

# تابع main
def main():
    TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'  # توکن ربات خود را اینجا وارد کنید

    # ایجاد اپلیکیشن
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
