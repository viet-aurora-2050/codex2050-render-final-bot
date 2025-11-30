from flask import Flask
app = Flask(__name__)
@app.route('/')
def index(): return 'Codex2050 Bot v2.1 Online'