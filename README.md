# OCI OOTB Budget alert gate

Built-in OCI Budgets provide actual-spend and forecast-spend alert rules. This repo
contains a Terraform configuration for that built-in workflow plus a runnable local
threshold preview. It is not another anomaly detector or a replacement forecasting engine.

## The workflow

A compartment-scoped monthly budget has two built-in email alert rules:
actual >=80% and forecast >=100%. The infrastructure declares the OCI Budget and
both rules. The local preview lets an operator check sample snapshots without a
cloud account. Rules warn humans; they do **not** stop resources or cap spending.

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
python examples/demo.py
```

Demo: a healthy snapshot fires no rule, a high forecast fires the forecast rule,
then rising actual spend fires both. Decimal arithmetic avoids float boundary drift.
Invalid amounts, non-finite amounts and unknown rule modes fail explicitly.

## Infrastructure template, not deployed

`infra/main.tf` declares `oci_budget_budget` and `oci_budget_alert_rule`. Before any
real use, an operator must review IAM, provider authentication, recipient authority,
rate-card currency, current service terms and their own plan. No credentials,
real OCIDs or email addresses are included. No apply command is run by CI.

The Python preview is tested. The Terraform configuration has not been plan/apply
validated against a tenancy. Forecast is a supplied number, not a calculated prediction.
Equality triggering is the local preview convention; delivery latency, daily evaluation,
forecast availability, rule re-notification and billing ingestion are not simulated.
No emails sent, no live OCI access, no resources created and no spend.

## Sources

Oracle Budget resource (amount is in the customer's rate-card currency):
https://docs.oracle.com/en-us/iaas/tools/terraform-provider-oci/latest/docs/r/budget_budget.html

Built-in ACTUAL / FORECAST and ABSOLUTE / PERCENTAGE alert rule fields:
https://docs.oracle.com/en-us/iaas/tools/terraform-provider-oci/latest/docs/r/budget_alert_rule.html

This demo is completely offline and free. It makes no promise that a real tenancy,
its existing workloads or alert delivery are free. Obtain approval before deployment.
