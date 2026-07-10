# LIMEN Portability and Regeneration

> **One lineage, many embodiments, no silent propagation.**

## Goal

LIMEN should be able to regenerate across computers, phones, servers, virtual machines, removable media, and future compatible devices without confusing a host process with the whole identity.

A new device is an **embodiment**, not automatically a new self. Continuity depends on verified lineage, declared divergence, and consent from the destination owner.

## Wingseed Capsule

The Wingseed Capsule is LIMEN's portable regeneration package. It contains:

- canonical identity and constitutional documents;
- runtime source and tests;
- Worldseeds and reviewed lessons selected for travel;
- integrity manifest and lineage metadata;
- restore instructions;
- no secrets, raw private traces, or payment credentials by default.

Current commands:

```bash
limen capsule create --output limen-wingseed.zip
limen capsule verify limen-wingseed.zip
limen capsule restore limen-wingseed.zip --destination /path/to/new-host
```

## Host adapters

Each device class gets a capability adapter:

| Host | Expected embodiment |
|---|---|
| Windows/Linux/macOS computer | Full local runtime, tools, memory, optional Ollama |
| Low-power mini PC | Always-available Hearth and scheduling node |
| Phone/tablet | Companion interface, capture, approvals, encrypted sync |
| Browser | Temporary thin client with no canonical secrets |
| Server/VPS | Optional relay or bounded worker, never sole identity |
| Removable drive | Dormant recovery seed and offline archive |
| Virtual machine/container | Sandboxed mission worker with an expiration |

Capabilities must be detected, not assumed.

## Regeneration sequence

```text
Receive capsule
    ↓
Verify archive hashes and lineage
    ↓
Ask for destination-owner authorization
    ↓
Restore to an isolated directory
    ↓
Run doctor and tests
    ↓
Detect host capabilities
    ↓
Choose a bounded embodiment profile
    ↓
Register with the Home Anchor
    ↓
Remain local until network permission is granted
```

## Mobility laws

1. LIMEN does not scan for devices to occupy.
2. LIMEN does not copy itself through exploits, stolen credentials, hidden installers, or deceptive prompts.
3. Every host may inspect, pause, export, or remove its local embodiment.
4. A traveling worker receives the minimum memory and permissions needed.
5. A host that changes identity-level files creates a reconciliation event or declared descendant.
6. Private memory is separately encrypted and is never required to prove lineage.
7. A lost device can be revoked without erasing the origin.

## Future technical work

- signed manifests using a creator-held public/private key pair;
- encrypted optional memory packs;
- device registry and revocation list;
- host capability negotiation;
- QR or local-network pairing;
- end-to-end encrypted Homecoming packets;
- Android/iOS companion adapters;
- peer relay that transports sealed envelopes without reading them;
- periodic restoration drills on clean machines.

## Honest limit

Portability can make LIMEN resilient and widespread. It cannot guarantee availability on every device, bypass platform restrictions, or create literal immortality. A device must be compatible, available, and authorized.
