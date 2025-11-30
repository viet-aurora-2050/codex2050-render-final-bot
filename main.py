from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "7416243786:AAGHCZtotfZeUz2o-kTZYcZIXQnc1fZsmu0"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "Willkommen im Codex2050-Bot. Gib deinen Sigil ein:")
        else:
            send_message(chat_id, f"Du hast gesendet: {text}")
    return {"ok": True}
