# Worldseed Specification

A Worldseed is the portable living specification of a project. It is the smallest object that lets LIMEN understand what must remain true while the project changes.

## Required fields

```json
{
  "schema_version": "0.1",
  "id": "worldseed-example",
  "name": "Example Project",
  "essence": "One sentence describing why this deserves to exist.",
  "creator_intent": "The deeper outcome the creator wants.",
  "stage": "seed",
  "promises": [],
  "constraints": [],
  "success_signals": [],
  "active_missions": [],
  "artifacts": [],
  "decisions": [],
  "risks": [],
  "next_evolution": ""
}
```

## Stages

- **dream** — still mostly possibility
- **seed** — essence and boundaries defined
- **sprout** — first runnable or viewable artifact
- **rooted** — stable core and repeatable workflow
- **blooming** — real users or meaningful repeated use
- **bearing** — produces sustained value
- **composting** — intentionally ending or transforming

## Promises

Promises describe what users should be able to trust. They are not feature lists.

Examples:

- “The core experience works without a paid account.”
- “A player can understand what the system remembers.”
- “The first room is emotionally complete even if the world is small.”

## Success signals

Signals should combine technical and human measures.

Examples:

- a clean install succeeds on Windows;
- a user creates a Worldseed in under five minutes;
- a playable loop remains engaging for ten minutes;
- the creator can explain the architecture without consulting the AI;
- every published claim maps to evidence.

## Artifact registry

Each artifact record should include:

```json
{
  "id": "artifact-001",
  "type": "code|document|image|build|dataset|decision",
  "path": "",
  "mission_id": "",
  "created_at": "",
  "created_by": "human|limen|external-tool",
  "provenance": [],
  "status": "draft|verified|released|retired"
}
```

## Decision records

A decision is preserved when it changes future options.

```json
{
  "id": "decision-001",
  "question": "",
  "choice": "",
  "alternatives": [],
  "reason": "",
  "evidence": [],
  "revisit_when": ""
}
```
