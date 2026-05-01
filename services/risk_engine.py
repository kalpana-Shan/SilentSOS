from datetime import datetime


def compute_final_score(
    semantic_score: int,
    hour: int = None,
    unusual_location: bool = False,
    message: str = ""
) -> dict:

    context_bonus = 0
    context_reasons = []

    if hour is None:
        hour = datetime.now().hour

    # Late night / early morning (10 PM – 5 AM)
    if hour >= 22 or hour <= 5:
        context_bonus += 15
        context_reasons.append("late-night message")

    # Unusual location
    if unusual_location:
        context_bonus += 15
        context_reasons.append("unusual location detected")

    # Excessive reassurance pattern
    reassurance_words = [
        "don't worry", "i'm fine", "worry pannadhe",
        "tension padathe", "everything is fine", "i'm okay",
        "be fine", "pannadhe", "bayapadathe", "periya vishayam illa"
    ]
    if any(w in message.lower() for w in reassurance_words):
        context_bonus += 10
        context_reasons.append("excessive reassurance pattern")

    # Communication restriction pattern
    comm_words = [
        "charge kammi", "battery low", "phone off",
        "can't call", "going offline", "won't reply",
        "call pannala", "pesa mudiyathu"
    ]
    if any(w in message.lower() for w in comm_words):
        context_bonus += 10
        context_reasons.append("communication restriction pattern")

    # Isolation / exit-limiting language
    isolation_words = [
        "don't come", "stay there", "i'll manage",
        "no need to come", "varadheenga", "varaadhey"
    ]
    if any(w in message.lower() for w in isolation_words):
        context_bonus += 10
        context_reasons.append("isolation or exit-limiting phrase")

    # ── Scoring formula ──────────────────────────────────────
    # semantic carries 70%, context carries 60%, base offset 10
    # Both high semantic AND high context = reliably HIGH risk
    final_score = min(100, int(
        (semantic_score * 0.70) +
        (context_bonus  * 0.60) +
        10
    ))

    # Risk thresholds
    if final_score >= 70:
        risk_level = "high"
    elif final_score >= 45:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "semantic_score":   semantic_score,
        "context_bonus":    context_bonus,
        "context_reasons":  context_reasons,
        "final_score":      final_score,
        "risk_level":       risk_level
    }