
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def dashboard():
    return "<h1>Codex2050 Dashboard online.</h1>"

if __name__ == '__main__':
    app.run()
