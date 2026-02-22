# Correct Practices

Use this checklist to teach good cost-optimization behavior, not just produce savings tips.

## 1. Cost Observability

Do:
- Track `cost/1M requests`, `cost/active user`, and `egress/1K requests`.
- Enforce tag/label standards across all environments.
- Review anomaly alerts weekly with clear owners.

Avoid:
- Reviewing only total monthly bill.
- Letting shared resources remain unowned.
- Optimizing without baseline unit metrics.

Measure:
- Percent tagged spend.
- Budget variance by workload.
- Time to detect and fix anomalies.

## 2. Compute And Runtime

Do:
- Right-size instances and keep autoscaling enabled.
- Shut down non-prod workloads off-hours.
- Use commitments only for stable, measured baseline usage.

Avoid:
- Buying long commitments before utilization stabilizes.
- Keeping high baseline capacity for rare spikes.
- Mixing burst and steady-state assumptions in one sizing model.

Measure:
- Requests per compute hour.
- Idle compute percentage.
- Commitment coverage and unused commitment rate.

## 3. Request, Preloading, And API Efficiency

Do:
- Cache high-read endpoints and define TTL/invalidations.
- Replace eager preloading with demand-driven fetch when hit-rate is low.
- Set retry budgets and idempotency for expensive operations.

Avoid:
- Chatty APIs and overfetching full payloads.
- Unlimited retries from clients.
- Preloading low-hit datasets by default.

Measure:
- Preload hit-rate.
- Requests per user journey.
- Cache hit ratio on top endpoints.

## 4. Bandwidth And Data Transfer

Do:
- Put static and cacheable responses behind CDN.
- Compress responses and trim unused fields.
- Keep traffic in-region when compliance allows.

Avoid:
- Cross-region reads by default.
- Serving uncompressed payloads at scale.
- Ignoring egress in architecture decisions.

Measure:
- Egress MB per 1K requests.
- Cross-region transfer share.
- CDN offload rate.

## 5. Storage And Data Platform

Do:
- Apply retention and lifecycle policies.
- Partition/prune analytical datasets.
- Tier cold data to cheaper classes.

Avoid:
- Infinite retention for low-value logs/events.
- Full-table scans as normal behavior.
- Mixing critical and non-critical data tiers blindly.

Measure:
- Storage growth rate.
- Query scanned bytes per report/job.
- Cost share of cold vs hot storage.

## 6. Tool Subscriptions And Seats

Do:
- Audit seat usage monthly.
- Keep paid seats for active producers/owners.
- Consolidate duplicate workspaces where governance permits.

Avoid:
- Paying for inactive seats.
- Duplicate tools for the same workflow.
- Permanent premium plans without usage review.

Measure:
- Active-to-paid seat ratio.
- Cost per active contributor.
- Unused workspace count.

## 7. Governance, Compliance, And Country Constraints

Do:
- Place data-plane workloads in allowed regions first.
- Document policy boundaries before choosing the cheapest region.
- Keep auditable change logs for cost controls.

Avoid:
- Region choices that violate residency requirements.
- Cost-only decisions that break PCI/HIPAA/FedRAMP controls.
- Untracked exceptions to spend policies.

Measure:
- Policy exception count.
- Remediation time for non-compliant deployments.
- Compliance control coverage for cost-critical services.
