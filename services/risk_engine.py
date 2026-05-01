from datetime import datetime

def compute_context_score(time_str: str, location_anomaly: bool, behavior_flags: dict) -> int:
    """Calculate context risk score (0-100)"""
    score = 0

    # Time anomaly — late night or early morning
    if time_str:
        try:
            hour = datetime.fromisoformat(time_str).hour
            if 22 <= hour or hour <= 5:
                score += 35  # Late night/early morning = high risk
            elif 20 <= hour <= 21:
                score += 15
        except:
            pass

    # Location anomaly
    if location_anomaly:
        score += 30

    # Behavior flags
    if behavior_flags.get("unusual_reassurance"):
        score += 20
    if behavior_flags.get("communication_restriction"):
        score += 25
    if behavior_flags.get("repeat_pattern"):
        score += 15

    return min(score, 100)

def compute_final_score(semantic_score: int, context_score: int) -> dict:
    """Fuse semantic AI score with contextual signals"""
    # Weighted formula: 55% semantic (AI), 45% context (behavioral)
    final = int(0.55 * semantic_score + 0.45 * context_score)
    final = min(final, 100)

    # Risk level thresholds
    if final >= 70:
        risk_level = "high"
    elif final >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "final_score": final,
        "risk_level": risk_level,
        "should_alert": final >= 70
    }

def extract_behavior_flags(message: str, signals: list) -> dict:
    """Extract behavioral patterns from message"""
    message_lower = message.lower()
    flags = {}

    reassurance_words = ["don't worry", "i'm fine", "everything ok", "be fine", "worry pannadhe", "naan fine"]
    flags["unusual_reassurance"] = any(w in message_lower for w in reassurance_words)

    restriction_words = ["phone off", "battery low", "won't call", "can't talk", "charge kammi"]
    flags["communication_restriction"] = any(w in message_lower for w in restriction_words)

    flags["repeat_pattern"] = len(signals) >= 3

    return flags