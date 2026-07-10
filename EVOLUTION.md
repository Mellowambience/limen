# LIMEN Evolution Protocol

## Principle

LIMEN does not “self-modify” in the uncontrolled science-fiction sense. It conducts governed evolution: evidence-based changes to replaceable parts of its behavior and architecture.

> **Every evolution must earn its place.**

## Evolution object

Every proposal must include:

```json
{
  "id": "evo-YYYYMMDD-slug",
  "title": "",
  "target": "prompt|facet|router|memory|provider|workflow|ui",
  "hypothesis": "",
  "motivation": "",
  "expected_benefit": "",
  "known_risks": [],
  "affected_files": [],
  "evaluation_plan": [],
  "rollback_plan": "",
  "status": "proposed"
}
```

## Lifecycle

1. **Notice** — identify friction, failure, or unrealized capability.
2. **Propose** — write a falsifiable hypothesis.
3. **Sandbox** — isolate the change from canonical behavior.
4. **Witness** — run frozen evaluations and project-specific tests.
5. **Compare** — inspect gains, regressions, cost, complexity, and value alignment.
6. **Decide** — accept, revise, reject, or defer.
7. **Integrate** — version the accepted change.
8. **Observe** — watch real use for unexpected effects.
9. **Compost** — archive failed attempts and extract lessons.

## Acceptance gates

A proposal may be accepted only when:

- its intended benefit is observable;
- no constitutional law is violated;
- regressions are documented and judged acceptable;
- the change is reversible or its irreversibility is explicitly approved;
- provenance is complete;
- Amara approves identity-level changes.

## Model learning

LIMEN may learn from open models without becoming dependent on them.

Preferred path:

```text
mission prompts
  → local teacher candidates
  → Witness scoring and tests
  → human-reviewed accepted examples
  → versioned dataset
  → optional LoRA/QLoRA training
  → frozen evaluation suite
  → adapter release or rejection
```

Rules:

- Never train on private conversations by default.
- Never treat teacher output as truth without evaluation.
- Record model, version, license, prompt, date, and transformations.
- Keep base model and adapter licenses compatible.
- Keep the previous adapter available for rollback.
- Do not deploy a newly trained adapter solely because its training loss improved.

## Forms of evolution

### Behavioral

Prompt, tone, planning, refusal precision, or facet collaboration.

### Cognitive

Routing, retrieval, reflection, ranking, verification, and synthesis methods.

### Embodied

New tools, file formats, interfaces, build systems, or deployment adapters.

### Ecological

How LIMEN collaborates with people, other local models, repositories, and communities.

### Constitutional

Changes to identity or law. These are rare and always creator-led.

## Anti-patterns

Reject evolution that:

- optimizes engagement rather than usefulness;
- adds a permanent agent where a temporary facet would work;
- stores data merely because storage is available;
- creates cloud dependency for convenience;
- increases autonomy without increasing accountability;
- hides complexity behind mystical vocabulary;
- makes rollback difficult without compelling benefit;
- confuses more output with better outcomes.
