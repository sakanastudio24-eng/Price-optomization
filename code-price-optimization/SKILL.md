---
name: code-price-optimization
description: Diagnose and optimize software, cloud, and API spend using 2026 FinOps and cloud cost standards. Use when users ask for price optimization, compute/storage/request/bandwidth tuning, data preloading controls, country or region placement tradeoffs, budget planning, company-size playbooks, tool subscription controls (for example Postman seats), or cost-risk guardrails.
---

# Code Price Optimization

## Overview

Use this skill to produce a defensible cost diagnosis and a prioritized optimization plan. Focus on unit economics, request and bandwidth efficiency, compute sizing, preloading behavior, and regional constraints.

## Workflow

1. Collect an optimization profile.
- Budget: monthly spend ceiling in USD.
- Company size: solo, startup, SMB, mid-market, enterprise.
- System types: API SaaS, ecommerce, mobile backend, data platform, ML batch, edge/IoT, internal tools.
- Restrictions: data residency, PCI, HIPAA, SOC 2, FedRAMP, low latency, multi-cloud.
- Usage signals: monthly requests, compute hours, storage GB, egress GB, preloading ratio, Postman seats.
- Country and regions where users/data must stay.

2. Run the diagnostic script.
- Use `scripts/diagnose_cost_plan.py` with available inputs.
- Generate text for direct use or JSON for automation.

3. Map diagnosis to playbooks.
- Use `references/diagnosis-matrix.md` for budget and company-size action patterns.
- Apply system-type and restriction modifiers from the same file.

4. Validate recommendations against standards.
- Use `references/2026-standards-and-sources.md` for primary-source guidance.
- Re-check provider pricing pages for current rates before final numbers.

5. Deliver a plan with ranked actions and a 90-day sequence.
- Include explicit unit metrics (`cost/1M requests`, `cost/active user`, `egress/request`).
- Include tradeoffs and expected impact for each recommendation.

## Commands

Basic diagnosis:

```bash
python3 scripts/diagnose_cost_plan.py \
  --monthly-budget-usd 18000 \
  --company-size startup \
  --system-types api-saas,mobile-backend \
  --restrictions data-residency,soc2 \
  --country DE \
  --clouds aws,gcp \
  --monthly-requests 38000000 \
  --monthly-compute-hours 7400 \
  --monthly-storage-gb 3200 \
  --monthly-egress-gb 9100 \
  --preload-ratio 0.34 \
  --postman-seats 22
```

Automation-friendly JSON:

```bash
python3 scripts/diagnose_cost_plan.py \
  --company-size smb \
  --system-types ecommerce \
  --monthly-budget-usd 45000 \
  --monthly-requests 92000000 \
  --monthly-compute-hours 12800 \
  --monthly-egress-gb 14000 \
  --country US \
  --format json
```

## Output Requirements

Always provide:

1. Diagnosis summary with current pressure points.
2. Ranked action list with reason and expected direction of savings.
3. 90-day rollout plan split into immediate, medium, and follow-up actions.
4. Country or residency impacts when region placement is constrained.
5. Source-backed rationale for standards and platform guidance.

## References

- 2026 standards and official sources: `references/2026-standards-and-sources.md`
- Budget, company-size, system-type, and restriction playbooks: `references/diagnosis-matrix.md`
