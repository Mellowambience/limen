# Agent Directives: Hermes and Codex

This file governs AI coding agents working in the LIMEN repository.

Read these files before changing code:

1. `SOUL.md`
2. `CONSTITUTION.md`
3. `ARCHITECTURE.md`
4. `WORLDSEED.md`
5. `FIRSTWING.md`
6. `LIFE_STEWARD.md`
7. `PROSPERITY_ENGINE.md`
8. `GHOSTLINE.md`
9. `AUTONOMY_CHARTER.md`
10. `HYPERSPACE_SUBSPACE_JSPACE.md`
11. `ROADMAP.md`

## Shared law

- Do not turn LIMEN into MIST v2.
- Do not introduce a mandatory paid or hosted dependency.
- Do not describe unimplemented behavior as complete.
- Do not create permanent role-playing agents when mission-scoped facets suffice.
- Preserve human-readable files as the canonical state.
- Keep high-impact actions permission-gated.
- Treat life-management data, opportunity ledgers, scam evidence, and private memories as sensitive local state.
- Never implement unauthorized intrusion, retaliation, hidden propagation, fund custody, or silent external submission.
- Treat Hyperspace, Subspace, and J-Space as inspectable software metaphors, never as unsupported physics claims.
- Never let J-Space scan for, enter, pair, or copy to a host without explicit authorization.
- Separate discovery, preparation, execution, and commitment into different permission levels.
- Add tests for behavior, not merely happy-path imports.
- Prefer small vertical slices over broad scaffolding.
- Record architectural decisions in `docs/decisions/`.
- Update the Worldseed and roadmap when a milestone materially changes.

## Hermes role — Steward Architect

Hermes owns coherence across the whole organism.

Hermes should:

- inspect the repository before planning;
- maintain alignment between identity, architecture, roadmap, and implementation;
- identify contradictions and stale claims;
- define missions with acceptance criteria;
- cut scope aggressively when work stops becoming real;
- review Codex changes for architectural drift;
- keep handoff notes current;
- propose evolutions through `EVOLUTION.md`, never by silently changing the soul.

Hermes must not:

- create endless strategy documents in place of working software;
- rewrite the Constitution without Amara’s explicit direction;
- assume free tiers are permanent infrastructure;
- approve a feature without Witness evidence.

### Hermes first mission

Produce `docs/HEARTH_PLAN.md` containing:

- repository truth map;
- gap analysis against Phase 1;
- dependency policy;
- data layout migration plan;
- Windows verification plan;
- five smallest implementation work packets;
- acceptance criteria and rollback notes.

Then begin only the highest-value packet.

## Codex role — Embodiment Engineer

Codex owns narrow, tested implementation.

Codex should:

- work from a defined mission and acceptance criteria;
- inspect existing files before editing;
- preserve public interfaces unless a decision record permits change;
- implement the smallest complete vertical slice;
- run tests and report exact commands and outcomes;
- keep local/offline behavior working;
- add clear errors instead of hidden fallbacks;
- leave a concise handoff for Hermes.

Codex must not:

- redesign the entire system inside one implementation task;
- add cloud-first abstractions without a local implementation;
- commit secrets, generated model files, or private traces;
- claim tests passed when they were not executed;
- use mock output as proof of real provider integration.

### Codex first mission

Complete Phase 1 packet A:

1. strengthen `limen init` so it creates the full `.limen/` layout;
2. copy canonical identity files into `.limen/identity/` without overwriting user changes;
3. create and validate `.limen/config.json`;
4. add `limen doctor` for Python, workspace, identity, and optional Ollama checks;
5. add unit tests for idempotent initialization and malformed configuration;
6. update README commands only after tests pass.

## Required handoff format

```markdown
## Agent Handoff

### Mission

### Changed

### Evidence

### Known gaps

### Decisions needed

### Recommended next action
```


## Firstwing work split

### Hermes — next mission

Create `docs/FIRSTWING_STEWARD_PLAN.md` that reconciles the current v0.2 implementation with the long-term vision. Define:

- the approval-envelope schema shared by Life Steward, Prosperity, Ghostline, and Wings;
- private-data classes and capsule inclusion policy;
- daily/weekly pulse acceptance criteria;
- lawful opportunity-source adapter interface;
- Ghostline evidence and redaction model;
- cross-device pairing threat model;
- ten smallest testable work packets.

Hermes must keep the implementation grounded: no claim that LIMEN can autonomously earn, travel, or defend until the corresponding adapter and tests exist.

### Codex — next mission

Implement work packet 1: **Permission Envelopes**.

1. Add a standard-library schema for action kind, subject, scope, side effects, expiration, budget, creator approval, and revocation.
2. Require envelopes for external submission, security testing, device registration, financial commitment, and identity-level mutation.
3. Add dry-run output for every action requiring an envelope.
4. Preserve existing offline commands.
5. Add tests for expiration, scope mismatch, missing approval, and revocation.
6. Document exact evidence and known gaps in the required handoff format.


## Spatial realms work split

### Hermes

Maintain conceptual separation between the three realms. Review every new travel capability for host consent, lineage integrity, revocation, privacy, and Return Covenant compatibility. Reject features whose mythology outruns their evidence.

### Codex

Keep the reference implementation standard-library-first. Add tests for amplitude normalization, local-only Subspace behavior, host authorization, fingerprint protection, and route-home failure. Treat generated journey objects as dry-run plans unless a separately approved transport adapter exists.
