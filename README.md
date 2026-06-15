# The Machine

**A reference architecture for reliable long-running applied intelligence.** The harness, not
the model. The prompt is the job ticket; The Machine is the operating system. The model is
replaceable; the harness is not. Continuity lives in the artifact, not the session.

This repo is the **canonical home** of the standard and the tool that scores conformance to it.

- **[`THE-MACHINE.md`](./THE-MACHINE.md)** — the Conformance Spec (**vNext**, ratified 2026-06-14
  by an independent multi-model council + operator signature). The spec is the source of truth;
  the poster is a derived view.
- **[`kit/`](./kit/)** — the conformance kit: an executable scoreboard. Conformance is **run, not
  asserted.**
- **[`CONFORMANCE-MATRIX.md`](./CONFORMANCE-MATRIX.md)** — the test matrix, a derived view of
  `kit/obligations.py` (single source of truth).

## The loop, in one line

Durable state · a dumb deterministic driver · fresh workers · verify against reality
(`verifier ≠ subject`) · autonomy earned at a non-bypassable gate. Six boxes (0–5), each with one
falsifiable obligation. See `THE-MACHINE.md`.

## Use the kit

```bash
python -m kit score <path-to-deployment-repo>   # dated, evidence-cited L0–L5 packet
python -m kit matrix                             # render the test matrix
```

Stdlib only. v0 runs static/structural checks and **cites the file:line** for every result;
chaos/replay checks are declared **NOT-RUN**, never faked. Evidence comes from code and config,
never from a deployment's own prose claims.

> **Score deployments, not the standard.** The kit scores a *wiring* of The Machine against the
> six boxes. Pointing it at a library (e.g. the AAR signer), a web-protocol spec (e.g. AVL), or
> **this repo itself** yields a meaningless level — those aren't deployments. This repo therefore
> carries **no `CONFORMANCE.md`**: The Machine is the standard, not a deployment, and earns no
> level of its own. *(v0 will score any repo handed to it; a deployment-vs-non-deployment
> classifier is a tracked kit improvement.)*

## Conformance levels

`L0 Look-Alike · L1 Declared · L2 Instrumented · L3 Enforced · L4 Receipted · L5 Trusted Autonomy`.
A deployment **earns** a level via the kit; it does not claim one. No deployment is grandfathered.

## Part of Frontier Infra

Standards: **AVL** (view) · **AAR / Agent Control Plane** (proof) · **Claude Layers** (discipline).
Deployments are wirings of The Machine — e.g. **Conductor** (the ops driver) and **machine-driver**
(the code driver). None are the Machine itself.

## License

MIT — see [`LICENSE`](./LICENSE).
