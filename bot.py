import logging
import uuid
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات را مستقیماً وارد کنید
TOKEN = '6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM'  # جایگزین با توکن واقعی ربات

# شناسه‌های ادمین‌ها را مستقیماً وارد کنید
ADMINS = [1866821551]  # شناسه‌های تلگرام ادمین‌ها را وارد کنید

# اطلاعات دیتابیس PostgreSQL (این را از Railway گرفته‌اید یا در سیستم محلی خود تنظیم کنید)
DATABASE_URL = 'postgresql://postgres:qgnlDHjwgJOAgzEkehjQiUBsORyxaUzO@postgres.railway.internal:5432/railway'  # جایگزین با آدرس دیتابیس خود

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
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    unique_link = f'https://t.me/{context.bot.username}?start={str(uuid.uuid4())}'
    await update.message.reply_text(f'سلام {user.first_name}! برای دریافت فایل، روی لینک زیر کلیک کنید:\n{unique_link}')

# تابع ذخیره فایل در دیتابیس
async def handle_file(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    file = update.message.document or update.message.photo[-1]  # برای انواع فایل‌ها و تصاویر
    file_id = file.file_id
    file_caption = update.message.caption

    # اگر کاربر ادمین نبود، فایل را رد کنید
    if user.id not in ADMINS:
        await update.message.reply_text('شما مجاز به ارسال فایل نیستید.')
        return

    # ذخیره اطلاعات فایل در دیتابیس
    session = Session()
    new_file = FileInfo(file_id=file_id, caption=file_caption, user_id=user.id)
    session.add(new_file)
    session.commit()
    session.close()

    await update.message.reply_text(f'فایل با موفقیت آپلود شد! ID فایل: {file_id}')

# تابع ارسال فایل به کاربر بر اساس لینک استارت
async def send_file(update: Update, context: CallbackContext) -> None:
    start_param = update.message.text.split(' ')[1]
    session = Session()
    file_info = session.query(FileInfo).filter(FileInfo.file_id == start_param).first()
    session.close()

    if file_info:
        file = await context.bot.get_file(file_info.file_id)
        await file.download(f"file_{start_param}")
        await update.message.reply_document(document=open(f"file_{start_param}", 'rb'))
    else:
        await update.message.reply_text("این فایل یافت نشد.")

# تابع اصلی ربات
async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # افزودن هندلرهای مختلف
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^/getfile '), send_file))

    # استفاده از run_polling که خودش حلقه رویداد را مدیریت می‌کند
    await application.run_polling()

if __name__ == '__main__':
    # فقط از run_polling برای شروع ربات استفاده می‌کنیم
    import asyncio
    asyncio.run(main())  # از اینجا استفاده می‌کنیم که asyncio خودش حلقه رویداد را مدیریت کند
