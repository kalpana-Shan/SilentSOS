import requests
import os
import json

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def analyze_message(message: str) -> dict:
    prompt = f"""Analyze this message for emotional distress risk.
Message: "{message}"

Return JSON with:
- semantic_score (0-100, higher = more distress)
- signals (list of detected warning signs)
- hidden_distress_reason (brief explanation)

Return ONLY valid JSON, nothing else."""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=130
        )
        result = response.json()
        text = result.get("response", "{}")
        
        # Extract JSON from response
        start = text.find("{")
        end = text.rfind("}") + 1
        data = json.loads(text[start:end])
        
        return {
            "semantic_score": int(data.get("semantic_score", 50)),
            "signals": data.get("signals", []),
            "hidden_distress_reason": data.get("hidden_distress_reason", "")
        }
    except Exception as e:
        print(f"⚠️ Ollama error: {e}")
        return {
            "semantic_score": 50,
            "signals": ["analysis_failed"],
            "hidden_distress_reason": "Could not analyze message"
        }