import json
from pathlib import Path
DATA=Path(__file__).parent/"data"/"options.json"
def lookup(name):return json.loads(DATA.read_text())[name]
