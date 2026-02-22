# Price Optimization Skill Pack

This repository contains a Codex skill for diagnosing and reducing software and cloud spend.

## Included Skill

- `code-price-optimization`
  - 2026 standards-aligned optimization guidance
  - Compute, storage, request volume, bandwidth, and data preloading analysis
  - Country and residency-aware planning
  - Budget and company-size tailored playbooks
  - Tool-subscription controls (including Postman seat usage)
  - Correct-practice teaching checklist with anti-patterns and validation metrics

## Quick Start

1. Open `code-price-optimization/SKILL.md`.
2. Run the diagnosis script with your workload profile:

```bash
python3 code-price-optimization/scripts/diagnose_cost_plan.py \
  --monthly-budget-usd 12000 \
  --company-size startup \
  --system-types api-saas,mobile-backend \
  --restrictions data-residency,soc2 \
  --country US \
  --monthly-requests 25000000 \
  --monthly-compute-hours 5000 \
  --monthly-egress-gb 4800 \
  --preload-ratio 0.28 \
  --postman-seats 14
```

3. Use JSON mode for automation:

```bash
python3 code-price-optimization/scripts/diagnose_cost_plan.py --format json
```

## Reference Sources

- `code-price-optimization/references/2026-standards-and-sources.md`
- `code-price-optimization/references/diagnosis-matrix.md`
- `code-price-optimization/references/correct-practices.md`
