import json
from pathlib import Path
DATA=Path(__file__).parent/"data"
def _load(name): return json.loads((DATA/name).read_text(encoding="utf-8"))
def get_incident(incident_id): return _load("incidents.json").get(incident_id)
def get_recent_deployments(service): return [x for x in _load("deployments.json") if x["service"]==service]
def get_metrics(service): return _load("metrics.json").get(service,{})
def get_logs(service): return [x for x in _load("logs.json") if x["service"]==service]
