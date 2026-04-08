import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def get_ai_response(message):
    return f"You said: {message}\n\nI'm your AI assistant 🚀"

@app.route("/", methods=["GET"])
def home():
    return "Jarvis is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = get_ai_response(text)

        requests.post(TELEGRAM_URL, json={
            "chat_id": chat_id,
            "text": reply
        })

    return "ok"
