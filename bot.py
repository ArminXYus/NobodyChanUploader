from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# توکن ربات تلگرام شما
TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'

# لیستی برای نگهداری فایل‌ها و لینک‌های استارت
files_data = {}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("سلام! شما می‌توانید فایل‌های خود را ارسال کنید.")

async def admin_handler(update: Update, context: CallbackContext) -> None:
    # اطمینان از اینکه فقط ادمین می‌تواند فایل ارسال کند
    admin_id = '1866821551'
    if update.message.from_user.id == int(admin_id):
        # گرفتن فایل و کپشن
        file = update.message.document
        caption = update.message.caption if update.message.caption else ""

        # ذخیره فایل
        file_id = file.file_id
        file_data = {'file_id': file_id, 'caption': caption}
        files_data[file_id] = file_data

        # ارسال تایید به ادمین
        await update.message.reply_text(f"فایل با موفقیت ذخیره شد! لینک استارت بات: https://t.me/{context.bot.username}?start=get_{file_id}")
    else:
        await update.message.reply_text("شما اجازه ارسال فایل ندارید.")

async def get_file(update: Update, context: CallbackContext) -> None:
    # گرفتن فایل از لینک استارت
    if context.args:
        file_id = context.args[0]
        file_data = files_data.get(file_id)

        if file_data:
            file = await context.bot.get_file(file_data['file_id'])
            await file.download(f"{file_id}.jpg")  # ذخیره فایل
            await update.message.reply_text(f"فایل با موفقیت دانلود شد: {file_data['caption']}")
        else:
            await update.message.reply_text("فایل یافت نشد.")
    else:
        await update.message.reply_text("لطفاً لینک استارت صحیح را وارد کنید.")

def main() -> None:
    # ایجاد و راه‌اندازی ربات
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن دستورات
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.ALL, admin_handler))  # گرفتن فایل از ادمین
    application.add_handler(CommandHandler('get', get_file))  # دریافت فایل از لینک استارت

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
