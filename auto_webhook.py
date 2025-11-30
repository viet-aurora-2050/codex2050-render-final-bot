import requests

BOT_TOKEN = "7416243786:AAGHCZtotfZeUz2o-kTZYcZIXQnc1fZsmu0"
WEBHOOK_URL = "https://codex2050-bot.onrender.com/webhook"

def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.get(url, params={"url": WEBHOOK_URL})
    print("Webhook set:", response.json())

if __name__ == "__main__":
    set_webhook()