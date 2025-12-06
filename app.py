from flask import Flask, request
import re
import requests
import os
import json

app = Flask(__name__)

# --- YOUR VALUES ---
TELEGRAM_TOKEN = "8270482574:AAFAOKe66e7iInHxXFHoSRrqCicJHANKre8"
CHAT_ID = 1628606216
# --------------------

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

@app.route("/", methods=["GET"])
def health():
    return "Jobot is running ✅", 200

@app.route("/", methods=["POST"])
def notify():
    # Try reading JSON first (Apps Script sends JSON)
    try:
        data = request.get_json(silent=True)
    except:
        data = None

    if data and isinstance(data, dict):
        raw_email = data.get("raw_email", "")
        subject = data.get("subject", "New Job Alert")
    else:
        # Fallback for raw POST text
        raw_email = request.data.decode("utf-8")
        subject_match = re.search(r"Subject: (.*)", raw_email)
        subject = subject_match.group(1) if subject_match else "New Job Alert"

    # Extract ALL links
    links = re.findall(r'https?://[^\s<>"\']+', raw_email)

    # Send notification if any link exists
    for link in links:
        send_telegram(f"📢 <b>{subject}</b>\n🔗 {link}")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
