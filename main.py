
# main.py – Codex2050Bot SIGIL-ready core
import os
import logging
import requests
from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    app.logger.warning("TELEGRAM_TOKEN is not set – bot will not send messages until configured.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None


def send_message(chat_id: int, text: str) -> None:
    """Send a simple text message to a Telegram chat."""
    if not TELEGRAM_API_URL:
        app.logger.error("Cannot send message: TELEGRAM_API_URL is not configured.")
        return

    try:
        resp = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )
        if resp.status_code != 200:
            app.logger.error("Telegram sendMessage error: %s", resp.text)
    except Exception as e:
        app.logger.error("send_message exception: %s", e)


@app.route("/", methods=["GET"])
def index():
    """Health-check endpoint for Render/Web browser."""
    return "✅ Codex2050Bot – SIGIL core online"


@app.route("/", methods=["POST"])
def webhook():
    """Telegram webhook endpoint."""
    try:
        update = request.get_json(force=True, silent=True) or {}
    except Exception:
        update = {}

    message = update.get("message", {}) or {}
    chat = message.get("chat", {}) or {}
    chat_id = chat.get("id")
    text = message.get("text", "") or ""

    if not chat_id:
        # Nothing to answer
        return {"ok": True}

    # Core logic
    if text == "/start":
        send_message(
            chat_id,
            "Willkommen im Codex2050-Bot.\n"
            "Gib deinen Sigil ein (z.B. sigil:epsilon!2050).",
        )
    else:
        normalized = text.strip().lower()

        if normalized == "sigil:epsilon!2050":
            send_message(
                chat_id,
                "🜏 Sigil ε erkannt.\n"
                "2050-Kernverbindung aktiv. Protokoll läuft im Hintergrund."
            )
        elif normalized == "sigil:alpha!2050":
            send_message(
                chat_id,
                "♜ Sigil α erkannt.\n"
                "Strategie-Kanal geöffnet. Weitere Module folgen."
            )
        else:
            # Default Echo + Log
            app.logger.info("Unbekannter Sigil oder Text empfangen: %s", text)
            send_message(
                chat_id,
                f"Sigil/Text empfangen: {text}\n"
                "(Noch keine spezielle Aktion hinterlegt – nur gespeichert.)"
            )

    return {"ok": True}


if __name__ == "__main__":
    # For local testing; on Render gunicorn will be used
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
