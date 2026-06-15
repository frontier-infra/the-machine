"""The conformance kit CLI.

    python -m kit score <repo> [--out FILE]   # score a deployment, emit a packet
    python -m kit matrix [--out FILE]          # render the test matrix (derived view)

Static/structural only (v0). Chaos/replay obligations are declared NOT-RUN. The kit
measures a deployment; it never modifies it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .packet import render_matrix, render_packet
from .score import score_repo


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="kit", description="The Machine — conformance kit (v0).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sc = sub.add_parser("score", help="Score a deployment repo against the vNext obligations.")
    sc.add_argument("repo")
    sc.add_argument("--name", default=None)
    sc.add_argument("--out", default=None)
    mx = sub.add_parser("matrix", help="Render the test matrix from obligations.py.")
    mx.add_argument("--out", default=None)
    args = p.parse_args(argv)

    if args.cmd == "matrix":
        text = render_matrix()
    else:
        if not Path(args.repo).exists():
            print(f"[FAIL] repo not found: {args.repo}", file=sys.stderr)
            return 1
        s = score_repo(args.repo, args.name)
        text = render_packet(s)
        print(f"[{s['deployment']}] confirmed level: {s['confirmed_level_name']}  "
              f"(blockers to {s['next_level_name']}: {len(s['blockers'])}; not-run: {len(s['not_run'])})",
              file=sys.stderr)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
