# Codex2050 Render Bot v2.2 – Telegram Ready

## Setup

1. Deploy to Render with `gunicorn app:app`
2. Run `auto_webhook.py` once to connect Telegram bot to Render
3. Extend `webhook()` logic in `app.py` to handle Telegram messages

## Files included:
- `app.py` – Main Flask app with webhook
- `auto_webhook.py` – Script to register webhook
- `telegram_handler.py` – Helper to send messages
- `requirements.txt`