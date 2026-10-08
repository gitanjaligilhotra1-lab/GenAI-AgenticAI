# Dependency Timeout Runbook
For repeated dependency timeouts:
1. Confirm the affected dependency.
2. Check whether latency and error rate increased together.
3. Check dependency health before scaling the caller.
4. Avoid unbounded retries.
5. Escalate production-changing actions to the on-call engineer.
