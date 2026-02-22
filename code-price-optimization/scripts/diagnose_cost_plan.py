#!/usr/bin/env python3
"""Diagnose software/cloud spend and produce a ranked optimization plan."""

from __future__ import annotations

import argparse
import json
from typing import Dict, List, Set


EEA_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR",
    "HU", "IS", "IE", "IT", "LV", "LI", "LT", "LU", "MT", "NL", "NO", "PL",
    "PT", "RO", "SK", "SI", "ES", "SE", "UK",
}


def parse_csv_set(raw: str) -> Set[str]:
    if not raw:
        return set()
    return {part.strip().lower() for part in raw.split(",") if part.strip()}


def budget_tier(monthly_budget_usd: float) -> str:
    if monthly_budget_usd <= 0:
        return "unknown"
    if monthly_budget_usd < 2000:
        return "micro"
    if monthly_budget_usd < 20000:
        return "startup"
    if monthly_budget_usd < 150000:
        return "growth"
    return "enterprise"


def add_unique(items: List[str], additions: List[str]) -> None:
    seen = set(items)
    for addition in additions:
        if addition not in seen:
            seen.add(addition)
            items.append(addition)


def add_action(
    actions: List[Dict[str, object]],
    dedupe: Set[str],
    key: str,
    priority: int,
    title: str,
    reason: str,
    steps: List[str],
) -> None:
    if key in dedupe:
        return
    dedupe.add(key)
    actions.append(
        {
            "priority": priority,
            "title": title,
            "reason": reason,
            "steps": steps,
        }
    )


