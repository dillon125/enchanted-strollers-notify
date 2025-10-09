from flask import Flask, request, jsonify
from twilio.rest import Client
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get credentials from environment
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP = os.getenv('TWILIO_WHATSAPP_SANDBOX')
TEST_PHONE = os.getenv('TEST_PHONE')
CLIENT_PHONE = os.getenv('CLIENT_PHONE')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_whatsapp(to_number, message):
    """Send WhatsApp message"""
    try:
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"
        
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP,
            to=to_number,
            body=message
        )
        
        logger.info(f"✅ WhatsApp sent: {msg.sid}")
        return {"status": "sent", "sid": msg.sid}
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"status": "error", "error": str(e)}


@app.route('/test', methods=['GET', 'POST'])
def test():
    """Quick test endpoint"""
    
    test_msg = f"""🧪 TEST - Enchanted Strollers

Order notification test!

⏰ {datetime.now().strftime('%I:%M %p')}
📱 System: Working perfectly! ✅

This is what your customers will see when they place an order."""
    
    result = send_whatsapp(TEST_PHONE, test_msg)
    
    return jsonify({
        "test": "complete",
        "sent_to": TEST_PHONE,
        "result": result
    }), 200


@app.route('/order', methods=['POST'])
def order():
    """Order notification endpoint"""
    data = request.get_json() or {}
    
    # Use test phone or client phone
    use_client = data.get('use_client', False)
    phone = CLIENT_PHONE if use_client else TEST_PHONE
    
    order_msg = f"""🎉 Order Confirmed - Enchanted Strollers

Hi {data.get('customer_name', 'Customer')}!

Your magical stroller rental is confirmed!

📋 Order #{data.get('order_id', 'ES001')}
📅 Pickup: {data.get('pickup_date', 'Oct 15, 2025')}
📍 Location: {data.get('pickup_location', 'Magic Kingdom')}
🛒 {data.get('items', 'Double Stroller')}
💰 Total: ${data.get('total', '89.99')}

We'll keep you updated! Questions? Just reply to this message. ✨"""
    
    result = send_whatsapp(phone, order_msg)
    
    return jsonify({
        "status": "success",
        "order_id": data.get('order_id'),
        "sent_to": phone,
        "result": result
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "whatsapp": TWILIO_WHATSAPP,
        "test_phone": TEST_PHONE,
        "time": datetime.now().isoformat()
    }), 200


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 ENCHANTED STROLLERS - Testing")
    print("="*50)
    print(f"📱 Sandbox: {TWILIO_WHATSAPP}")
    print(f"🧪 Your Phone: {TEST_PHONE}")
    print(f"👤 Client Phone: {CLIENT_PHONE}")
    print("="*50)
    print("\n🧪 Test URL: http://localhost:5000/test")
    print("📦 Order URL: http://localhost:5000/order")
    print("\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
