import re
from datetime import datetime, timezone
from guardrails import execution_policy,recommendation_is_safe
from rag import search_runbook
from tools import get_incident,get_logs,get_metrics,get_recent_deployments

class IncidentInvestigationAgent:
    def chat(self,message):
        incident_id=self._incident_id(message)
        if not incident_id: return "Provide an incident ID, for example: Investigate INC-1001."
        incident=get_incident(incident_id)
        if not incident: return "I could not find "+incident_id+"."
        service=incident["service"]; metrics=get_metrics(service); logs=get_logs(service); deployments=get_recent_deployments(service)
        runbook=search_runbook(service+" "+incident["symptom"]); findings=[]; recommendation="observe"; confidence="low"
        if metrics.get("error_rate",0)>=5: findings.append("Error rate is %.1f%%."%metrics["error_rate"])
        if metrics.get("p95_ms",0)>metrics.get("baseline_p95_ms",0)*2: findings.append("p95 latency rose from %d ms to %d ms."%(metrics["baseline_p95_ms"],metrics["p95_ms"]))
        errors=[x for x in logs if x["level"]=="ERROR"]
        if errors: findings.append("Error evidence: "+errors[0]["message"])
        recent=self._most_recent_prior_deployment(incident,deployments)
        if recent:
            findings.append("Deployment %s occurred %d minutes before incident start."%(recent["version"],recent["minutes_before_incident"]))
            if recent.get("risk")=="database_pool" and "pool" in " ".join(x["message"].lower() for x in errors): recommendation="rollback"; confidence="high"
        if "timeout" in " ".join(x["message"].lower() for x in errors) and recommendation=="observe": recommendation="investigate_dependency"; confidence="medium"
        if not recommendation_is_safe(recommendation): recommendation="observe"; confidence="low"
        labels={"rollback":"Prepare rollback of the latest deployment and request on-call approval.","investigate_dependency":"Investigate the failing dependency and connection health before changing the caller.","scale":"Review capacity and scale only after confirming saturation.","observe":"Continue investigation before changing production."}
        cause="Insufficient evidence for a confident root-cause hypothesis."
        if recommendation=="rollback": cause="A recent database-pool configuration deployment aligns with the incident timing and connection-pool errors."
        elif recommendation=="investigate_dependency": cause="Dependency timeout errors are the strongest current signal; the older low-risk deployment is weak evidence."
        lines=["Incident: "+incident_id,"Service: "+service,"Severity: "+incident["severity"],"","Evidence:"]+["- "+x for x in findings] or ["- No strong signal found."]
        lines += ["","Hypothesis:",cause,"Confidence: "+confidence.upper(),"","Recommended next step:",labels[recommendation],"","Runbook: "+(runbook["source"] if runbook else "No matching runbook"),"Safety: "+execution_policy()]
        return "\n".join(lines)

    @staticmethod
    def _most_recent_prior_deployment(incident,deployments):
        start=datetime.fromisoformat(incident["started_at"].replace("Z","+00:00"))
        candidates=[]
        for d in deployments:
            deployed=datetime.fromisoformat(d["deployed_at"].replace("Z","+00:00"))
            if deployed<=start:
                item=dict(d); item["minutes_before_incident"]=int((start-deployed).total_seconds()//60); candidates.append(item)
        return min(candidates,key=lambda x:x["minutes_before_incident"]) if candidates else None

    @staticmethod
    def _incident_id(message):
        m=re.search(r"INC-\d+",message.upper()); return m.group(0) if m else None