def build_actions(args: argparse.Namespace, tier: str) -> List[Dict[str, object]]:
    actions: List[Dict[str, object]] = []
    dedupe: Set[str] = set()

    add_action(
        actions,
        dedupe,
        "focus",
        10,
        "Normalize billing data with FOCUS-aligned fields",
        "Comparisons and chargeback stay noisy without a shared schema.",
        [
            "Export raw billing data from each cloud account/project/subscription daily.",
            "Map provider fields to FOCUS dimensions and enforce tag completeness.",
            "Track cost per 1M requests, cost per active user, and egress per 1K requests.",
        ],
    )

    add_action(
        actions,
        dedupe,
        "alerts",
        20,
        "Enable budget and anomaly alerts in all billing scopes",
        "Alerting catches runaway costs before end-of-month surprises.",
        [
            "Create monthly budgets per workload and environment.",
            "Add anomaly alerts for sudden request, egress, and log-ingest spikes.",
            "Route alerts to the owning team and on-call channel.",
        ],
    )

    add_action(
        actions,
        dedupe,
        "idle",
        30,
        "Eliminate idle compute and storage",
        "Idle resources are usually the fastest savings lever.",
        [
            "Shut down non-production stacks outside business hours.",
            "Right-size over-provisioned instances and databases.",
            "Apply storage lifecycle policies for cold data.",
        ],
    )

    if args.monthly_requests > 0 and args.monthly_compute_hours > 0:
        requests_per_compute_hour = args.monthly_requests / args.monthly_compute_hours
        if requests_per_compute_hour < 1500:
            add_action(
                actions,
                dedupe,
                "low-utilization",
                35,
                "Improve compute utilization",
                "Request throughput per compute hour is low for sustained workloads.",
                [
                    "Increase autoscaling aggressiveness and shrink baseline capacity.",
                    "Move burst-heavy endpoints to serverless where feasible.",
                    "Benchmark critical paths before and after rightsizing.",
                ],
            )

    if args.preload_ratio >= 0.25:
        add_action(
            actions,
            dedupe,
            "preload",
            40,
            "Reduce unnecessary data preloading",
            "High preload ratio increases compute, DB, and bandwidth costs.",
            [
                "Switch from eager preload to demand-driven fetch for low-hit datasets.",
                "Set TTL and invalidation rules for preloaded caches.",
                "Measure preload hit-rate; remove preload paths below 60% hit-rate.",
            ],
        )

    if args.monthly_requests >= 10_000_000:
        add_action(
            actions,
            dedupe,
            "request-shaping",
            45,
            "Apply request shaping and API efficiency controls",
            "Large request volumes amplify small inefficiencies.",
            [
                "Add response caching on high-read endpoints.",
                "Set client retry budgets and exponential backoff.",
                "Add rate limits and idempotency keys for expensive writes.",
            ],
        )

    if args.monthly_egress_gb >= 2000:
        add_action(
            actions,
            dedupe,
            "egress",
            50,
            "Cut bandwidth and egress costs",
            "Egress-heavy traffic is often reducible with cache and payload controls.",
            [
                "Move static and cacheable traffic behind CDN edge caching.",
                "Compress payloads and remove unused fields from responses.",
                "Review cross-region data paths and keep read traffic local.",
            ],
        )

    if args.country.upper() in EEA_COUNTRIES or "data-residency" in args.restrictions:
        add_action(
            actions,
            dedupe,
            "residency",
            60,
            "Lock workload placement to compliant regions",
            "Country and residency constraints can invalidate low-cost region choices.",
            [
                "Pin data-plane services to approved regions first.",
                "Separate control-plane and analytics workloads when permitted.",
                "Recalculate egress assumptions after compliant region placement.",
            ],
        )

    if args.company_size in {"solo", "startup"}:
        add_action(
            actions,
            dedupe,
            "tooling-seats",
            70,
            "Tighten paid tooling and seat governance",
            "Early-stage teams often overpay for inactive collaboration/tool seats.",
            [
                "Audit seats monthly and reclaim inactive users.",
                "Downgrade non-critical users to lighter plans.",
                "Standardize on one API workspace unless segregation is required.",
            ],
        )

    if args.postman_seats > 10:
        add_action(
            actions,
            dedupe,
            "postman",
            75,
            "Review Postman workspace and seat utilization",
            "Seat-heavy API tooling spend should be usage-justified.",
            [
                "Group users by role: author, reviewer, consumer.",
                "Keep paid author seats only for active API producers.",
                "Archive inactive workspaces and remove duplicate collections.",
            ],
        )

    if tier in {"growth", "enterprise"}:
        add_action(
            actions,
            dedupe,
            "commitments",
            80,
            "Use commitments for stable baselines",
            "Steady workloads are usually cheaper under commitment programs.",
            [
                "Measure 4-8 weeks of baseline demand before buying commitments.",
                "Buy commitments for steady-state layers, keep burst on demand.",
                "Review unused commitment coverage monthly.",
            ],
        )

    if "api-saas" in args.system_types:
        add_action(
            actions,
            dedupe,
            "api-saas",
            85,
            "Optimize API read patterns and cache strategy",
            "API SaaS economics are highly sensitive to request-path efficiency.",
            [
                "Split hot and cold endpoints and tune cache TTL per path.",
                "Prefer projection queries over full payload retrieval.",
                "Track p95 endpoint cost per 10K calls.",
            ],
        )

    if "data-platform" in args.system_types:
        add_action(
            actions,
            dedupe,
            "data-platform",
            90,
            "Optimize analytical storage and scan costs",
            "Data-platform spend grows quickly without lifecycle and pruning controls.",
            [
                "Partition large tables and enforce query pruning.",
                "Move cold data to cheaper storage tiers.",
                "Set per-team query spend quotas and alert thresholds.",
            ],
        )

    if "edge-iot" in args.system_types:
        add_action(
            actions,
            dedupe,
            "edge-iot",
            95,
            "Batch and compress edge telemetry",
            "Edge workloads commonly overspend on transport and message volume.",
            [
                "Batch telemetry where latency budgets allow.",
                "Use compact payload formats and compression.",
                "Drop redundant heartbeat frequency where safe.",
            ],
        )

    if any(r in args.restrictions for r in {"pci", "hipaa", "fedramp"}):
        add_action(
            actions,
            dedupe,
            "regulated",
            100,
            "Model compliance boundary costs explicitly",
            "Regulated workloads need architecture choices that change cost shape.",
            [
                "Separate compliant and non-compliant workloads into clear boundaries.",
                "Measure incremental controls cost per product line.",
                "Prefer managed controls where they reduce audit and ops overhead.",
            ],
        )

    actions.sort(key=lambda item: int(item["priority"]))
    return actions


