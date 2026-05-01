# services/email_service.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT   = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL    = os.getenv("ALERT_EMAIL")
SENDER_PASSWORD = os.getenv("ALERT_PASSWORD")  # Gmail App Password


def send_alert_email(to_email: str, contact_name: str, alert_data: dict) -> bool:
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("❌ Email credentials not set in .env")
        return False

    risk     = alert_data.get("risk_level", "unknown").upper()
    score    = alert_data.get("final_score", 0)
    message  = alert_data.get("message_text", "")
    signals  = alert_data.get("signals", [])
    reason   = alert_data.get("explanation") or alert_data.get("hidden_distress_reason", "N/A")
    lat      = alert_data.get("lat", "N/A")
    lng      = alert_data.get("lng", "N/A")

    if lat != "N/A":
        maps_url = f"https://maps.google.com/?q={lat},{lng}"
        location_html = f'<a href="{maps_url}" style="color:#2563eb">📍 View on Google Maps ({lat}, {lng})</a>'
    else:
        location_html = "<span style='color:#6b7280'>Location not available</span>"

    risk_color = {"HIGH": "#dc2626", "MEDIUM": "#d97706", "LOW": "#16a34a"}.get(risk, "#6b7280")

    html = f"""
    <div style="font-family:sans-serif;max-width:520px;margin:auto;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden">
      <div style="background:{risk_color};padding:20px 24px">
        <h2 style="color:#fff;margin:0;font-size:20px">🚨 SilentSOS Alert</h2>
        <p style="color:#fff;opacity:0.9;margin:4px 0 0">Possible distress signal detected</p>
      </div>
      <div style="padding:24px">
        <p>Hi <b>{contact_name}</b>, someone you trust may need help.</p>

        <table style="width:100%;border-collapse:collapse;margin:16px 0">
          <tr style="background:#f9fafb">
            <td style="padding:10px 14px;font-weight:600;width:38%">Risk Level</td>
            <td style="padding:10px 14px;color:{risk_color};font-weight:700">{risk}</td>
          </tr>
          <tr>
            <td style="padding:10px 14px;font-weight:600">Confidence Score</td>
            <td style="padding:10px 14px">{score}/100</td>
          </tr>
          <tr style="background:#f9fafb">
            <td style="padding:10px 14px;font-weight:600">Message Analyzed</td>
            <td style="padding:10px 14px;font-style:italic">"{message}"</td>
          </tr>
          <tr>
            <td style="padding:10px 14px;font-weight:600">Signals Detected</td>
            <td style="padding:10px 14px">{', '.join(signals) if signals else 'None'}</td>
          </tr>
          <tr style="background:#f9fafb">
            <td style="padding:10px 14px;font-weight:600">AI Reasoning</td>
            <td style="padding:10px 14px">{reason}</td>
          </tr>
          <tr>
            <td style="padding:10px 14px;font-weight:600">Last Location</td>
            <td style="padding:10px 14px">{location_html}</td>
          </tr>
        </table>

        <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:14px 16px;margin-top:8px">
          <b style="color:#dc2626">⚠️ What to do now:</b>
          <ul style="margin:8px 0 0;padding-left:18px;color:#374151">
            <li>Call them immediately</li>
            <li>Ask only yes/no questions if unsure of their safety</li>
            <li>Do NOT confront any suspected threat directly</li>
            <li>Contact local emergency services if unreachable</li>
          </ul>
        </div>
      </div>
      <div style="background:#f9fafb;padding:14px 24px;text-align:center">
        <p style="color:#9ca3af;font-size:12px;margin:0">
          Sent by SilentSOS · AI-Powered Safety System<br>
          This alert was generated automatically. Trust your instincts.
        </p>
      </div>
    </div>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 SilentSOS [{risk}] Distress Signal Detected"
        msg["From"]    = f"SilentSOS Alert <{SENDER_EMAIL}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"✅ Alert email sent to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail auth failed — use an App Password, not your account password")
        print("   → https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False