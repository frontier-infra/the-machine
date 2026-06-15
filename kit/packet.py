"""Render — the dated conformance packet, and the test matrix (a derived view).

The packet separates what v0 actually verified (static) from what it declared
not-run (chaos), so a reader can never mistake "not measured" for "passed."
"""
from __future__ import annotations

from datetime import datetime, timezone

from .obligations import OBLIGATIONS

MARK = {"PASS": "✓ PASS", "PARTIAL": "~ PARTIAL", "FAIL": "✗ FAIL", "NOT_RUN": "· NOT-RUN", "NA": "– NA"}


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def render_packet(s: dict) -> str:
    L = s["confirmed_level"]
    out: list[str] = []
    out.append(f"# Conformance packet — {s['deployment']}")
    out.append(f"_Kit {s['kit_version']} · static/structural · {_today()} · against {s['spec']}_\n")
    out.append(f"## Confirmed level: **{s['confirmed_level_name']}**")
    out.append("> Strict: the highest level at which every *static* obligation ≤ that level is a clean PASS. "
               "PARTIAL/FAIL cap the level and are listed as blockers. Chaos checks are NOT-RUN in v0.\n")

    # vNext deltas headline
    out.append("**vNext deltas (the obligations the 2026-06-14 ratification added):**")
    for oid in ("delta1_reversibility", "gov_override", "gov_contract_enforce", "delta3_heartbeat", "delta3_anomaly"):
        if oid in s["vnext"]:
            o, r = s["vnext"][oid]
            out.append(f"- {MARK[r.status]} — {o.title}")
    out.append("")

    # per-level tally
    out.append("| Level | PASS | PARTIAL | FAIL | NOT-RUN |")
    out.append("|---|---|---|---|---|")
    for lvl in sorted(s["tally"]):
        t = s["tally"][lvl]
        out.append(f"| L{lvl} | {t['PASS']} | {t['PARTIAL']} | {t['FAIL']} | {t['NOT_RUN']} |")
    out.append("")

    # blockers to next level
    if s["blockers"]:
        out.append(f"### To reach {s['next_level_name']} — clear these")
        for o, r in s["blockers"]:
            out.append(f"- {MARK[r.status]} **{o.title}** — {r.evidence}")
        out.append("")

    # full evidence table
    out.append("### Full obligation results (evidence-cited)")
    out.append("| Status | L | Obligation | Evidence |")
    out.append("|---|---|---|---|")
    for o, r in s["rows"]:
        if r.status == "NOT_RUN":
            continue
        ev = r.evidence.replace("|", "\\|")
        tag = " ·Δ" if o.vnext else ""
        out.append(f"| {MARK[r.status]} | L{o.level} | {o.title}{tag} | {ev} |")
    out.append("")

    # not-run (no silent gaps)
    out.append("### Declared NOT-RUN in v0 (need a live deployment — chaos/replay)")
    for o, r in s["not_run"]:
        out.append(f"- · **{o.title}** — {r.evidence}")
    out.append("")
    out.append("_Score is deterministic from repo content; re-running yields the same level. "
               "Only this packet's date moves._")
    return "\n".join(out)


def render_matrix() -> str:
    out = ["# The Machine — Conformance Test Matrix",
           "_Derived view of `kit/obligations.py` (single source of truth). "
           "Regenerate: `python -m kit matrix`._\n",
           "| ID | Obligation | Plane | Level | Kind | Δ | What passing looks like |",
           "|---|---|---|---|---|---|---|"]
    for o in OBLIGATIONS:
        d = "Δ" if o.vnext else ""
        ev = o.evidence.replace("|", "\\|")
        out.append(f"| `{o.id}` | {o.title} | {o.plane} | L{o.level} | {o.kind} | {d} | {ev} |")
    out.append("\n**Kind:** `static` = the v0 runner checks it now · `chaos` = needs a live "
               "deployment, declared NOT-RUN in v0 (never faked).")
    return "\n".join(out)
