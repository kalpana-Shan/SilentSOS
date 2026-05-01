from fastapi import APIRouter
from database import get_connection
import json

router = APIRouter()

@router.get("/alerts")
def get_alerts():
    """Get all alert history"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY created_at DESC LIMIT 50"
    ).fetchall()
    conn.close()
    
    result = []
    for row in rows:
        r = dict(row)
        # Parse signals JSON string back to list
        if r["signals"]:
            try:
                r["signals"] = json.loads(r["signals"])
            except:
                r["signals"] = []
        else:
            r["signals"] = []
        result.append(r)
    
    return result

@router.get("/alerts/stats")
def get_stats():
    """Get alert statistics"""
    conn = get_connection()
    
    total = conn.execute("SELECT COUNT(*) as count FROM alerts").fetchone()
    high = conn.execute("SELECT COUNT(*) as count FROM alerts WHERE risk_level='high'").fetchone()
    medium = conn.execute("SELECT COUNT(*) as count FROM alerts WHERE risk_level='medium'").fetchone()
    low = conn.execute("SELECT COUNT(*) as count FROM alerts WHERE risk_level='low'").fetchone()
    
    conn.close()
    
    return {
        "total_analyses": total["count"],
        "high_risk": high["count"],
        "medium_risk": medium["count"],
        "low_risk": low["count"]
    }

@router.get("/alerts/{alert_id}")
def get_alert(alert_id: int):
    """Get specific alert details"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,)).fetchone()
    conn.close()
    
    if row:
        result = dict(row)
        if result["signals"]:
            try:
                result["signals"] = json.loads(result["signals"])
            except:
                result["signals"] = []
        return result
    else:
        return {"error": "Alert not found"}