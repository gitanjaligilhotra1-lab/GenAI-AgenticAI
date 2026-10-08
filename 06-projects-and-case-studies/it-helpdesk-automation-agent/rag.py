import json
import re
from pathlib import Path
DATA = Path(__file__).parent / "data" / "knowledge.json"
def search_kb(query):
    items = json.loads(DATA.read_text(encoding="utf-8"))
    words = set(re.findall(r"[a-z]+", query.lower()))
    ranked = sorted(items, key=lambda item: len(words & set(re.findall(r"[a-z]+", (item["title"] + " " + item["keywords"]).lower()))), reverse=True)
    if not ranked:
        return None
    best = ranked[0]
    score = len(words & set(re.findall(r"[a-z]+", (best["title"] + " " + best["keywords"]).lower())))
    return best if score else None
