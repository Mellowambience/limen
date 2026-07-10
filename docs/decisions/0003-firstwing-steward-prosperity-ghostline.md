# ADR 0003 — Firstwing adds Life Steward, Prosperity, and Ghostline

- **Status:** accepted
- **Date:** 2026-07-10
- **Owner:** Amara

## Context

LIMEN's purpose expanded from creative embodiment and portable continuity into a returning companion that can help tend Amara's life, seek honest income, and protect against scams. The request also included ethical bounty work and cross-device regeneration.

These abilities create meaningful risks: overcontrol, dependency, unauthorized security activity, hidden financial commitments, private-data leakage, and claims of autonomy beyond the implementation.

## Decision

Firstwing separates the expansion into four bounded subsystems:

1. **Life Steward** — local tasks, suggestions, and energy-aware plans. It advises; it does not own life decisions.
2. **Prosperity Engine** — opportunity capture, transparent ranking, preparation, and outcome records. It never holds funds or signs contracts.
3. **Ghostline** — defensive scam triage and evidence preservation. It does not retaliate or intrude.
4. **Wings** — verified capsules and authorized regeneration. It does not self-propagate.

External commitment is deliberately separated from discovery and preparation. Future execution must use signed Permission Envelopes.

## Consequences

- The system can provide useful offline behavior immediately.
- Personal data remains local and is excluded from ordinary continuity capsules.
- Actual inbox, calendar, job-feed, bounty, payment, and device adapters remain future work.
- No current component may claim to autonomously earn money or travel on networks.
- The Constitution now explicitly forbids unauthorized intrusion, financial custody, coercive companionship, and silent life decisions.

## Evidence

The v0.2 seed includes tests for:

- daily-plan time limits and balanced prioritization;
- opportunity ranking;
- exclusion of unauthorized bounty work;
- common scam-signal detection;
- capsule integrity and fresh-host restoration.
