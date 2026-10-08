import json
from pathlib import Path
DATA=Path(__file__).parent/"data"/"ip_reputation.json"
def lookup_ip(ip):return json.loads(DATA.read_text()).get(ip,{"risk":"unknown"})
