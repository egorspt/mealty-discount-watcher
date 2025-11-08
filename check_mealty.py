import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- НАСТРОЙКИ ---
URL = "https://www.mealty.ru/?express_flash_promo=1"
KEYWORDS = ["скидка 25", "экспресс-доставка", "акция"]
BOT_TOKEN = "8370343717:AAHxZWfIxji4q7sHeTA0AAafOpiREdv8nYA"
CHAT_ID = "227016019"

def send_telegram_message(text: str):
    """Отправить сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")

def check_discount():
    """Проверить наличие акции"""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text().lower()

        if any(keyword in text for keyword in KEYWORDS):
            msg = f"🎉 На Mealty появилась акция на экспресс-доставку!\n{URL}"
            print(f"[{datetime.now()}] {msg}")
            send_telegram_message(msg)
        else:
            print(f"[{datetime.now()}] Акции нет.")
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка при проверке: {e}")

if __name__ == "__main__":
    check_discount()