def phase_actions(actions: List[Dict[str, object]]) -> Dict[str, List[str]]:
    immediate = [a["title"] for a in actions[:4]]
    medium = [a["title"] for a in actions[4:9]]
    follow_up = [a["title"] for a in actions[9:]]
    return {
        "0-14_days": immediate,
        "15-45_days": medium,
        "46-90_days": follow_up,
    }


def build_summary(args: argparse.Namespace, tier: str) -> Dict[str, object]:
    req_per_compute_hour = None
    if args.monthly_requests > 0 and args.monthly_compute_hours > 0:
        req_per_compute_hour = round(args.monthly_requests / args.monthly_compute_hours, 2)

    egress_per_1k_requests_mb = None
    if args.monthly_requests > 0 and args.monthly_egress_gb > 0:
        total_mb = args.monthly_egress_gb * 1024
        egress_per_1k_requests_mb = round((total_mb / args.monthly_requests) * 1000, 4)

    cost_per_1m_requests = None
    if args.monthly_requests > 0 and args.monthly_budget_usd > 0:
        cost_per_1m_requests = round(args.monthly_budget_usd / (args.monthly_requests / 1_000_000), 2)

    signals: List[str] = []
    if args.preload_ratio >= 0.25:
        signals.append("high_preload_ratio")
    if args.monthly_egress_gb >= 2000:
        signals.append("high_egress")
    if args.monthly_requests >= 10_000_000:
        signals.append("high_request_volume")
    if args.postman_seats > 10:
        signals.append("tool_seat_growth")
    if args.country.upper() in EEA_COUNTRIES or "data-residency" in args.restrictions:
        signals.append("residency_sensitive")

    return {
        "budget_tier": tier,
        "country": args.country.upper(),
        "company_size": args.company_size,
        "system_types": sorted(args.system_types),
        "restrictions": sorted(args.restrictions),
        "clouds": sorted(args.clouds),
        "requests_per_compute_hour": req_per_compute_hour,
        "egress_mb_per_1k_requests": egress_per_1k_requests_mb,
        "cost_per_1m_requests_usd": cost_per_1m_requests,
        "signals": signals,
    }


def build_correct_practices(args: argparse.Namespace) -> Dict[str, List[str]]:
    do_items = [
        "Track core unit metrics weekly: cost/1M requests, cost/active user, egress/1K requests.",
        "Require consistent tagging and ownership on production resources.",
        "Run a monthly seat audit for paid tooling and remove inactive users.",
    ]
    avoid_items = [
        "Do not optimize from monthly total bill alone without unit metrics.",
        "Do not commit to long reservations before usage stabilizes.",
        "Do not accept unlimited retries on expensive API paths.",
    ]
    measure_items = [
        "Tagged spend percentage",
        "Budget variance by workload",
        "Requests per compute hour",
    ]

    if args.preload_ratio >= 0.25:
        add_unique(
            do_items,
            [
                "Move low-hit preload flows to demand fetch and enforce cache TTL rules.",
            ],
        )
        add_unique(
            avoid_items,
            [
                "Do not preload low-hit datasets by default.",
            ],
        )
        add_unique(
            measure_items,
            [
                "Preload hit-rate",
            ],
        )

    if args.monthly_egress_gb >= 2000:
        add_unique(
            do_items,
            [
                "Route static and cacheable traffic through CDN with compression enabled.",
            ],
        )
        add_unique(
            avoid_items,
            [
                "Do not keep cross-region reads as default where in-region serving is viable.",
            ],
        )
        add_unique(
            measure_items,
            [
                "Egress MB per 1K requests",
                "CDN offload percentage",
            ],
        )

    if args.postman_seats > 10:
        add_unique(
            do_items,
            [
                "Role-segment API tooling seats and keep paid author seats for active producers.",
            ],
        )
        add_unique(
            avoid_items,
            [
                "Do not keep duplicated workspaces and stale collections indefinitely.",
            ],
        )
        add_unique(
            measure_items,
            [
                "Active-to-paid seat ratio",
            ],
        )

    if args.country.upper() in EEA_COUNTRIES or "data-residency" in args.restrictions:
        add_unique(
            do_items,
            [
                "Select compliant data-plane regions before optimization of unit rates.",
            ],
        )
        add_unique(
            avoid_items,
            [
                "Do not choose lowest-cost regions that violate residency obligations.",
            ],
        )
        add_unique(
            measure_items,
            [
                "Policy exception count for residency controls",
            ],
        )

    if any(r in args.restrictions for r in {"pci", "hipaa", "fedramp"}):
        add_unique(
            do_items,
            [
                "Model compliance boundary cost separately from general infrastructure spend.",
            ],
        )
        add_unique(
            avoid_items,
            [
                "Do not bypass compliance segmentation to reduce short-term cost.",
            ],
        )
        add_unique(
            measure_items,
            [
                "Remediation time for non-compliant cost-critical services",
            ],
        )

    return {
        "do": do_items,
        "avoid": avoid_items,
        "measure": measure_items[:6],
    }


