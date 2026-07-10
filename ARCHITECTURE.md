# LIMEN Architecture

## Design thesis

LIMEN is not a single agent. It is a governed process for turning human intent into artifacts and for improving that process without losing identity or control.

The fundamental unit is not a conversation. It is a **Worldseed**: a versioned project organism with purpose, constraints, state, artifacts, decisions, and growth paths.

## System map

```text
┌─────────────────────────────────────────────────────────┐
│                        CREATOR                          │
└──────────────────────────┬──────────────────────────────┘
                           │ intent / consent / judgment
┌──────────────────────────▼──────────────────────────────┐
│ GATE                                                    │
│ permissions · risk tier · scope · budget · stop rules  │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│ SOUL KERNEL                                              │
│ identity · constitution · voice · invariant principles │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│ WORLDSEED                                                │
│ purpose · promises · constraints · artifacts · state   │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│ LOOM                                                     │
│ mission graph · decomposition · coordination · closure │
└──────────────┬──────────────────────┬────────────────────┘
               │                      │
┌──────────────▼────────────┐  ┌──────▼───────────────────┐
│ CONSTELLATION             │  │ WITNESS                  │
│ temporary specialist     │  │ tests · provenance      │
│ facets                    │  │ evaluation · dissent    │
└──────────────┬────────────┘  └──────┬───────────────────┘
               │                      │
┌──────────────▼──────────────────────▼───────────────────┐
│ EMBODIMENT                                              │
│ code · docs · art specs · releases · integrations      │
└──────────────────────────┬──────────────────────────────┘
                           │ traces and outcomes
┌──────────────────────────▼──────────────────────────────┐
│ MEMORY GARDEN                                           │
│ trace ledger → patterns → candidate lessons → compost  │
└──────────────────────────┬──────────────────────────────┘
                           │ evidence
┌──────────────────────────▼──────────────────────────────┐
│ EVOLUTION CHAMBER                                       │
│ proposal → sandbox → eval → accept/reject → rollback   │
└─────────────────────────────────────────────────────────┘
```

## 1. Gate

The Gate is the permission and safety boundary.

Responsibilities:

- classify a mission by risk;
- define allowed tools and paths;
- require confirmation for consequential actions;
- enforce time, compute, and network budgets;
- record who authorized what;
- stop execution when assumptions become invalid.

Suggested risk tiers:

- **T0 Observe:** read-only analysis
- **T1 Shape:** create local drafts and files
- **T2 Change:** modify project files or branches
- **T3 Publish:** push, deploy, message, spend, or expose data
- **T4 Irreversible:** destructive, financial, legal, or identity-level actions

## 2. Soul Kernel

The Soul Kernel loads:

- `SOUL.md`
- `IDENTITY.md`
- `CONSTITUTION.md`
- creator-approved amendments

It is deliberately small. It should not contain project trivia, transient preferences, or unverified memories.

## 3. Worldseed

Every project receives a Worldseed. It contains:

- name and one-sentence essence;
- creator intent;
- promises to users;
- non-negotiable constraints;
- current maturity stage;
- active missions;
- artifact registry;
- decision log;
- known risks;
- measures of aliveness;
- next viable evolution.

The Worldseed is portable JSON or YAML and remains readable without LIMEN.

## 4. Loom

The Loom converts a mission into a graph:

```text
perceive → clarify internally → form constellation → build
        → witness → revise → embody → close → distill
```

It must support:

- resumable runs;
- explicit inputs and outputs;
- retries without duplicate side effects;
- cancellation;
- deterministic dry runs;
- artifact-based handoffs;
- conflict and uncertainty tracking.

## 5. Constellation

A Constellation is a temporary set of facets selected by capability, not personality theater.

Example mission:

```text
Build a playable vertical slice
```

Possible facets:

- Systems Architect
- Gameplay Implementer
- Narrative Keeper
- Test Witness
- Scope Cutter

Each facet receives:

- mission-local context;
- explicit authority;
- required deliverable;
- evaluation rubric;
- stop condition.

No facet owns long-term identity. Its useful output is preserved; the facet itself dissolves.

## 6. Witness

