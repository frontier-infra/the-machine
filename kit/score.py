"""Scoring — run every obligation against a deployment, aggregate to a level.

The SCORE is a deterministic function of repo content (static checks), so a re-run
yields the same level and per-obligation statuses. Only the packet's timestamp moves.

`confirmed_level` is strict and honest: the highest conformance level L at which
EVERY static obligation with level ≤ L is a clean PASS. A PARTIAL or FAIL at level L
caps the deployment below L — and is reported as a blocker, not hidden. Chaos
obligations are NOT_RUN in v0 and never count toward the static level; they are listed
so the gap is visible, never silently assumed covered.
"""
from __future__ import annotations

from .checks import CHECKS, CheckResult, RepoView
from .obligations import OBLIGATIONS

LEVEL_NAMES = {0: "L0 Look-Alike", 1: "L1 Declared", 2: "L2 Instrumented",
               3: "L3 Enforced", 4: "L4 Receipted", 5: "L5 Trusted Autonomy"}


def _run_rows(repo: RepoView):
    rows = []
    for o in OBLIGATIONS:
        if o.kind == "chaos":
            res = CheckResult("NOT_RUN", o.evidence)
        else:
            res = CHECKS[o.id](repo)
        rows.append((o, res))
    return rows


def _confirmed_level(rows) -> int:
    level = 0
    for L in (1, 2, 3, 4, 5):
        at = [(o, r) for (o, r) in rows if o.kind == "static" and o.level <= L]
        if at and all(r.status == "PASS" for (_, r) in at):
            level = L
    if level == 0 and any(o.plane == "box" and r.status in ("PASS", "PARTIAL") for (o, r) in rows):
        level = 1
    return level


def _classify(rows) -> tuple[bool, str]:
    """Is this repo a Machine deployment at all?

    A deployment must show the irreducible signature of a long-running agent: a
    deterministic driver loop (Box 2). A signing library, a web-protocol spec, or the
    standard itself has no driver loop — the six-box ladder does not describe it. For
    those the kit declines to assign a level (and refuses the L1 floor-bump) rather than
    report a meaningless 'Machine L1'. Box 2 is the discriminator because every real
    deployment passes it and a non-deployment cannot.
    """
    for o, r in rows:
        if o.id == "box2_driver":
            if r.status in ("PASS", "PARTIAL"):
                return True, ""
            return False, f"no deterministic driver loop — Box 2 {r.status} ({r.evidence})"
    return True, ""  # box2 obligation absent from the set → don't misclassify


def score_repo(root: str, name: str | None = None) -> dict:
    repo = RepoView(root)
    rows = _run_rows(repo)
    is_deployment, classification_reason = _classify(rows)
    level = _confirmed_level(rows) if is_deployment else None

    tally = {L: {"PASS": 0, "PARTIAL": 0, "FAIL": 0, "NOT_RUN": 0} for L in (2, 3, 4, 5)}
    for o, r in rows:
        tally.setdefault(o.level, {"PASS": 0, "PARTIAL": 0, "FAIL": 0, "NOT_RUN": 0})
        tally[o.level][r.status] = tally[o.level].get(r.status, 0) + 1

    if is_deployment:
        level_name = LEVEL_NAMES[level]
        next_name = LEVEL_NAMES.get(level + 1, "—")
        blockers = [(o, r) for (o, r) in rows
                    if o.kind == "static" and o.level == level + 1 and r.status != "PASS"]
    else:
        level_name = "NOT A MACHINE DEPLOYMENT"
        next_name = "—"
        blockers = []
    vnext = {o.id: (o, r) for (o, r) in rows if o.vnext}
    not_run = [(o, r) for (o, r) in rows if r.status == "NOT_RUN"]

    return {
        "deployment": name or root.rstrip("/").split("/")[-1],
        "root": str(repo.root),
        "kit_version": "v0",
        "spec": "The Machine — Conformance Spec vNext (ratified 2026-06-14)",
        "is_deployment": is_deployment,
        "classification_reason": classification_reason,
        "confirmed_level": level,
        "confirmed_level_name": level_name,
        "next_level_name": next_name,
        "tally": tally,
        "rows": rows,
        "vnext": vnext,
        "blockers": blockers,
        "not_run": not_run,
    }
