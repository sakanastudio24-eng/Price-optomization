# 2026 Standards And Source Set

Last checked: 2026-02-22

Use this file as the baseline source set before giving any recommendation that can change over time.

## Core Standards And Frameworks

1. FinOps Framework (operating model for cloud cost management)
- https://www.finops.org/framework/

2. FinOps Open Cost and Usage Specification (FOCUS)
- https://focus.finops.org/

3. AWS Cost Optimization guidance
- https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html

4. Google Cloud Architecture Framework: cost optimization
- https://cloud.google.com/architecture/framework/cost-optimization

5. Azure Well-Architected: cost optimization
- https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/

## Billing Data And Cost Telemetry Sources

1. AWS Cost and Usage Reports (CUR)
- https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html

2. Google Cloud Billing export to BigQuery
- https://cloud.google.com/billing/docs/how-to/export-data-bigquery

3. Azure Cost Management + Billing docs hub
- https://learn.microsoft.com/en-us/azure/cost-management-billing/

## Commitment And Discount Instruments

1. AWS Savings Plans
- https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html

2. Azure Reservations
- https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations

3. Google Cloud committed use discounts
- https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview

## Pricing Calculators And Subscription Inputs

1. AWS Pricing Calculator
- https://calculator.aws/

2. Azure Pricing Calculator
- https://azure.microsoft.com/en-us/pricing/calculator/

3. Google Cloud Pricing Calculator
- https://cloud.google.com/products/calculator

4. Postman pricing plans
- https://www.postman.com/pricing/

## Country And Region Planning Sources

1. AWS Regions and availability zones
- https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html

2. Azure geographies and regions
- https://learn.microsoft.com/en-us/azure/reliability/regions-list

3. Google Cloud regions and zones
- https://cloud.google.com/compute/docs/regions-zones

4. Google Cloud data residency controls (Assured Workloads)
- https://cloud.google.com/assured-workloads/docs/data-residency

## 2026 Recommendation Baseline

Treat these as the default optimization standard:

1. Normalize multi-cloud cost data into a FOCUS-compatible model.
2. Run weekly unit-cost review for at least three metrics:
- Cost per 1M requests
- Cost per active user
- Egress per 1K requests
3. Enable budget alerting and anomaly detection in each provider account/subscription/project.
4. Block untagged production resources from deployment unless exempted.
5. Purchase commitments only after at least 4-8 weeks of stable baseline utilization.
6. Tie country and residency requirements to workload placement before tuning compute.
7. Review high-seat tooling subscriptions quarterly against active usage.

Note: Pricing and policies can change at any time. Always confirm current terms on the source URLs above before final cost estimates.
