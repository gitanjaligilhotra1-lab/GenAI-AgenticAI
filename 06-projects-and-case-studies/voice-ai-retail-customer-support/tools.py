import json
from pathlib import Path
from uuid import uuid4
DATA=Path(__file__).parent/"data"/"orders.json"
def get_order(order_id): return json.loads(DATA.read_text(encoding="utf-8")).get(order_id)
def create_replacement(order_id):
    order=get_order(order_id)
    if not order or not order["delivered"]: return None
    return "REPL-"+uuid4().hex[:6].upper()
