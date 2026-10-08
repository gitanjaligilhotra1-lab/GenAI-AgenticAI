from tools import project_data

class ProjectStatusAssistant:
    def answer(self, question):
        data = project_data()
        text = question.lower().strip()
        tasks = data["tasks"]
        blocked = [task for task in tasks if task["status"] == "blocked"]
        latency = data.get("p95_ms")
        target = data.get("target_p95_ms")
        metrics_available = isinstance(latency, (int, float)) and isinstance(target, (int, float)) and target > 0
        latency_exceeded = metrics_available and latency >= target
        if "block" in text:
            if not blocked:
                return "No blocked tasks are recorded in this snapshot."
            return "\n".join("- " + task["name"] + ": " + task.get("reason", "Reason not recorded") for task in blocked)
        if "changed" in text or "update" in text:
            return "\n".join("- " + change for change in data["changes"]) if data["changes"] else "No recent changes are recorded in this snapshot."
        if text not in {"status", "summary", "overview", ""}:
            return "Try: status, blockers, or what changed."
        done = sum(task["status"] == "done" for task in tasks)
        risk = "AT RISK" if blocked or latency_exceeded else ("UNKNOWN / NEEDS REVIEW" if not metrics_available or not tasks else "ON TRACK")
        reasons = []
        if blocked:
            reasons.append(str(len(blocked)) + " blocked task(s)")
        if not metrics_available:
            reasons.append("required latency evidence missing or invalid")
        if not tasks:
            reasons.append("task evidence missing")
        if latency_exceeded:
            reasons.append("p95 latency exceeds target by " + str(data["p95_ms"] - data["target_p95_ms"]) + " ms")
        return "\n".join([
            "Project: " + data["project"],
            "Status: " + risk,
            "Completed: " + str(done) + "/" + str(len(tasks)) + " tasks",
            "Blockers: " + str(len(blocked)),
            "p95 latency: " + (str(latency) + " ms (target <" + str(target) + " ms)" if metrics_available else "UNKNOWN (required evidence unavailable)"),
            "Next milestone: " + data["milestone"],
            "Assessment basis: " + ("; ".join(reasons) if reasons else "No blocked tasks or latency breach in this snapshot"),
            "Source: local project.json snapshot; not a live project-system update."
        ])
