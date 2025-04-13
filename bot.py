from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext
import os
import logging

# تنظیمات لاگینگ برای اشکال‌زدایی
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)
logger = logging.getLogger(__name__)

# مسیر ذخیره فایل‌ها
UPLOAD_DIR = '/path/to/save/files'

# فرمان /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("سلام! برای دریافت فایل‌ها، لطفاً لینک شروع را بزنید.")

# فرمان برای دریافت فایل
async def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_id = file.file_id
    file_name = file.file_name

    # دانلود فایل
    new_file = await context.bot.get_file(file_id)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    await new_file.download(file_path)

    # ارسال لینک به کاربر
    start_link = f"https://t.me/{context.bot.username}?start=get_{file_id}"
    await update.message.reply_text(f"فایل با موفقیت ذخیره شد! برای دریافت آن از لینک زیر استفاده کنید:\n{start_link}")

# تابع main
def main():
    # دریافت API Token از BotFather
    TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'

    # ایجاد اپلیکیشن جدید
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
