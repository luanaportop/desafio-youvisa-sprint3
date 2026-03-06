import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("backend/src/nlp/ai_governance_log.json")

def log_ai_interaction(user_input: str, ai_response: str, model: str = "gemini"):
    record = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "user_input": user_input,
        "ai_response": ai_response
    }

    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)