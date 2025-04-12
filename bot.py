import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

# برای نگهداری آیدی فایل‌ها
FILE_STORAGE = "files.json"

# توکن بات تلگرام (توکن خودتون رو از BotFather بگیرید)
TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'

# ادمین‌ها
ADMINS = ['1866821551']

# ذخیره‌سازی فایل‌ها
def load_files():
    if os.path.exists(FILE_STORAGE):
        with open(FILE_STORAGE, "r") as file:
            return json.load(file)
    return {}

def save_files(files):
    with open(FILE_STORAGE, "w") as file:
        json.dump(files, file)

# فرمان start
def start(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    if str(user.id) in ADMINS:
        update.message.reply_text(
            f"سلام {user.first_name}, ارسال فایل رو شروع کن."
        )
    else:
        update.message.reply_text("دسترسی شما مجاز نیست.")

# فرمان برای دریافت فایل
def get_file(update: Update, _: CallbackContext) -> None:
    file_id = update.message.text.split(' ')[1]
    files = load_files()
    
    if file_id in files:
        file = files[file_id]
        update.message.reply_text(f"لینک فایل شما: {file['link']}")
    else:
        update.message.reply_text("فایلی با این شناسه پیدا نشد.")

# فرمان ارسال فایل توسط ادمین
def upload_file(update: Update, _: CallbackContext) -> None:
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
            
            update.message.reply_text(f"فایل آپلود شد! لینک دسترسی: {file_link}")
        else:
            update.message.reply_text("لطفاً یک فایل ارسال کنید.")
    else:
        update.message.reply_text("شما ادمین نیستید!")

def main() -> None:
    # ایجاد updater و dispatcher
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # دستورات بات
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("get", get_file))
    dispatcher.add_handler(MessageHandler(Filters.document, upload_file))

    # شروع بات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
