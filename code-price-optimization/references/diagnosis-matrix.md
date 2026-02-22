# Diagnosis Matrix

Use this matrix after running the script to tailor recommendations.

## Budget Tiers (Monthly)

1. Micro: under $2k
- Prioritize serverless and managed services.
- Avoid premature multi-region active/active.
- Cap non-essential seats and duplicate tools.

2. Startup: $2k-$20k
- Enforce unit economics from day one.
- Use autoscaling plus aggressive idle shutdown.
- Add CDN and response compression early.

3. Growth: $20k-$150k
- Establish formal FinOps cadence.
- Introduce commitment instruments for stable baselines.
- Split shared and customer-facing workloads for clearer chargeback.

4. Enterprise: over $150k
- Run platform-level commitment portfolio management.
- Add BU-level chargeback and showback.
- Build policy-as-code for spend guardrails and exception workflows.

## Company Size Playbook

1. Solo or Small Team
- Keep stack simple and managed.
- Limit paid seats to active users only.
- Instrument only high-value telemetry to avoid log over-spend.

2. SMB
- Add monthly optimization review and owners per cost domain.
- Standardize environments and shut down non-prod after hours.
- Require business case for high-cost add-ons.

3. Mid-Market and Enterprise
- Define service-level unit metrics and cost SLOs.
- Assign budget owners by product line.
- Audit commitment coverage and unused reservations monthly.

## System Type Modifiers

1. API SaaS
- Focus on request efficiency, cache hit rates, and read/write split.
- Add request tiering and retry budgets.

2. Ecommerce
- Protect peak traffic with autoscaling guardrails.
- Optimize image delivery and edge caching first.

3. Mobile Backend
- Reduce chatty APIs and overfetching.
- Tune push, polling, and fanout patterns.

4. Data Platform
- Enforce partitioning, pruning, and lifecycle policies.
- Move cold datasets to lower-cost storage tiers.

5. ML Batch
- Right-size training clusters and schedule off-peak jobs.
- Separate experiment and production budgets.

6. Edge/IoT
- Batch ingest where latency allows.
- Compress payloads before transport.

## Restriction Modifiers

1. Data Residency
- Place data-plane services in compliant regions first.
- Keep control plane separated when needed.

2. PCI or HIPAA
- Factor compliance boundary costs before pure unit-cost optimization.
- Limit blast radius with strict network segmentation.

3. SOC 2
- Require auditable cost controls and change trails.

4. FedRAMP or Public Sector
- Account for approved-service limits and region constraints in estimates.

5. Multi-Cloud
- Use common tagging taxonomy and cost schema (FOCUS).
- Track cross-cloud egress explicitly.

6. Low Latency Global
- Optimize cache topology before adding compute in new regions.

## Country-Specific Notes

1. Country-level constraints usually affect:
- Allowed regions
- Data transfer paths
- Tax/compliance overhead

2. When country restrictions are strict:
- Prioritize in-country data persistence
- Use nearest compliant edge for static and cacheable traffic
- Recalculate egress assumptions after regional placement is fixed
