import json
from pathlib import Path
from uuid import uuid4

DATA_FILE = Path(__file__).parent / "data" / "orders.json"

def _load_orders():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def get_order(order_id):
    return _load_orders().get(order_id)

def create_replacement(order_id):
    order = get_order(order_id)
    if not order or not order["delivered"]:
        return None
    return "REPL-" + uuid4().hex[:6].upper()

def create_refund(order_id, amount):
    order = get_order(order_id)
    if not order or amount < 0 or amount > order["price"]:
        return None
    return "REF-" + uuid4().hex[:6].upper()
