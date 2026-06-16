# Changelog

All notable changes to The Machine (spec + kit) are recorded here.
**Every commit updates this file** — enforced by `.githooks/pre-commit`.
Format follows [Keep a Changelog](https://keepachangelog.com); the kit is v0/unversioned.

## [Unreleased]

### Added
- **Orchestrator shape** (Δ7 · Council 5–0 · 2026-06-16): the kit scores two **shapes** — `machine`
  (Dumb Driver) and `orchestrator` (model-in-the-loop). `kit score <repo> --shape orchestrator` scores
  the **Orchestrator Keystone** (closed typed transitions · persist-before-effect · zero-token replay)
  in place of Box 2. Scores stamp `Machine-L*` / `Orchestrator-L*` (never bare `L*`); cross-shape
  label-laundering is refused; the orchestrator ceiling is **L4** (L5 barred). subctl + argentos now
  read as `Orchestrator-L1` instead of false machine scores. Shape is **declared** via `--shape`;
  auto-detection from source is deferred (parser work).
- **Deployment classifier** (`kit/score.py`): repos with no deterministic driver loop
  (Box 2 absent) return **NOT A MACHINE DEPLOYMENT** with a cited reason, instead of being
  floor-bumped to a meaningless L1. Catches the AAR signing library, the AVL web spec, and
  the spec repo itself. (`8f5dee1`)
- **`CHANGELOG.md` + pre-commit hook** (`.githooks/pre-commit`) requiring a changelog entry
  on every commit.

### Changed
- **Box 2 purity restored** (`THE-MACHINE.md`): deleted the "calibration / an LLM-orchestrated driver
  is acceptable until observed mishandling" escape hatch. Box 2 is token-free, full stop;
  model-in-the-loop is the `orchestrator` shape, not a calibrated Dumb Driver.
- **Substring false-positive cleanup** in the evidence scan (`kit/checks.py`):
  - Exclude dependency manifests + lockfiles (`package.json`, `package-lock.json`,
    `pnpm-lock.yaml`, `yarn.lock`, `*.lock`) — dep/script names are declarations, not
    implementation. (Killed argentos's `@noble/ed25519`, `transformer-throttler`,
    `package-manager-detector` false-PASSes.)
  - Box 1 atomic-write match excludes `x.replace(/regex/)` (a string replace) while keeping
    `os.replace(var)` and pathlib `tmp.replace(dst)`. Kills avl's route-trim false-PASS;
    machine-driver / conductor unaffected.
  - `CHECKS` registry built from `OBLIGATIONS` ids — no longer a `globals()` scrape that
    leaked `Path` / `dataclass` as bogus entries.

### Removed
- Dead `RepoView.exists()` (no callers).

### Known gaps (deferred)
- TS string-replace `x.replace(ident)` and bare `while True:` false-positives (e.g. argentos)
  are syntactically identical to legitimate Python-deployment idioms (`tmp.replace(dst)`,
  `driver.py: while True:`). Separating them needs a parser — out of scope for the stdlib-only
  v0. **argentos + subctl are deferred** to the shape-profile / Council decision on
  non-dumb-driver (orchestrator / kernel) architectures.
