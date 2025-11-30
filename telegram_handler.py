import requests
import json

def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    headers = {"Content-Type": "application/json"}
    requests.post(url, data=json.dumps(payload), headers=headers)