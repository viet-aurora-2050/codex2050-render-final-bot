from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Bot v2.2 Online"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)  # Debug-Zweck
    return jsonify({"status": "received"})