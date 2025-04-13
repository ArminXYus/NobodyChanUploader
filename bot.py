from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
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
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! برای دریافت فایل‌ها، لطفاً لینک شروع را بزنید.")

# فرمان برای دریافت فایل
def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_id = file.file_id
    file_name = file.file_name

    # دانلود فایل
    new_file = context.bot.get_file(file_id)
    file_path = os.path.join(UPLOAD_DIR, file_name)
    new_file.download(file_path)

    # ارسال لینک به کاربر
    start_link = f"https://t.me/{context.bot.username}?start=get_{file_id}"
    update.message.reply_text(f"فایل با موفقیت ذخیره شد! برای دریافت آن از لینک زیر استفاده کنید:\n{start_link}")

# تابع main
def main():
    # دریافت API Token از BotFather
    TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # اضافه کردن هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    # شروع ربات
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
