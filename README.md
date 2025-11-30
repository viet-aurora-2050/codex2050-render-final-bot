
# Codex2050Bot – SIGIL Ready v1

Minimaler, aber kompletter Telegram-Webhook-Bot für Render.

## Dateien

- `main.py` – Flask-App mit SIGIL-Logik und Telegram-Webhooks
- `requirements.txt` – Python-Pakete
- `Procfile` – Startbefehl für Render (`gunicorn main:app`)

## Kurz-Anleitung

1. ZIP entpacken, als neues GitHub-Repo hochladen.
2. Auf Render als Web Service deployen.
3. Environment Variable setzen: `TELEGRAM_TOKEN` = dein Bot-Token.
4. Webhook setzen:

   `https://api.telegram.org/bot<DEIN_TOKEN>/setWebhook?url=<DEINE_RENDER_URL>`

Dann in Telegram `/start` + deinen Sigil schicken (z.B. `sigil:epsilon!2050`).
