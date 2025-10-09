from twilio.rest import Client

# Your credentials
ACCOUNT_SID = "ACd422fa0e3b159cee66a35d482c745caf"
AUTH_TOKEN = "40e778cf32fc1b81e0832255ab5785e8"

# Sandbox number
TWILIO_WHATSAPP = "whatsapp:+14155238886"

# Your phone number
YOUR_PHONE = "whatsapp:+14077929959"

# Initialize client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Send test message
print("📤 Sending test WhatsApp message...")

message = client.messages.create(
    from_=TWILIO_WHATSAPP,
    to=YOUR_PHONE,
    body="""🎉 Test Message - Enchanted Strollers

Hi Michael! This is a test notification from your new WhatsApp system.

If you're seeing this, everything is working perfectly! ✅

Next step: Set up Telegram notifications and deploy to production.

🚀 System Status: READY"""
)

print(f"✅ Message sent successfully!")
print(f"📋 Message SID: {message.sid}")
print(f"📱 Status: {message.status}")
print(f"\nCheck your WhatsApp now! 📱")
