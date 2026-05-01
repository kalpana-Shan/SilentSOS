from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

from services.gemini_service import analyze_message
from services.risk_engine import compute_context_score, compute_final_score, extract_behavior_flags
from services.alert_service import send_sms_alert
from database import get_connection

router = APIRouter()

class AnalyzeRequest(BaseModel):
    message: str
    time: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    location_anomaly: Optional[bool] = False
    user_name: Optional[str] = "User"

@router.post("/analyze-message")
def analyze_message_endpoint(req: AnalyzeRequest):
    # Step 1: Get AI semantic analysis
    ai_result = analyze_message(req.message)
    semantic_score = ai_result.get("semantic_score", 0)
    signals = ai_result.get("signals", [])

    # Step 2: Extract behavior flags
    behavior_flags = extract_behavior_flags(req.message, signals)

    # Step 3: Calculate context score
    time_str = req.time or datetime.now().isoformat()
    context_score = compute_context_score(
        time_str,
        req.location_anomaly or False,
        behavior_flags
    )

    # Step 4: Calculate final risk score
    risk_data = compute_final_score(semantic_score, context_score)
    final_score = risk_data["final_score"]
    risk_level = risk_data["risk_level"]
    should_alert = risk_data["should_alert"]

    # Step 5: Save to database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alerts 
        (message_text, semantic_score, context_score, final_score, 
         risk_level, signals, location_lat, location_lng, alert_sent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        req.message, semantic_score, context_score, final_score,
        risk_level, json.dumps(signals),
        req.location_lat, req.location_lng,
        1 if should_alert else 0
    ))
    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()

    # Step 6: Send alerts if high risk
    alert_results = []
    if should_alert:
        conn = get_connection()
        contacts = conn.execute("SELECT * FROM trusted_contacts").fetchall()
        conn.close()
        
        for contact in contacts:
            result = send_sms_alert(
                contact["phone"], contact["name"],
                req.user_name, risk_level, signals,
                req.location_lat, req.location_lng
            )
            alert_results.append({
                "contact": contact["name"], 
                "sent": result,
                "phone": contact["phone"]
            })

    # Step 7: Return response
    return {
        "alert_id": alert_id,
        "semantic_score": semantic_score,
        "context_score": context_score,
        "final_score": final_score,
        "risk_level": risk_level,
        "signals": signals,
        "hidden_distress_reason": ai_result.get("hidden_distress_reason"),
        "confidence": ai_result.get("confidence", "low"),
        "recommended_action": ai_result.get("recommended_action", "monitor"),
        "alert_triggered": should_alert,
        "alert_results": alert_results
    }