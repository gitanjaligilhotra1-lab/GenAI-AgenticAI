from agents import Planner, Researcher, Comparator, Critic

class Pipeline:
    def run(self, task):
        plan = Planner().plan(task)
        state = {"task": task, "plan": plan, "research": [], "errors": []}
        researcher = Researcher()
        for subject in plan:
            try:
                result = researcher.run(subject)
                if not result or not all(key in result for key in ("name", "strength", "tradeoff")):
                    raise ValueError("Missing or incomplete evidence")
                state["research"].append(result)
            except (KeyError, ValueError, OSError) as exc:
                state["errors"].append(subject + ": " + str(exc))
        state["comparison"] = Comparator().run(state["research"])
        state["review"] = Critic().run(state["comparison"])
        sections = ["Plan: " + ", ".join(plan), "", state["comparison"], "", state["review"]]
        if state["errors"]:
            sections.extend(["", "Evidence gaps:", *["- " + error for error in state["errors"]]])
        return "\n".join(sections)
