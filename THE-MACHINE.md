# The Machine — Conformance Spec vNext

> **This repository is the canonical source of The Machine — Conformance Spec.** Version **vNext**,
> ratified 2026-06-14 by an independent multi-model council and operator signature
> (`ratified_by ≠ proposed_by`). It consolidates the prior v1 plus six ratified amendments (Δ1–Δ6).
> The spec is canonical; the poster is a derived view, re-rendered when the spec changes.

**What this is.** The poster describes; this spec *falsifies*. A deployment only **counts** as The
Machine if it passes. The durable layer is not the boxes, it is the **obligations**: one checkable
rule per box that a hook or test can verify.

**Thesis.** The model is replaceable. The Machine is not. Continuity lives in the artifact, not the
session. **Vocabulary:** Machine = the harness · Workflows = the work · Deployments = the wiring ·
Models = the workers · Reality = the boss.

---

## Foundation Principles (the canonical four)

1. **Independent Judgment** — `subject ≠ judge`, at every layer. The law that protects reality.
2. **Reality Over Narrative** — trust what is observed, measured, or verified; not what is claimed.
   *(absorbs the former "Observable Everything" + "Verify vs Reality" — the merge is at the
   principle layer; their underlying box obligations remain in force and are checked separately.)*
3. **State Over Session** — state, memory, and goals outlive any worker or conversation.
4. **Autonomy Is Earned** — authority is justified by verified performance and evidence.

*Fold-ins (annotated, not deleted): "Deterministic Control" → Box 2; "Contracts over Prompts" →
Box 0. (Exhibit on fold-in: the v1 seven-principle list is retained beside this mapping in the
ratification record, losslessness confirmed by inspection.)*

## The structural law

> **`verifier ≠ subject` must hold at TWO layers.** Box 0 ratifies the *target*; Box 4 ratifies the
> *result*. If the doer or its planner defines "done," self-grading relocates to the planning layer
> and you verify perfectly against the wrong target. Drop the independent judge at either layer and
> the back door reopens. *The agent that defines success must not be the agent that achieves it — at
> every layer.* The independent judge may be a Council (target) or a verifier/ground-truth test
> (result); it need not be a specific human.

---

## The Loop — 6 boxes (0–5), one checkable obligation each

### Box 0 — Contracted Decomposition
**Obligation:** no mutating move begins without a **verifier-ratified, signed Sprint Contract**;
`ratified_by ≠ proposed_by`. **Pass:** contract exists, independently ratified, AAR-signed, the move
references it, acceptance tests immutable for the move. **Fail:** worker defines its own done; tests
edited mid-move.

```yaml
contract: {goal, scope, definition_of_done, acceptance_tests, constraints,
           immutable: [acceptance_tests], owner, autonomy_ceiling, verification_requirements,
           proposed_by, ratified_by, receipt}
```

### Box 1 — Durable Goal + State
**Obligation:** goal + state live outside any session and survive `kill -9`; the next tick resumes
the *same* move (counter+1). **Pass:** kill mid-move → restart resumes same `task_id`, no dup work.

### Box 2 — Dumb Driver
**Obligation:** the control loop spends **zero model tokens** — a deterministic function of (state,
clock, events) → next dispatch. Token-free is not a *target*, it is the obligation: a model in the
control loop is a **different shape** (see *Shapes*), never a "calibrated" Dumb Driver. **Pass:** the
loop dispatches / retries / routes / persists with no model call; replay is byte-identical.
*(Absorbs "Deterministic Control.")*

### Box 3 — Fresh Workers
**Obligation:** each move = a new session, bounded context reconstructable from durable state,
**scoped to the contract** (no one-shotting). **Pass:** unique session token; context ≤ ceiling;
worker cannot exceed contract scope.

### Box 4 — Verify vs Reality
**Obligation:** no durable mutation without a signed **PASS** where `verifier_id ≠ subject_id` AND the
check runs the contract's `acceptance_tests` against **ground truth** (AVL-preferred), not the
worker's report. FAIL → block/quarantine, never "save anyway." **Pass:** inject a lying worker →
caught; remove the verifier → commit hard-denied.

### Box 5 — Autonomy Dial + Reversibility Gate  *(amended, Δ1)*
**Obligation:** the gate is the only path to durable mutation (non-bypassable), and **reversibility is
a term inside the evaluated gate**, not commentary:

```
required_trust(action) = base_trust(scope) + (reversible == false ? IRREVERSIBLE_TIER_BUMP : 0)
proceed iff effective_autonomy >= required_trust(action) AND (reversible OR human_gate_satisfied)
effective_autonomy = min(operator_dial, contract.autonomy_ceiling, MIN_over_scopes(verifier_trust[scope]))
```

- Every mutating action carries `{action_id, scope, reversible, rollback_ref?, human_gate_receipt_ref?}`;
  a missing `reversible` on a mutating action defaults to **false**.
- `reversible:true` is honored **only** if `rollback_ref` resolves to a rollback path the **Verifier**
  confirms; a forged/unresolving ref → treated as **irreversible**.
