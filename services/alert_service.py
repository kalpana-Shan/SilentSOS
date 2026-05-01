# services/alert_service.py
import os
from dotenv import load_dotenv
load_dotenv()


def trigger_alert(alert_data: dict) -> bool:
    from database import get_db
    from services.email_service import send_alert_email

    email_enabled = os.getenv("EMAIL_ALERTS_ENABLED", "false").lower() == "true"

    try:
        conn = get_db()
        contacts = conn.execute("SELECT * FROM trusted_contacts").fetchall()

        if not contacts:
            print("⚠️ No trusted contacts found — demo mode")
            _demo_log(alert_data)
            conn.close()
            return True

        sent = 0
        for contact in contacts:
            if email_enabled and contact["email"]:
                print(f"📧 Sending alert email to: {contact['email']} ({contact['name']})")
                success = send_alert_email(
                    to_email=contact["email"],
                    contact_name=contact["name"],
                    alert_data=alert_data
                )
                if success:
                    sent += 1
            else:
                _demo_log(alert_data, contact["name"])
                sent += 1

        conn.close()
        print(f"✅ Alerts sent: {sent}/{len(contacts)}")
        return sent > 0

    except Exception as e:
        print(f"❌ trigger_alert failed: {e}")
        _demo_log(alert_data)
        return False


def _demo_log(alert_data: dict, contact_name: str = "Contact") -> None:
    print(f"\n{'='*50}")
    print(f"🚨 [SILENTSOS DEMO ALERT]")
    print(f"   To:      {contact_name}")
    print(f"   Risk:    {alert_data.get('risk_level', '?').upper()}")
    print(f"   Score:   {alert_data.get('final_score', 0)}/100")
    print(f"   Msg:     {alert_data.get('message_text', '')}")
    print(f"   Signals: {', '.join(alert_data.get('signals', []))}")
    print(f"   Reason:  {alert_data.get('explanation') or alert_data.get('hidden_distress_reason', 'N/A')}")
    print(f"{'='*50}\n")