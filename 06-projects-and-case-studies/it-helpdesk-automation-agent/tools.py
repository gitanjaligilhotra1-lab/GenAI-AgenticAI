import json
from pathlib import Path
from uuid import uuid4
D=Path(__file__).parent/"data"
def device_status(device): return json.loads((D/"devices.json").read_text()).get(device)
def create_ticket(summary): return "IT-"+uuid4().hex[:6].upper()
