import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8645374295:AAFWk0wDoFJBZEbIZZACSWnxhVW0esetJ9Y"
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

# 🔥 IMPORTANT FIX FOR RENDER
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