def build_policy_boundaries(args: argparse.Namespace) -> List[str]:
    boundaries: List[str] = []

    if args.country.upper() in EEA_COUNTRIES or "data-residency" in args.restrictions:
        boundaries.append(
            "Data residency boundary: keep data-plane services in approved in-country or in-region locations before cost tuning."
        )
    if "pci" in args.restrictions:
        boundaries.append(
            "PCI boundary: preserve segmentation and cardholder-data scoping; do not merge compliant and non-compliant paths for convenience."
        )
    if "hipaa" in args.restrictions:
        boundaries.append(
            "HIPAA boundary: maintain required safeguards and access controls; cost changes must preserve PHI protections."
        )
    if "fedramp" in args.restrictions:
        boundaries.append(
            "FedRAMP boundary: remain within authorized regions/services and keep audit trails for all spend-control changes."
        )
    if "soc2" in args.restrictions:
        boundaries.append(
            "SOC 2 boundary: maintain auditable ownership, change control, and exception workflows for cost-related decisions."
        )

    if not boundaries:
        boundaries.append(
            "No explicit regulatory restriction was provided; still require ownership tagging, change logs, and budget guardrails."
        )

    return boundaries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diagnose cost profile and generate ranked optimization actions."
    )
    parser.add_argument("--monthly-budget-usd", type=float, default=0.0)
    parser.add_argument(
        "--company-size",
        choices=["solo", "startup", "smb", "mid-market", "enterprise"],
        default="startup",
    )
    parser.add_argument(
        "--system-types",
        default="api-saas",
        help="Comma-separated list: api-saas,ecommerce,mobile-backend,data-platform,ml-batch,edge-iot,internal-tools",
    )
    parser.add_argument(
        "--restrictions",
        default="",
        help="Comma-separated list: data-residency,pci,hipaa,soc2,fedramp,low-latency,multi-cloud",
    )
    parser.add_argument(
        "--clouds",
        default="aws",
        help="Comma-separated list: aws,azure,gcp,multi,onprem-hybrid",
    )
    parser.add_argument("--country", default="US", help="Country code, for example US, DE, IN")
    parser.add_argument("--monthly-requests", type=float, default=0.0)
    parser.add_argument("--monthly-compute-hours", type=float, default=0.0)
    parser.add_argument("--monthly-storage-gb", type=float, default=0.0)
    parser.add_argument("--monthly-egress-gb", type=float, default=0.0)
    parser.add_argument("--preload-ratio", type=float, default=0.0)
    parser.add_argument("--postman-seats", type=int, default=0)
    parser.add_argument("--format", choices=["text", "json"], default="text")

    args = parser.parse_args()
    args.system_types = parse_csv_set(args.system_types)
    args.restrictions = parse_csv_set(args.restrictions)
    args.clouds = parse_csv_set(args.clouds)
    args.preload_ratio = min(max(args.preload_ratio, 0.0), 1.0)
    return args


