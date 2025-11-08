import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.mealty.ru/?express_flash_promo=1"
KEYWORDS = ["скидка 25", "экспресс-доставка", "акция"]

# токены будут подставляться GitHub Actions через secrets
BOT_TOKEN = None
CHAT_ID = None

def send_telegram_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Не заданы BOT_TOKEN или CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")

def check_discount():
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text().lower()
        if any(keyword in text for keyword in KEYWORDS):
            msg = f"🎉 На Mealty появилась акция на экспресс-доставку!\n{URL}"
            print(msg)
            send_telegram_message(msg)
        else:
            print(f"[{datetime.now()}] Акции нет.")
    except Exception as e:
        msg = f"[{datetime.now()}] Ошибка: {e}"
        print(msg)
        send_telegram_message(msg)

if __name__ == "__main__":
    import os
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    check_discount()
