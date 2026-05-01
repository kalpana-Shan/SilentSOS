# test_risk.py
from services.risk_engine import compute_final_score

tests = [
    {"semantic_score": 75, "hour": 23, "unusual_location": True,  "message": "worry pannadhe charge kammi"},
    {"semantic_score": 75, "hour": 14, "unusual_location": False, "message": "worry pannadhe"},
    {"semantic_score": 15, "hour": 14, "unusual_location": False, "message": "coming home for dinner"},
    {"semantic_score": 90, "hour": 23, "unusual_location": True,  "message": "dont call me everything is fine"},
]

for t in tests:
    r = compute_final_score(**t)
    print(f"Semantic: {t['semantic_score']} | Bonus: {r['context_bonus']} | Final: {r['final_score']} | Level: {r['risk_level']}")
    print(f"  Reasons: {r['context_reasons']}")
    print()