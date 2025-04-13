import requests
import json

# توکن ربات تلگرام خود را وارد کنید
TOKEN = "6668878971:AAG2S5-H1e-eVk-ffpjYt20bEJp5MRJc-vM"  
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

# وبهوک که پیام‌های دریافتی را پردازش می‌کند
def handle_telegram_update(update):
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]

        # بررسی نوع پیام
        if "document" in update["message"] or "video" in update["message"] or "photo" in update["message"]:
            file_id = None

            if "document" in update["message"]:
                file_id = update["message"]["document"]["file_id"]
            elif "video" in update["message"]:
                file_id = update["message"]["video"]["file_id"]
            elif "photo" in update["message"]:
                # عکس‌ها لیستی از ابعاد مختلف دارند، بنابراین باید آخرین عکس را انتخاب کرد
                file_id = update["message"]["photo"][-1]["file_id"]

            # دریافت لینک فایل از تلگرام
            file_link = get_telegram_file_url(file_id)

            # ارسال پیام به کاربر با لینک فایل
            response_text = f"✅ فایل شما آپلود شد!\n🔗 لینک دانلود: {file_link}"
            send_message(chat_id, response_text)

        else:
            send_message(chat_id, "📂 لطفاً یک فایل ارسال کنید!")

    return "Message processed"

# دریافت لینک فایل از سرور تلگرام
def get_telegram_file_url(file_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    response = requests.get(url)
    result = response.json()

    if result["ok"]:
        file_path = result["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    else:
        return "❌ خطا در دریافت لینک فایل."

# ارسال پیام به چت تلگرام
def send_message(chat_id, text):
    url = f"{API_URL}sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)

# تابع اصلی که وبهوک را پردازش می‌کند
def main(request):
    update = request.json()  # داده‌های ورودی از ربات تلگرام

    # پردازش آپدیت
    return handle_telegram_update(update)

