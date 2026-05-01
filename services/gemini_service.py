import json
from ollama import Client

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Client(host="http://localhost:11434")
        print("✅ Ollama client initialized")
    return _client

SYSTEM_PROMPT = """You are a silent distress detection AI for SilentSOS.

Analyze if the sender might be in danger or under coercion.

Look for these signals:
- Excessive reassurance ("don't worry", "I'm fine", "worry pannadhe", "tension padathe")
- Communication restrictions ("phone off", "can't call", "battery low", "charge kammi", "going offline")
- Exit-blocking phrases ("I'll stay here", "can't leave", "don't come")
- Unusual phrasing for a routine message
- Distancing from family or friends

Return ONLY a valid JSON object. No markdown, no extra text.

Schema:
{
  "semantic_score": <integer 0-100>,
  "signals": ["list of detected signal phrases"],
  "hidden_distress_reason": "<one sentence or null>",
  "confidence": "<low | medium | high>",
  "recommended_action": "<monitor | alert_contacts | emergency>"
}"""


def analyze_message(message: str) -> dict:
    try:
        print("🤖 Calling Ollama llama3.2...")
        response = get_client().chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f'Analyze this message for hidden distress: "{message}"'}
            ],
            format="json",
            options={"temperature": 0.1}
        )
        result = json.loads(response.message.content)
        print("✅ Ollama analysis success")
        return {
            "semantic_score": int(result.get("semantic_score", 0)),
            "signals": result.get("signals", []),
            "hidden_distress_reason": result.get("hidden_distress_reason"),
            "confidence": result.get("confidence", "low"),
            "recommended_action": result.get("recommended_action", "monitor"),
            "model_used": "ollama/llama3.2"
        }
    except Exception as e:
        print(f"❌ Ollama failed: {e}")
        return fallback_analysis(message)


def fallback_analysis(message: str) -> dict:
    message_lower = message.lower()
    score = 0
    signals = []

    if any(w in message_lower for w in ["worry", "don't worry", "i'm fine", "worry pannadhe", "pannadhe"]):
        score += 30
        signals.append("excessive reassurance")

    if any(w in message_lower for w in ["battery low", "phone off", "charge kammi", "can't call", "going offline"]):
        score += 35
        signals.append("communication restriction")

    if any(w in message_lower for w in ["don't come", "don't wait", "will be late", "stay there"]):
        score += 20
        signals.append("distancing language")

    if any(w in message_lower for w in ["can't leave", "stuck here", "they won't let", "not allowed"]):
        score += 40
        signals.append("exit-blocking language")

    final_score = min(score, 100)
    return {
        "semantic_score": final_score,
        "signals": signals,
        "hidden_distress_reason": " | ".join(signals) if signals else None,
        "confidence": "medium" if signals else "low",
        "recommended_action": "emergency" if final_score >= 70 else "alert_contacts" if final_score >= 40 else "monitor",
        "model_used": "keyword_fallback"
    }