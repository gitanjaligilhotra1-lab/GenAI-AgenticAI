# Checkout API Runbook
For elevated checkout errors after a deployment:
1. Compare error rate and latency with the baseline.
2. Inspect database connection acquisition failures.
3. Correlate incident start with recent deployments.
4. If the latest deployment is the strongest correlated change, prepare a rollback.
5. Production rollback requires on-call approval.
