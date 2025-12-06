from flask import Flask, request
import re
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "Y8270482574:AAFAOKe66e7iInHxXFHoSRrqCicJHANKre8"
CHAT_ID = 1628606216

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

@app.route("/", methods=["GET"])
def health():
    return "Jobot is running ✅", 200

@app.route("/", methods=["POST"])
def notify():
    raw = request.data.decode("utf-8")

    links = re.findall(r'https?://\S+', raw)
    subject_match = re.search(r"Subject: (.*)", raw)
    title = subject_match.group(1) if subject_match else "New Job Alert"

    if links:
        for link in links:
            send_telegram(f"📢 <b>{title}</b>\n🔗 {link}")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
