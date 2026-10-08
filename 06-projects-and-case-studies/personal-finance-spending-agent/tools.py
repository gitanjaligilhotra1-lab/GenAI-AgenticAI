import json
from pathlib import Path
D=Path(__file__).parent/"data"
def transactions():return json.loads((D/"transactions.json").read_text())
def monthly_income():return 6200.0
