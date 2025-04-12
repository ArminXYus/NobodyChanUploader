from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import json
import os

# توکن بات تلگرام
TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'

# یوزرنیم بات تلگرام (به صورت دستی وارد کنید)
BOT_USERNAME = 'NobodyUp_bot'  # به اینجا یوزرنیم بات خود را وارد کنید

# ادمین‌ها
ADMINS = ['1866821551']

# ذخیره‌سازی فایل‌ها
FILE_STORAGE = "files.json"

# تابع برای بارگذاری فایل‌ها
def load_files():
    if os.path.exists(FILE_STORAGE):
        with open(FILE_STORAGE, "r") as file:
            return json.load(file)
    else:
        # اگر فایل وجود نداشت، یک فایل جدید ایجاد می‌کنیم
        with open(FILE_STORAGE, "w") as file:
            json.dump({}, file)
        return {}

# تابع برای ذخیره فایل‌ها
def save_files(files):
    with open(FILE_STORAGE, "w") as file:
        json.dump(files, file)

# فرمان start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if str(user.id) in ADMINS:
        await update.message.reply_text(
            f"سلام {user.first_name}, ارسال فایل رو شروع کن."
        )
    else:
        await update.message.reply_text("دسترسی شما مجاز نیست.")

# فرمان برای دریافت فایل
async def get_file(update: Update, context: CallbackContext) -> None:
    # لینک استارت که کاربر می‌فرستد، باید شامل 'get_<file_id>' باشد
    file_id = update.message.text.split(' ')[1].replace('get_', '')  # حذف 'get_' از فایل آیدی
    files = load_files()

    if file_id in files:
        file = files[file_id]
        # ارسال فایل همراه با کپشن
        await update.message.reply_document(
            document=file['file'],
            caption=file['caption']
        )
    else:
        await update.message.reply_text("فایلی با این شناسه پیدا نشد.")

# فرمان ارسال فایل توسط ادمین
async def upload_file(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if str(user.id) in ADMINS:
        if update.message.document:
            file = update.message.document
            file_id = file.file_id
            file_name = file.file_name
            caption = update.message.caption if update.message.caption else "بدون کپشن"
            
            # لینک استارت برای ارسال فایل
            file_link = f"https://t.me/{BOT_USERNAME}?start=get_{file_id}"
            
            # نمایش اطلاعات فایل دریافتی و کپشن
            await update.message.reply_text(f"فایل دریافتی: {file_name} با file_id: {file_id}\nکپشن: {caption}")
            
            # ذخیره‌سازی فایل و کپشن در فایل JSON
            files = load_files()
            files[file_id] = {"file": file, "caption": caption, "link": file_link}
            save_files(files)
            
            await update.message.reply_text(f"فایل آپلود شد! لینک دسترسی: {file_link}\nکپشن: {caption}")
        else:
            await update.message.reply_text("لطفاً یک فایل ارسال کنید.")
    else:
        await update.message.reply_text("شما ادمین نیستید!")

# استفاده از application.run_polling() بدون نیاز به asyncio.run()
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # دستورات بات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get", get_file))

    # تغییر فیلتر برای دریافت هر نوع فایل
    application.add_handler(MessageHandler(filters.ALL, upload_file))

    # شروع بات
    application.run_polling()

if __name__ == '__main__':
    main()