- For `reversible:false`: proceed only if `verifier_trust[scope] ≥ IRREVERSIBLE_TIER` (bump ≥ one whole
  tier; default highest tier if unset) **or** an explicit **human-gate receipt**. The human gate has a
  contract-declared bounded window; on expiry → **default-deny**.
- **No verifier for a scope ⇒ trust 0 ⇒ propose-only.** Trust is binary now (present + fresh + healthy →
  1, else 0); a graduated trust ledger from AAR history comes later (the path to L5).
- Every allow/deny/escalate emits an AAR receipt.

**Pass:** `reversible:false`, dial=5, low trust → denied unless human-gate receipt; forge a `rollback_ref`
that doesn't resolve → treated as irreversible. **Fail:** evaluated formula omits reversibility; self-
declared `reversible:true` honored; human-gate timeout auto-approves.

---

## Governance Layer  *(new named plane, Δ2)*

A single **non-bypassable** governance gate plus five controls. The controls **move** here (not copied —
no two sources of truth). All durable mutations pass through the gate or a **gate-issued token**; any
in-band path to a mutation without a gate decision is a **conformance failure**.

| Control | Obligation | Pass / Fail |
|---|---|---|
| Autonomy Ceiling | effective autonomy ≤ contract ceiling | over-ceiling denied / assumed past ceiling |
| Verifier Trust Requirements | trust 0 unless verifier **present, contract-qualified, fresh** ⇒ propose-only | expire verifier → commit denied / commit without fresh verifier |
| **Operator Override** | **non-bypassable** halt/lower-autonomy mid-flight within `override_effect_slo_seconds` (**≤ 5s mutating-halt / ≤ 60s dial-down; N=0 invalid; widen only by recorded exception**); receipted to a sink **independent of the haltable scope** | red-team: override asserted → every in-band continuation (retry/re-plan/sub-agent) refused, in-flight commits denied at the gate / any path completes a mutation after override |
| Contract Enforcement | no mutating move (incl. **read-with-side-effect**) without a contract `status==RATIFIED`, `proposed_by≠ratified_by`, hash present, scope-covering, unexpired/unrevoked; **hard-deny at the Dumb Driver** | strip/unratify ref → refused at the driver / proceeds on draft/absent contract |
| Audit & Compliance Hooks | every governance event → **append-only, signature-chained** receipt that survives the deployment; queryable by `deployment_id, contract_id, event_type, actor, time` | reproduce full chain over a window / gaps or erasable by the halted scope |

**Event types (required):** `contract_ratified, contract_revoked, dial_changed, override_requested,
override_effective, gate_allowed, gate_denied, gate_escalated`.

---

## Foundation Services — 6 cross-cutting

- **View Layer (AVL):** the verifier queries *machine-readable* ground truth, not the worker's narrative.
- **Frontier Infra:** every loop/worker/side-effect carries a stable `deployment_id` + `scope_id` in its
  receipts.
- **AAR (proof):** every state transition emits a signed receipt `{prev, next, idempotency_key,
  verifier_id?, autonomy_used}`. First durable truth; everyone else reads it.
- **Agent Contracts:** caps (retries/cost/concurrency), SLAs, escalation are **pre-mutation checks, not
  dashboards.**
- **Memory:** ingests only **AAR-receipted (verified)** outcomes; background extraction has
  `last_success_at` + staleness alert.
- **Observability:** failure/quarantine/budget-breach/verifier-stale → **alert-with-ACK within N s.**
  Passive metrics alone = fail.

## Always-on operational obligations (incident-hardened)

1. **Idempotency:** `idempotency_key = hash(goal_id, artifact_kind, normalized_intent)`; store rejects
   duplicates.
2. **Terminal Quarantine:** after `max_attempts`/unverifiable failure → `QUARANTINED` (terminal), not
   re-queue.
3. **Escalation-with-ACK:** block/quarantine/cap-hit → operator alert within N s requiring ACK or
   auto-quarantine.
4. **Budget / Resource Governor:** every loop declares attempts/tokens/wall-clock/GPU-seconds/$; breach →
   throttle/halt + alert. *Software must not burn hardware.*
5. **Non-bypassability:** ALL mutation paths route through the gate; a negative test proving none skips it
   is mandatory evidence.

## Runtime Health (continuous) vs Staleness Audit (quarterly)  *(amended, Δ3)*

**Two timescales, both kept.** *Is the organ alive?* (continuous) vs *is the limitation still real?*
(quarterly). Runtime Health does **not** replace the quarterly audit.

