from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.gemini_service import analyze_message
from services.risk_engine import compute_final_score
from services.alert_service import trigger_alert
from database import get_db
from datetime import datetime
import json

router = APIRouter()


class MessageRequest(BaseModel):
    message: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    unusual_location: bool = False


@router.post("/analyze-message")
def analyze(req: MessageRequest):

    # Step 1: AI distress analysis
    ai_result = analyze_message(req.message)

    # Step 2: Context risk scoring
    risk = compute_final_score(
        semantic_score=ai_result["semantic_score"],
        hour=datetime.now().hour,
        unusual_location=req.unusual_location,
        message=req.message
    )

    # Step 3: Build final response
    final_result = {
        **ai_result,
        "final_score":    risk["final_score"],
        "risk_level":     risk["risk_level"],
        "context_bonus":  risk["context_bonus"],
        "context_reasons": risk["context_reasons"],
        "lat": req.lat,
        "lng": req.lng,
        "alert_sent": False,
        "alert_channels": ""
    }

    # Step 4: Save to DB
    alert_id = None
    try:
        conn = get_db()
        cursor = conn.execute("""
            INSERT INTO alerts (
                message_text, semantic_score, context_bonus, final_score,
                risk_level, signals, explanation, lat, lng,
                unusual_location, alert_sent, alert_channels
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, '')
        """, (
            req.message,
            ai_result["semantic_score"],
            risk["context_bonus"],
            risk["final_score"],
            risk["risk_level"],
            json.dumps(ai_result["signals"]),
            ai_result.get("hidden_distress_reason", ""),
            req.lat,
            req.lng,
            int(req.unusual_location),
        ))
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"💾 Alert saved to DB — ID {alert_id}")
    except Exception as e:
        print(f"⚠️ DB save failed: {e}")

    # Step 5: Trigger alert if medium or high risk
    if risk["risk_level"] in ("high", "medium") and risk["final_score"] >= 60:
        try:
            alert_sent = trigger_alert(final_result)
            final_result["alert_sent"] = alert_sent
            final_result["alert_channels"] = "email" if alert_sent else "demo_log"

            # Update DB row with sent status
            if alert_id:
                conn = get_db()
                conn.execute(
                    "UPDATE alerts SET alert_sent = ?, alert_channels = ? WHERE id = ?",
                    (1 if alert_sent else 0, final_result["alert_channels"], alert_id)
                )
                conn.commit()
                conn.close()

        except Exception as e:
            print(f"⚠️ Alert trigger failed: {e}")

    return final_result