import os
from dotenv import load_dotenv

load_dotenv()

# Try to import Twilio, but don't fail if not available
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("⚠️ Twilio not available - using simulation mode")

def send_sms_alert(contact_phone: str, contact_name: str,
                   user_name: str, risk_level: str,
                   signals: list, location_lat: float = None,
                   location_lng: float = None) -> bool:
    """Send SMS alert via Twilio or fallback to simulation"""
    
    signal_text = ", ".join(signals[:3]) if signals else "behavioral anomaly detected"

    location_text = ""
    if location_lat and location_lng:
        location_text = f"\n📍 Location: https://maps.google.com/?q={location_lat},{location_lng}"

    guidance = {
        "high": "⚠️ URGENT: Call immediately. Ask simple yes/no questions. Do NOT confront anyone directly.",
        "medium": "📞 Please check in with them when possible.",
        "low": "ℹ️ This is a monitoring alert only. No immediate action needed."
    }.get(risk_level, "")

    message_body = (
        f"🔴 SILENTSOS ALERT\n\n"
        f"Hi {contact_name},\n"
        f"{user_name} may need help.\n"
        f"Risk Level: {risk_level.upper()}\n"
        f"Signals: {signal_text}"
        f"{location_text}\n\n"
        f"{guidance}\n\n"
        f"— SilentSOS Safety System"
    )

    # Try Twilio if configured
    if TWILIO_AVAILABLE and os.getenv("TWILIO_ACCOUNT_SID"):
        try:
            client = Client(
                os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN")
            )
            client.messages.create(
                body=message_body,
                from_=os.getenv("TWILIO_FROM_NUMBER"),
                to=contact_phone
            )
            print(f"✅ SMS sent to {contact_name} ({contact_phone})")
            return True
        except Exception as e:
            print(f"❌ SMS failed: {e}")
            return False
    else:
        # Simulation mode for hackathon
        print(f"\n📱 [SIMULATED SMS]")
        print(f"   To: {contact_name} ({contact_phone})")
        print(f"   Message: {message_body[:200]}...")
        return True

def simulate_alert(contact_name: str, user_name: str, risk_level: str, signals: list) -> dict:
    """Simple simulation for demo purposes"""
    return {
        "status": "simulated",
        "to": contact_name,
        "message": f"SilentSOS: {user_name} flagged at {risk_level} risk. Signals: {signals[:2]}"
    }