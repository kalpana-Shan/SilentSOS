# routes/history.py
from fastapi import APIRouter
from database import get_db
import json

router = APIRouter()

@router.get("/alerts")
def get_alerts():
    conn = get_db()
    alerts = conn.execute(
        "SELECT * FROM alerts ORDER BY created_at DESC LIMIT 50"
    ).fetchall()
    conn.close()

    result = []
    for a in alerts:
        alert = dict(a)
        try:
            alert["signals"] = json.loads(alert["signals"]) if alert["signals"] else []
        except:
            alert["signals"] = []
        result.append(alert)
    return result

@router.get("/alerts/stats")
def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    high = conn.execute("SELECT COUNT(*) FROM alerts WHERE risk_level='high'").fetchone()[0]
    medium = conn.execute("SELECT COUNT(*) FROM alerts WHERE risk_level='medium'").fetchone()[0]
    low = conn.execute("SELECT COUNT(*) FROM alerts WHERE risk_level='low'").fetchone()[0]
    sent = conn.execute("SELECT COUNT(*) FROM alerts WHERE alert_sent=1").fetchone()[0]
    conn.close()
    return {
        "total_analyses": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "alerts_sent": sent
    }