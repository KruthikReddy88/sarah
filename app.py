import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8645374295:AAFWk0wDoFJBZEbIZZACSWnxhVW0esetJ9Y"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

import requests

def get_ai_response(message):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    headers = {
        "Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"
    }

    payload = {
        "inputs": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()

        if isinstance(data, list):
            return data[0]["generated_text"]
        else:
            return "Error getting response."

    except Exception as e:
        return "AI is busy, try again."

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