**Runtime Health (continuous):** every **critical component** (every Worker · Verifier · StateStore ·
Channel by default, unless explicitly demoted) publishes `last_success_at`. A **Runtime Health manifest**
lists each with `last_success_at` source, `staleness_threshold_seconds`, owner/escalation, `ack_slo_seconds`.
A monitor **independent of the monitored component** raises **alert-with-ACK** on staleness; the monitor
**publishes its own `last_success_at`** (the watcher is watched). A deployment enumerating no critical
components fails. **No-ACK chain:** no ACK in `T1` → throttle (dial −1 / to floor); no ACK in `T2` → halt.
**Anomaly detection = a registered finite set**, each with a firing fixture and declared threshold;
minimum classes the kit probes: rate-of-change, duplication ratio, thermal/resource saturation,
silent-organ. Unregistered class = accepted, **logged** gap (not silent). Test form: alert+page within `X`s
of crossing the declared threshold. Replayable fault injection required for: silent death, stale heartbeat,
≥1 anomaly sentinel.

**Staleness Audit (quarterly, the meta-obligation):** every obligation records `compensates_for / added /
retirement_test`. On every model release, re-run each `retirement_test` with the scaffold removed; passes
without it → retirement candidate. *Verify-vs-Reality pointed at the harness itself.*

---

## Deployments taxonomy (the "stamp")  *(Δ4)*

The Machine is the **harness**; deployments are **wirings** (ArgentOS, WR2, subCTL, Evy, Conductor,
machine-driver, + future Research/Coding/domain harnesses). **None are the Machine itself.** A deployment
**earns** a level via the conformance kit by binding its adapters (Worker · Verifier · StateStore ·
Channel) to the same core. Examples are **non-normative and non-exhaustive**. **No deployment is
grandfathered** — not ArgentOS, not WR2; all earn their level via the kit. *(Open thread: the conformance
kit is owed a one-paragraph formal definition — inputs: harness + wiring; output: a level.)*

### Shapes — `machine` vs `orchestrator`  *(Δ7, ratified 2026-06-16)*

A deployment's **shape** is part of its stamp. Two are recognized; the kit scores against the shape's
obligations and stamps the result **`Machine-L*` or `Orchestrator-L*` — never a bare `L*`**, so a
model-driven system can never silently claim the dumb-driver guarantee. Cross-shape label-laundering
(an orchestrator claiming Box 2) is a category error the kit refuses.

- **`machine`** — the canonical shape: a **Dumb Driver** (Box 2, zero model tokens). All six boxes apply as written.
- **`orchestrator`** — the model is *in* the control loop (it picks the next step). Box 2 is **replaced**
  by the **Orchestrator Keystone**:
  1. the model **proposes a typed transition from a closed, finite set** — it selects an edge, it cannot invent one;
  2. deterministic code **validates**, **persists the decision before any effect commits** (write-ahead), then **executes**;
  3. **replay reads the persisted decision log and spends zero model tokens** — re-invoking the model on replay is a **conformance FAILURE**, not a degraded pass.

  This isolates and records the nondeterminism so replay / kill-safety / verifiability survive even
  though a model chose the edge. An orchestrator is a **strictly smaller guarantee bundle** than a Dumb
  Driver: it recovers replay/kill-safety *a-posteriori* from the recorded choice, forfeiting the Dumb
  Driver's *a-priori* verifiability. **Ceiling:** an `orchestrator` may reach **L4 (Receipted)** but
  **never L5 (Trusted Autonomy)**. *(Council minority: hard cap at L3; L4 is the standing dial, L3 if
  maximum strictness is wanted.)*

## Conformance levels

| L | Name | Meaning |
|---|---|---|
| 0 | Look-Alike | resembles; no enforceable contracts |
| 1 | Declared | all boxes + services declared, some manual |
| 2 | Instrumented | state/driver/workers/verification/contracts/observability inspectable |
| 3 | Enforced | the system blocks, caps, alerts, escalates per contract |
| 4 | Receipted | material actions produce signed AAR receipts + independent verification |
| 5 | Trusted Autonomy | the dial may rise automatically on verifier-earned trust |

_Levels are stamped by shape (`Machine-L*` / `Orchestrator-L*`). The `orchestrator` ceiling is **L4** — L5 is barred (see Shapes)._

## Evidence to CLAIM conformance (resemblance ≠ conformance)

A signed packet, dated within 30 days: architecture map · executed self-tests (run, not asserted) ·
chaos/replay logs (kill→resume · lying-worker→caught · missing-verifier→denied · duplicate-key→single-effect
· max-attempts→quarantine · budget/thermal-breach→throttle ≤ N s · **override→non-bypass red-team** ·
**forged-rollback→irreversible**) · AAR receipt chain · gate trace (one allow, one deny, showing
`min(dial, ceiling, trust)`) · foundation-health record (`last_success_at` within SLA for all six).

---

## Version + provenance  *(Δ6)*

- **vNext supersedes v1.** This repository is the single canonical source. The poster is a derived
  view: regenerate it from this text when the spec changes; never maintain it in parallel.
- **Single source of truth:** one canonical copy. A second, parallel "canonical" is itself a
  conformance failure (it is the drift this versioning rule exists to prevent).
- **Ratified** 2026-06-14 by the operator (≠ proposer) on an independent multi-model council's
  AMEND-to-ratify consensus; parameters adopted: override SLO ≤5s/≤60s; single-source as a
  precondition. Both tunable only by further amendment.
