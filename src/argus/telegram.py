import logging
import os
import requests


def is_telegram_enabled() -> bool:
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def send_telegram_message(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logging.error(
            "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing from environment variables."
        )
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if data.get("ok"):
            logging.info("Telegram message sent successfully")
            return True
        else:
            logging.error(f"Failed to send Telegram message: {data.get('description')}")
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while sending Telegram message: {e}")
        return False
