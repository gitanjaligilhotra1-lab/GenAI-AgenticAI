from pathlib import Path
import re
ROOT=Path(__file__).parent/"data"/"policies"
def words(s): return set(re.findall(r"[a-z0-9]+",s.lower()))
def search_policy(q):
    best=None
    for p in ROOT.glob("*.md"):
        t=p.read_text(encoding="utf-8"); score=len(words(q)&words(t))
        if best is None or score>best["score"]: best={"score":score,"source":p.name,"text":t.strip()}
    return best if best and best["score"] else None
