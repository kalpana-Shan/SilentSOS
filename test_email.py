from services.email_service import send_alert_email

result = send_alert_email(
    to_email="silentsos.alert@gmail.com",
    contact_name="Kalpana",
    alert_data={
        "risk_level": "high",
        "final_score": 87,
        "message_text": "Amma naan late varuven, phone charge kammi, worry pannadhe",
        "signals": ["excessive reassurance", "communication restriction"],
        "hidden_distress_reason": "Message contains reassurance with battery restriction cue",
        "context_reasons": ["late-night message", "unusual location detected"],
        "lat": 10.7905,
        "lng": 78.7047
    }
)

print("Email sent:", result)