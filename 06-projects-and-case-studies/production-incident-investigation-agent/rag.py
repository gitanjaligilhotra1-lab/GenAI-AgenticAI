from pathlib import Path
import re
RUNBOOK_DIR=Path(__file__).parent/"data"/"runbooks"
def _tokens(text): return set(re.findall(r"[a-z0-9]+",text.lower()))
def search_runbook(query):
    words=_tokens(query); best=None
    for path in RUNBOOK_DIR.glob("*.md"):
        text=path.read_text(encoding="utf-8"); score=len(words&_tokens(text))
        if best is None or score>best["score"]: best={"score":score,"source":path.name,"text":text.strip()}
    return best if best and best["score"] else None
