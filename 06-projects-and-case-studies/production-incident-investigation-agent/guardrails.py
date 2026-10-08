ALLOWED_RECOMMENDATIONS={"rollback","scale","investigate_dependency","observe"}
def recommendation_is_safe(action): return action in ALLOWED_RECOMMENDATIONS
def execution_policy(): return "This reference agent recommends production actions; it does not execute them."
