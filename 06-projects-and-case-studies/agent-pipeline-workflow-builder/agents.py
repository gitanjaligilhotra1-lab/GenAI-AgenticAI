from tools import lookup

class Planner:
    def plan(self, task):
        names = ["postgres", "mongodb", "dynamodb"]
        requested = [name for name in names if name in task.lower()]
        return requested or ["postgres", "mongodb"]

class Researcher:
    def run(self, subject):
        return lookup(subject)

class Comparator:
    def run(self, rows):
        if not rows:
            return "Comparison unavailable: no evidence was collected."
        return "Comparison:\n" + "\n".join(
            "- %(name)s: %(strength)s; trade-off: %(tradeoff)s" % row for row in rows
        )

class Critic:
    def run(self, comparison):
        if comparison.startswith("Comparison unavailable"):
            return "Critic: insufficient evidence; do not recommend an option."
        return "Critic: recommendation should be tied to workload requirements; the comparison alone is not enough to choose a winner."
