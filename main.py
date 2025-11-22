import os
import logging
import requests
from flask import Flask, request
from codex2050_engine import Codex2050Engine

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
ME = YOUR_TELEGRAM_USER_ID = 0  # <- ERSETZEN MIT DEINER USER ID

engine = Codex2050Engine()

def send(cid, text, preview=False, protect=False):
    requests.post(
        f"{BASE}/sendMessage",
        json={
            "chat_id": cid,
            "text": text[:3900],
            "disable_web_page_preview": not preview,
            "protect_content": protect
        }
    )

def get_file(file_id):
    fi = requests.get(f"{BASE}/getFile?file_id={file_id}").json()
    path = fi["result"]["file_path"]
    return requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{path}").content


@app.route("/", methods=["POST"])
def hook():
    try:
        upd = request.get_json()

        if "message" not in upd:
            return {"ok": True}

        msg = upd["message"]
        cid = msg["chat"]["id"]
        uid = msg["from"]["id"]

        # 🔒 Sicherheit: finale Stufe
        def allowed():
            return uid == YOUR_TELEGRAM_USER_ID

        # ░░ TEXT ░░
        if "text" in msg:
            t = msg["text"].strip()

            # /start
            if t == "/start":
                send(cid, "🔥 Codex2050 – Finale Stufe aktiviert.\nAlles freigeschaltet.")
                return {"ok": True}

            # /menu
            if t == "/menu":
                send(cid,
                     "🔮 *Codex2050 – Menü*\n"
                     "/analyse <txt>\n"
                     "/run <cmd>\n"
                     "/vision\n"
                     "/secret <txt>\n"
                     "/vault <txt>\n"
                     "/predict <frage>\n"
                     "/hash <txt>\n"
                     "/codex <befehl>\n"
                     "/recover\n"
                     "/archive\n",
                     preview=False)
                return {"ok": True}

            # /analyse
            if t.startswith("/analyse "):
                payload = t.replace("/analyse ", "", 1)
                out = engine.analyse(payload)
                send(cid, f"🔍 Analyse:\n{out}")
                return {"ok": True}

            # /run
            if t.startswith("/run "):
                if not allowed():
                    send(cid, "❌ Zugriff verweigert.")
                    return {"ok": True}
                cmd = t.replace("/run ", "", 1)
                out = engine.execute(cmd)
                send(cid, f"⚙️ Engine:\n{out}")
                return {"ok": True}

            # /secret
            if t.startswith("/secret "):
                secret = t.replace("/secret ", "", 1)
                send(cid, f"🔒 {secret}", protect=True)
                return {"ok": True}

            # /vault (finale Sicherheitsstufe)
            if t.startswith("/vault "):
                if not allowed():
                    send(cid, "❌ Nicht autorisiert.")
                    return {"ok": True}
                x = t.replace("/vault ", "", 1)
                reply = engine.vault(x)
                send(cid, f"🗄️ Vault:\n{reply}", protect=True)
                return {"ok": True}

            # /hash
            if t.startswith("/hash "):
                raw = t.replace("/hash ", "", 1)
                out = engine.hash(raw)
                send(cid, f"🔑 SHA256:\n{out}")
                return {"ok": True}

            # /predict
            if t.startswith("/predict "):
                q = t.replace("/predict ", "", 1)
                out = engine.predict(q)
                send(cid, f"🔮 Prognose:\n{out}")
                return {"ok": True}

            # /codex
            if t.startswith("/codex "):
                if not allowed():
                    send(cid, "❌ Zugriff verweigert.")
                    return {"ok": True}
                c = t.replace("/codex ", "", 1)
                out = engine.codex(c)
                send(cid, f"📜 Codex:\n{out}")
                return {"ok": True}

            # /recover
            if t == "/recover":
                if not allowed():
                    send(cid, "❌ Nicht autorisiert.")
                    return {"ok": True}
                out = engine.recover()
                send(cid, f"🛡️ Recovery:\n{out}")
                return {"ok": True}

            # /vision
            if t == "/vision":
                send(cid, "📸 Sende ein Bild zur Analyse.")
                return {"ok": True}

            # /archive
            if t == "/archive":
                out = engine.archive()
                send(cid, f"📦 Archiv:\n{out}")
                return {"ok": True}

            # Fallback
            send(cid, "Befehl erkannt – finale Stufe aktiv.")
            return {"ok": True}

        # ░░ BILDER ░░
        if "photo" in msg:
            fid = msg["photo"][-1]["file_id"]
            img = get_file(fid)
            out = engine.vision(img)
            send(cid, f"🖼️ Vision:\n{out}")
            return {"ok": True}

        # ░░ DATEIEN ░░
        if "document" in msg:
            f = msg["document"]
            fid = f["file_id"]
            name = f["file_name"]
            bin = get_file(fid)
            out = engine.analyse_file(name, bin)
            send(cid, f"📂 Datei:\n{out}")
            return {"ok": True}

        return {"ok": True}

    except Exception as e:
        logging.error(f"ERR: {e}")
        if YOUR_TELEGRAM_USER_ID:
            send(YOUR_TELEGRAM_USER_ID, f"❌ Render-Error:\n{e}")
        return {"ok": False}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
