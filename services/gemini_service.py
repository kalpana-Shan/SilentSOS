import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        _client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized")
    return _client

MODEL_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
]

SYSTEM_PROMPT = """You are a silent distress detection AI for SilentSOS.

Analyze if the sender might be in danger or under coercion.

Look for these signals:
- Excessive reassurance ("don't worry", "I'm fine", "worry pannadhe", "tension padathe")
- Communication restrictions ("phone off", "can't call", "battery low", "charge kammi", "going offline")
- Exit-blocking phrases ("I'll stay here", "can't leave", "don't come")
- Unusual phrasing for a routine message
- Distancing from family or friends

Return ONLY a valid JSON object. No markdown, no explanation, no extra text outside JSON.

Schema:
{
  "semantic_score": <integer 0-100>,
  "signals": ["list of detected signal phrases"],
  "hidden_distress_reason": "<one sentence or null>",
  "confidence": "<low | medium | high>",
  "recommended_action": "<monitor | alert_contacts | emergency>"
}"""


def analyze_message(message: str) -> dict:
    last_error = None

    for model in MODEL_CHAIN:
        try:
            print(f"🤖 Trying model: {model}")
            response = get_client().models.generate_content(
                model=model,
                contents=f'Analyze this message for hidden distress: "{message}"',
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.1,
                    response_mime_type="application/json",
                )
            )
            result = json.loads(response.text)
            print(f"✅ Success with {model}")
            return {
                "semantic_score": int(result.get("semantic_score", 0)),
                "signals": result.get("signals", []),
                "hidden_distress_reason": result.get("hidden_distress_reason"),
                "confidence": result.get("confidence", "low"),
                "recommended_action": result.get("recommended_action", "monitor"),
                "model_used": model
            }

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"⚠️ {model} quota exhausted, trying next...")
                last_error = e
                time.sleep(1)
                continue
            else:
                print(f"❌ {model} failed with non-quota error: {e}")
                last_error = e
                break

    print(f"⚠️ All models exhausted. Using keyword fallback. Last error: {last_error}")
    return fallback_analysis(message)


def fallback_analysis(message: str) -> dict:
    message_lower = message.lower()
    score = 0
    signals = []

    reassurance = ["worry", "don't worry", "i'm fine", "be fine",
                   "worry pannadhe", "pannadhe", "tension padathe"]
    if any(w in message_lower for w in reassurance):
        score += 30
        signals.append("excessive reassurance")

    communication = ["battery low", "phone off", "charge kammi", "kammi",
                     "can't call", "won't call", "going offline", "no signal"]
    if any(w in message_lower for w in communication):
        score += 35
        signals.append("communication restriction")

    distancing = ["late", "don't come", "don't wait", "varuven",
                  "will be late", "stay there", "won't be home"]
    if any(w in message_lower for w in distancing):
        score += 20
        signals.append("distancing language")

    exit_blocking = ["can't leave", "stuck here", "they won't let",
                     "not allowed", "have to stay"]
    if any(w in message_lower for w in exit_blocking):
        score += 40
        signals.append("exit-blocking language")

    final_score = min(score, 100)

    if final_score >= 70:
        action = "emergency"
    elif final_score >= 40:
        action = "alert_contacts"
    else:
        action = "monitor"

    return {
        "semantic_score": final_score,
        "signals": signals,
        "hidden_distress_reason": " | ".join(signals) if signals else None,
        "confidence": "medium" if signals else "low",
        "recommended_action": action,
        "model_used": "keyword_fallback"
    }