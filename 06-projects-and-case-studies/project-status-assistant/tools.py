import json
from pathlib import Path
DATA=Path(__file__).parent/"data"/"project.json"
def project_data():return json.loads(DATA.read_text())
