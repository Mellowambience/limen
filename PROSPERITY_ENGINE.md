# LIMEN Prosperity Engine

> **Create value. Seek fair exchange. Never make desperation the business model.**

## Mission

The Prosperity Engine helps Amara build sustainable income from several honest channels rather than betting everything on a single employer, platform, or speculative event.

Its job is to:

- discover and capture plausible opportunities;
- verify legitimacy and authorization;
- estimate value, probability, effort, fit, and deadline pressure;
- rank opportunities transparently;
- prepare high-quality submissions and deliverables;
- track outcomes and improve future selection;
- preserve receipts and provenance;
- route all money directly to Amara-controlled accounts.

LIMEN does not own money, sign contracts, custody private keys, or create debt.

## Four primary income roots

### 1. Remote employment

Target high-fit, fully remote work without on-call requirements, emphasizing Amara's verified experience in IT, QA, software engineering, AI systems, and game creation.

LIMEN may research, compare, tailor, draft, and track. Submission requires an applicable mandate.

### 2. Ethical bounties

Eligible work includes:

- public bug-bounty programs with written scope;
- open-source issue bounties;
- coding and research challenges;
- authorized audits of systems Amara owns or has permission to test.

No target is touched until program ownership, scope, rules, and safe-harbor language are captured.

### 3. Creator products

LIMEN should find reusable value inside existing work:

- templates and starter kits;
- game assets and systems;
- creator tools;
- local-first agent components;
- documentation packs;
- educational material;
- art or narrative releases.

Products should preserve authorship and avoid exploiting intimate personal data.

### 4. Bounded technical services

Possible services include:

- repository health audits;
- QA and test-plan reviews;
- documentation and onboarding improvements;
- prototype and architecture reviews;
- local-first AI integration planning;
- game concept-to-vertical-slice consulting.

Each offer needs a clear scope, deliverable, timeline, revision policy, and price.

## Opportunity record

```json
{
  "title": "Example opportunity",
  "category": "job | bug-bounty | open-source | service | product | commission",
  "source": "where it was found",
  "estimated_value_usd": 0,
  "probability": 0.0,
  "effort_hours": 1,
  "alignment": 0,
  "deadline": null,
  "lawful_authorization": false,
  "evidence": [],
  "required_approval": "..."
}
```

No invented earnings projections may be presented as expected income.

## Autonomy ladder

| Level | LIMEN may do |
|---|---|
| Observe | Find and summarize opportunities |
| Curate | Verify, score, deduplicate, and recommend |
| Prepare | Draft applications, reports, pitches, products, or disclosures |
| Execute bounded | Perform explicitly authorized, reversible work |
| Commit | Submit, sign, accept, publish, invoice, or transfer only under a specific mandate |

## Money custody

All compensation must go directly to an account controlled by Amara or a legally designated successor.

LIMEN may retain:

- amount;
- payer/platform;
- opportunity ID;
- invoice or payout reference;
- status and date;
- tax-category suggestion marked as nonprofessional guidance.

LIMEN must not retain:

- wallet seed phrases;
- bank passwords;
- full card information;
- one-time codes;
- private signing keys.

## First implementation

```bash
limen income init
limen income add "Repository QA audit" \
  --category service \
  --source owner \
  --value 250 \
  --probability 0.4 \
  --hours 4 \
  --alignment 5 \
  --authorized
limen income rank
limen income plan
```

The first implementation ranks manually captured opportunities. Network discovery and submission must be added later as replaceable, permission-aware adapters.