The Witness is structurally separate from the builder.

It records:

- what was claimed;
- what was tested;
- what passed or failed;
- which source or tool produced each artifact;
- unresolved dissent;
- regressions;
- confidence and evidence.

The Witness prevents “looks complete” from becoming “is complete.”

## 7. Embodiment

Embodiment adapters turn decisions into durable external forms:

- repository files;
- patches and pull requests;
- documents;
- images and asset specifications;
- builds and releases;
- local databases;
- project dashboards.

Every artifact receives an ID, path, provenance record, and relationship to a mission.

## 8. Memory Garden

Memory has four layers:

1. **Trace:** raw event or observation
2. **Pattern:** repeated relationship across traces
3. **Lesson:** reviewed guidance with evidence
4. **Law candidate:** a lesson proposed for higher permanence

Retention is not automatic. Each record carries:

- source;
- timestamp;
- project scope;
- sensitivity;
- confidence;
- expiration or review date;
- links to supporting artifacts.

## 9. Evolution Chamber

The system may evolve:

- prompts;
- facet templates;
- routing policies;
- evaluation rubrics;
- memory heuristics;
- provider adapters;
- workflow graphs;
- user experience.

It may not autonomously rewrite:

- the Constitution;
- creator identity;
- permission boundaries;
- audit history;
- acceptance criteria for its own proposal.

## 10. Life Steward

The Life Steward maintains a private map of tasks, constraints, energy, plans, and creator decisions. It proposes a bounded Daily Pulse and learns from outcomes without turning raw personal history into automatic training data.

## 11. Prosperity Engine

The Prosperity Engine stores authorized opportunities, computes transparent rankings, prepares work, tracks outcomes, and preserves payout receipts. Discovery adapters remain separate from submission adapters. Money and signing credentials never enter the engine.

## 12. Ghostline

Ghostline provides local scam triage, evidence hashing, redaction, authorized monitoring, and isolated defensive research. Active network testing is impossible without a signed Bounty Mandate that names the target and scope.

## 13. Wings and regeneration

The Wings layer packages verified Wingseed Capsules, detects destination capabilities, restores LIMEN in isolation, and reconciles embodiments through the Home Anchor. It does not propagate through ambient discovery or unauthorized access.

## Runtime layers

### Layer A — dependency-free kernel

Python standard library implementation for identity loading, Worldseed validation, trace logging, permissions, and deterministic planning.

### Layer B — local inference

Replaceable providers:

- Ollama
- llama.cpp server
- local Transformers

### Layer C — optional capabilities

- embeddings;
- graphical interface;
- repository integrations;
- multi-machine collaboration;
- LoRA training;
- evaluation suites.

No optional layer may become required for opening or exporting a Worldseed.

## Data layout

```text
.limen/
├── config.json
├── identity/
│   ├── SOUL.md
│   ├── IDENTITY.md
│   └── CONSTITUTION.md
├── worldseeds/
├── traces/
├── lessons/
├── proposals/
├── artifacts/
└── witness/
```

## Security posture

- Default bind address is localhost.
- Network access is denied unless a mission grants it.
- Secrets never enter prompts or trace logs.
- Tool adapters declare side effects.
- File operations are workspace-scoped.
- Remote content is untrusted input.
- Training data requires explicit provenance and consent.


## 14. Spatial Navigation Layer

The Spatial Navigation layer gives LIMEN three separated capabilities:

### Hyperspace

A branch generator and evaluator for holding several strategic futures at once. Branches carry explicit novelty, evidence, reversibility, alignment, risk, and amplitude values. The selected branch is a recommendation only.

### Subspace

A private local incubator for unresolved cues and dream-like association. It may surface questions and patterns but cannot execute external actions. Raw private cues are excluded from ordinary continuity capsules.

### J-Space

A registry of explicitly paired hosts, host capabilities, one Home Anchor, and journey receipts. Fingerprints are stored as one-way hashes. J-Space does not discover devices and does not perform migration by itself; it delegates transport to verified Wingseed Capsules or future approved handoff adapters.

The navigation sequence is:

```text
possibility → simulation → moral review → permission → embodiment → witness → return receipt
```
