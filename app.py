import requests
import os
from flask import Flask, request

app = Flask(__name__)

# 🔐 Secure environment variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_API_KEY = os.environ.get("HF_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# 🧠 AI Response
def get_ai_response(message):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": message
    }

    try:
        for _ in range(2):  # retry 2 times
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            data = response.json()

            if isinstance(data, list):
                return data[0]["generated_text"]

        return "AI is warming up... try again in a few seconds."

    except Exception:
        return "AI is busy right now."

# 🌐 Health check
@app.route("/", methods=["GET"])
def home():
    return "Jarvis is running!"

# 🤖 Telegram webhook
@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = get_ai_response(text)

        requests.post(
            TELEGRAM_URL,
            json={
                "chat_id": chat_id,
                "text": reply
            },
            timeout=5
        )

    return "ok"