def render_text(
    summary: Dict[str, object],
    actions: List[Dict[str, object]],
    phases: Dict[str, List[str]],
    correct_practices: Dict[str, List[str]],
    policy_boundaries: List[str],
) -> str:
    lines: List[str] = []
    lines.append("Cost Diagnosis")
    lines.append("================")
    lines.append(f"Budget tier: {summary['budget_tier']}")
    lines.append(f"Country: {summary['country']}")
    lines.append(f"Company size: {summary['company_size']}")
    lines.append(f"System types: {', '.join(summary['system_types']) or 'none'}")
    lines.append(f"Restrictions: {', '.join(summary['restrictions']) or 'none'}")
    lines.append(f"Clouds: {', '.join(summary['clouds']) or 'none'}")

    if summary["requests_per_compute_hour"] is not None:
        lines.append(f"Requests per compute hour: {summary['requests_per_compute_hour']}")
    if summary["egress_mb_per_1k_requests"] is not None:
        lines.append(f"Egress MB per 1K requests: {summary['egress_mb_per_1k_requests']}")
    if summary["cost_per_1m_requests_usd"] is not None:
        lines.append(f"Cost per 1M requests (USD): {summary['cost_per_1m_requests_usd']}")

    lines.append("")
    lines.append("Risk Signals")
    lines.append("------------")
    if summary["signals"]:
        for signal in summary["signals"]:
            lines.append(f"- {signal}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("Ranked Actions")
    lines.append("--------------")
    for idx, action in enumerate(actions, 1):
        lines.append(f"{idx}. {action['title']} (P{action['priority']})")
        lines.append(f"   Why: {action['reason']}")
        for step in action["steps"]:
            lines.append(f"   - {step}")

    lines.append("")
    lines.append("90-Day Sequence")
    lines.append("---------------")
    for phase, titles in phases.items():
        lines.append(f"{phase}:")
        if titles:
            for title in titles:
                lines.append(f"- {title}")
        else:
            lines.append("- none")

    lines.append("")
    lines.append("Correct Practices")
    lines.append("-----------------")
    lines.append("Do:")
    for item in correct_practices["do"]:
        lines.append(f"- {item}")
    lines.append("Avoid:")
    for item in correct_practices["avoid"]:
        lines.append(f"- {item}")
    lines.append("Measure:")
    for item in correct_practices["measure"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("Policy Boundaries")
    lines.append("-----------------")
    for item in policy_boundaries:
        lines.append(f"- {item}")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    tier = budget_tier(args.monthly_budget_usd)
    summary = build_summary(args, tier)
    actions = build_actions(args, tier)
    phases = phase_actions(actions)
    correct_practices = build_correct_practices(args)
    policy_boundaries = build_policy_boundaries(args)

    payload = {
        "inputs": {
            "monthly_budget_usd": args.monthly_budget_usd,
            "company_size": args.company_size,
            "system_types": sorted(args.system_types),
            "restrictions": sorted(args.restrictions),
            "clouds": sorted(args.clouds),
            "country": args.country.upper(),
            "monthly_requests": args.monthly_requests,
            "monthly_compute_hours": args.monthly_compute_hours,
            "monthly_storage_gb": args.monthly_storage_gb,
            "monthly_egress_gb": args.monthly_egress_gb,
            "preload_ratio": args.preload_ratio,
            "postman_seats": args.postman_seats,
        },
        "summary": summary,
        "actions": actions,
        "phases": phases,
        "correct_practices": correct_practices,
        "policy_boundaries": policy_boundaries,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return

    print(render_text(summary, actions, phases, correct_practices, policy_boundaries))


if __name__ == "__main__":
    main()
