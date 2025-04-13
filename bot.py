import logging
import uuid
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دیکشنری برای ذخیره فایل‌ها و شناسه‌های منحصر به فرد
file_storage = {}

# فرمان /start
async def start(update: Update, context: CallbackContext):
    # ارسال پیامی به ادمین بعد از شروع ربات
    await update.message.reply_text("سلام! لطفاً فایل خود را ارسال کنید.")

# فرمان برای دریافت فایل
async def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_id = file.file_id
    file_name = file.file_name
    caption = update.message.caption  # دریافت کپشن فایل

    # دانلود فایل از تلگرام
    new_file = await context.bot.get_file(file_id)

    # ایجاد شناسه منحصر به فرد برای فایل
    file_key = str(uuid.uuid4())  # شناسه منحصر به فرد با استفاده از uuid

    # ذخیره فایل در دیکشنری
    file_storage[file_key] = {
        "file_id": file_id,
        "file_name": file_name,
        "file_path": new_file.file_path,
        "caption": caption  # ذخیره کپشن
    }

    # لینک استارت به شکل صحیح برای دریافت فایل
    start_link = f"https://t.me/{context.bot.username}?start=get_{file_key}"

    # ارسال لینک استارت به کاربر
    await update.message.reply_text(f"فایل شما با موفقیت ذخیره شد!\nبرای دریافت فایل از لینک استارت زیر استفاده کنید:\n{start_link}")

# فرمان برای دریافت فایل از لینک استارت
async def get_file_from_link(update: Update, context: CallbackContext):
    start_arg = update.message.text.split(' ')[1]  # دریافت پارامتر بعد از `start=`
    
    # بررسی اینکه شناسه فایل موجود است یا نه
    if start_arg.startswith("get_") and start_arg[4:] in file_storage:
        file_key = start_arg[4:]
        file_data = file_storage[file_key]
        
        # ارسال فایل به همراه کپشن به کاربر
        await update.message.reply_document(
            document=file_data["file_path"], 
            filename=file_data["file_name"],
            caption=file_data["caption"]  # ارسال کپشن فایل
        )
    else:
        await update.message.reply_text("لینک معتبر نیست یا فایل یافت نشد.")

# تابع main
def main():
    TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'  # توکن ربات خود را اینجا وارد کنید

    # ایجاد اپلیکیشن
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.Regex(r'^/start=get_'), get_file_from_link))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
