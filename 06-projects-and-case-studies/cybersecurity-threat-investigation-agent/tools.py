import json
from pathlib import Path
D=Path(__file__).parent/"data"
def load(n):return json.loads((D/n).read_text())
def get_alert(i):return load("alerts.json").get(i)
def get_auth_events(user):return [e for e in load("auth_events.json") if e["user"]==user]
def get_device(i):return load("devices.json").get(i)
