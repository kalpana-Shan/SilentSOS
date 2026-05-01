import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are a silent distress detection AI for SilentSOS.

Analyze if the sender might be in danger or under coercion.

Look for:
- Excessive reassurance ("don't worry", "I'm fine")
- Communication restrictions ("phone off", "can't call")
- Exit-blocking phrases ("I'll stay here", "can't leave")
- Distancing from family/friends

Return ONLY JSON:
{
  "semantic_score": 0-100,
  "signals": ["cue1", "cue2"],
  "hidden_distress_reason": "explanation or null",
  "confidence": "low|medium|high",
  "recommended_action": "monitor|alert_contacts|emergency"
}

Score 0-39: normal | 40-69: suspicious | 70-100: distress
"""

def analyze_message(message: str) -> dict:
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nMessage: \"{message}\""
        response = model.generate_content(prompt)
        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        return json.loads(raw.strip())
    except Exception as e:
        return {
            "semantic_score": 0,
            "signals": [],
            "hidden_distress_reason": None,
            "confidence": "low",
            "recommended_action": "monitor",
            "error": str(e)
        }