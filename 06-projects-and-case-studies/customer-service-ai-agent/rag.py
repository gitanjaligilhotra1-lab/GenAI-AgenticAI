from pathlib import Path
import re

POLICY_DIR = Path(__file__).parent / "data" / "policies"

def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def search_policy(question):
    query = _tokens(question)
    best = None
    for path in POLICY_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        score = len(query & _tokens(text))
        if best is None or score > best["score"]:
            best = {"score": score, "text": text.strip(), "source": path.name}
    return best if best and best["score"] > 0 else None
