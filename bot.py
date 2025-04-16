import logging
import uuid
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دریافت توکن ربات از متغیر محیطی
TOKEN = os.getenv('TELEGRAM_TOKEN')

# دریافت شناسه ادمین‌ها از متغیر محیطی
ADMINS = list(map(int, os.getenv('ADMINS').split(',')))

# اطلاعات دیتابیس PostgreSQL (این را از Railway گرفته‌اید)
DATABASE_URL = os.getenv("DATABASE_URL")

# تنظیمات دیتابیس
Base = declarative_base()

class FileInfo(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True)
    file_id = Column(String, nullable=False)
    caption = Column(Text)
    user_id = Column(Integer, nullable=False)

# ایجاد دیتابیس و جدول
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# تابع شروع (Start) ربات
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    unique_link = f'https://t.me/{context.bot.username}?start={str(uuid.uuid4())}'
    update.message.reply_text(f'سلام {user.first_name}! برای دریافت فایل، روی لینک زیر کلیک کنید:\n{unique_link}')

# تابع ذخیره فایل در دیتابیس
def handle_file(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    file = update.message.document or update.message.photo[-1]  # برای انواع فایل‌ها و تصاویر
    file_id = file.file_id
    file_caption = update.message.caption

    # اگر کاربر ادمین نبود، فایل را رد کنید
    if user.id not in ADMINS:
        update.message.reply_text('شما مجاز به ارسال فایل نیستید.')
        return

    # ذخیره اطلاعات فایل در دیتابیس
    session = Session()
    new_file = FileInfo(file_id=file_id, caption=file_caption, user_id=user.id)
    session.add(new_file)
    session.commit()
    session.close()

    update.message.reply_text(f'فایل با موفقیت آپلود شد! ID فایل: {file_id}')

# تابع ارسال فایل به کاربر بر اساس لینک استارت
def send_file(update: Update, context: CallbackContext) -> None:
    start_param = update.message.text.split(' ')[1]
    session = Session()
    file_info = session.query(FileInfo).filter(FileInfo.file_id == start_param).first()
    session.close()

    if file_info:
        file = context.bot.get_file(file_info.file_id)
        file.download(f"file_{start_param}")
        update.message.reply_document(document=open(f"file_{start_param}", 'rb'))
    else:
        update.message.reply_text("این فایل یافت نشد.")

# تابع اصلی ربات
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # افزودن هندلرهای مختلف
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document | Filters.photo, handle_file))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex('^/getfile '), send_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
