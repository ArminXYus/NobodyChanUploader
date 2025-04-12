from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import json
import os

# توکن بات تلگرام
TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'

# ادمین‌ها
ADMINS = ['1866821551']

# ذخیره‌سازی فایل‌ها
FILE_STORAGE = "files.json"

def load_files():
    if os.path.exists(FILE_STORAGE):
        with open(FILE_STORAGE, "r") as file:
            return json.load(file)
    return {}

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
    file_id = update.message.text.split(' ')[1]
    files = load_files()

    if file_id in files:
        file = files[file_id]
        await update.message.reply_text(f"لینک فایل شما: {file['link']}")
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
            file_link = f"https://t.me/{update.message.bot.username}?start={file_id}"
            
            # ذخیره‌سازی فایل در فایل JSON
            files = load_files()
            files[file_id] = {"name": file_name, "link": file_link}
            save_files(files)
            
            await update.message.reply_text(f"فایل آپلود شد! لینک دسترسی: {file_link}")
        else:
            await update.message.reply_text("لطفاً یک فایل ارسال کنید.")
    else:
        await update.message.reply_text("شما ادمین نیستید!")

async def main() -> None:
    # ایجاد application و dispatcher
    application = Application.builder().token(TOKEN).build()

    # دستورات بات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get", get_file))
    application.add_handler(MessageHandler(filters.Document.ALL, upload_file))

    # شروع بات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
