from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
ACCOUNT_SID = "AC2a60eb2397bf6c06bce71086c5c629e3"
AUTH_TOKEN = "7a7693cdc7fef39f318c03b3254736f4"
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Twilio sandbox numbers
TWILIO_WHATSAPP = "whatsapp:+14155238886"
MY_WHATSAPP = "whatsapp:+14077929959"

@app.route("/send-notification", methods=["POST"])
def send_notification():
    data = request.get_json()
    msg = data.get("message", "📦 Your stroller order has been received and is being processed.")
    phone = MY_WHATSAPP  # or dynamically assign from your order system

    message = client.messages.create(
        from_=TWILIO_WHATSAPP,
        to=phone,
        body=msg
    )

    print("✅ WhatsApp message sent:", message.sid)
    return jsonify({"status": "sent", "sid": message.sid})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
