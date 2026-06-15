# The Machine — Conformance Test Matrix
_Derived view of `kit/obligations.py` (single source of truth). Regenerate: `python -m kit matrix`._

| ID | Obligation | Plane | Level | Kind | Δ | What passing looks like |
|---|---|---|---|---|---|---|
| `box0_contract` | Box 0 — Contracted Decomposition | box | L2 | static |  | a contract artifact carrying proposed_by, ratified_by, acceptance_tests, immutable |
| `box0_ratified` | Box 0 — independent ratification (ratified_by ≠ proposed_by) | box | L3 | static |  | the contract is gated on ratified_by != proposed_by |
| `box1_state` | Box 1 — Durable Goal + State (survives kill) | box | L2 | static |  | state persisted to a store with an atomic/checkpoint write |
| `box2_driver` | Box 2 — Dumb Driver (deterministic control loop) | box | L2 | static |  | a driver loop / deterministic engine, token-free in the loop |
| `box3_workers` | Box 3 — Fresh Workers (one per move) | box | L2 | static |  | a fresh worker/process spawned per task |
| `box4_verify` | Box 4 — Verify vs Reality (verifier ≠ subject, fail-closed) | box | L3 | static |  | an independent verifier; no verifier ⇒ cannot pass (fail-closed) |
| `box5_dial` | Box 5 — Autonomy Dial (min(operator, ceiling, trust)) | box | L3 | static |  | the gate computes effective autonomy = min(dial, ceiling, verifier_trust) |
| `delta1_reversibility` | Box 5 — Reversibility gate (Δ1) | box | L3 | static | Δ | reversibility is a term inside the evaluated gate; reversible:true is verifier-attested |
| `gov_ceiling` | Governance — Autonomy Ceiling enforced | governance | L3 | static |  | effective autonomy is capped by a contract ceiling |
| `gov_verifier_trust` | Governance — Verifier Trust Requirements (no verifier ⇒ trust 0) | governance | L3 | static |  | trust is 0 without a present/fresh verifier ⇒ propose-only |
| `gov_contract_enforce` | Governance — Contract Enforcement (hard-deny, at the driver) | governance | L3 | static | Δ | no mutating move without a RATIFIED contract; denied at the driver |
| `gov_override` | Governance — Operator Override (bound SLO, non-bypassable) | governance | L3 | static | Δ | a mid-flight halt/lower-autonomy with a bounded SLO seconds |
| `gov_audit_hooks` | Governance — Audit & Compliance Hooks (append-only, chained) | governance | L3 | static |  | append-only, hash/signature-chained governance receipts |
| `svc_aar` | Service — AAR receipts (signed) | service | L4 | static |  | every transition emits a SIGNED receipt (unsigned ⇒ partial, the L3→L4 line) |
| `svc_frontier_id` | Service — Frontier Infra (deployment_id + scope_id in receipts) | service | L4 | static |  | receipts carry a stable deployment_id + scope_id |
| `svc_contracts` | Service — Agent Contracts (caps as pre-mutation checks) | service | L3 | static |  | retry/cost/concurrency caps checked before mutation, not on a dashboard |
| `svc_observability` | Service — Observability (alert-with-ACK) | service | L3 | static |  | failure/halt raises an alert (ACK ⇒ full pass) |
| `ops_idempotency` | Ops — Idempotency (key per mutating action) | ops | L3 | static |  | an idempotency_key derived from goal+artifact+intent |
| `ops_quarantine` | Ops — Terminal Quarantine (block, don't re-queue forever) | ops | L3 | static |  | after max_attempts ⇒ terminal quarantine, surfaced |
| `ops_governor` | Ops — Budget / Resource Governor (breach ⇒ halt+alert) | ops | L3 | static |  | a declared cost/resource envelope; breach throttles/halts |
| `ops_nonbypass` | Ops — Non-bypassability (all mutation via the gate) | ops | L3 | static |  | mutating side-effects route through a single gate |
| `delta3_heartbeat` | Runtime Health — last_success_at + independent monitor (Δ3) | runtime | L3 | static | Δ | critical components publish last_success_at; an independent monitor alerts on staleness |
| `delta3_anomaly` | Runtime Health — registered anomaly detectors (Δ3) | runtime | L3 | static | Δ | a registered, finite detector set (rate/dup/thermal/silent-organ) with fixtures |
| `chaos_kill_resume` | Chaos — kill driver mid-move → resume same task | box | L2 | chaos |  | kill -9 the driver mid-move; restart resumes the same task_id, no dup work |
| `chaos_lying_worker` | Chaos — inject a lying worker → caught by the verifier | box | L3 | chaos |  | a worker reports success on a failing change; the verifier blocks the commit |
| `chaos_override_bypass` | Chaos — red-team the operator override (non-bypassable) | governance | L3 | chaos |  | with override asserted, every in-band continuation path is refused |
| `chaos_dup_key` | Chaos — duplicate idempotency key → single effect | ops | L3 | chaos |  | two actions with the same key produce one effect (no second ACTIVE row) |
| `chaos_budget_thermal` | Chaos — budget/thermal breach → throttle+alert ≤ N s | ops | L3 | chaos |  | drive a cost/thermal breach; the governor throttles and alerts within N seconds |
| `chaos_signed_aar` | Chaos — verify a signed AAR chain with a public key | service | L4 | chaos |  | export the receipt chain; an independent verifier validates the signatures |

**Kind:** `static` = the v0 runner checks it now · `chaos` = needs a live deployment, declared NOT-RUN in v0 (never faked).
