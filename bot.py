import os
import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pyshorteners

# تنظیمات اولیه
TOKEN = os.getenv('TELEGRAM_TOKEN')  # توکن ربات از Railway
ADMIN_USERS = [1866821551]  # ID ادمین‌ها
UPLOAD_DIR = 'uploaded_files/'

# فعال‌سازی logging برای اشکال‌زدایی
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# اطمینان از ایجاد دایرکتوری برای ذخیره فایل‌ها
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# تابع استارت برای کاربرانی که از لینک استارت استفاده می‌کنند
def start(update: Update, context: CallbackContext) -> None:
    # دریافت شناسه فایل از داده‌های start
    file_unique_id = context.args[0] if context.args else None
    
    if file_unique_id:
        # تلاش برای پیدا کردن فایل بر اساس unique_id
        file_path = os.path.join(UPLOAD_DIR, f"{file_unique_id}.pdf")  # فرض کردیم که فایل PDF است
        if os.path.exists(file_path):
            update.message.reply_document(document=open(file_path, 'rb'))
        else:
            update.message.reply_text("متاسفانه فایل مورد نظر یافت نشد.")
    else:
        update.message.reply_text('لطفا فایل ارسال کنید.')

# دریافت فایل از کاربر
def handle_file(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # چک کردن که آیا کاربر از ادمین‌ها است یا خیر
    if user_id not in ADMIN_USERS:
        update.message.reply_text("شما مجاز به ارسال فایل نیستید!")
        return

    # دریافت فایل و ذخیره‌سازی آن
    file = update.message.document
    if file:
        # دریافت فایل و ذخیره‌سازی آن
        file_unique_id = file.file_unique_id
        file_path = os.path.join(UPLOAD_DIR, f"{file_unique_id}.pdf")
        file.download(file_path)
        
        # ایجاد لینک استارت
        start_link = f"https://t.me/{update.message.bot.username}?start={file_unique_id}"

        # ارسال لینک استارت به کاربر
        update.message.reply_text(f"فایل شما با موفقیت ذخیره شد! برای دسترسی به فایل خود، از لینک زیر استفاده کنید:\n{start_link}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # ثبت دستور استارت
    dispatcher.add_handler(CommandHandler('start', start))

    # ثبت handler برای دریافت فایل
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
