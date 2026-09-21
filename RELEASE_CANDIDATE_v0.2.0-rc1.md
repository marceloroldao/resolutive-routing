# resolutive-routing v0.2.0-rc1 — Release Candidate Gate

Status: PRE-RELEASE / EXPERIMENTAL

## Candidate scope

This release candidate freezes the routing decision boundary consumed by MA2A resilient execution.

The code line starts from routing main commit `d5bb5a5be495002836817780d10a3d8abb6e4ef3` and adds release hardening/metadata only.

## Required gates

- [x] v0.2 routing ownership boundary documented in `docs/ROUTING_CONTRACT_V0.2.md`.
- [x] C++20 deterministic routing core implemented.
- [x] Python/C++ routing parity test present.
- [x] Deterministic reroute after node failure implemented.
- [x] Cumulative exclusion prevents immediate reuse of failed nodes.
- [x] Authenticated MA2A failure-notice adapter implemented.
- [x] Native authenticated failure-to-reroute test present.
- [x] Python MA2A adapter remains a normalization boundary rather than transport ownership.
- [x] Route-quality corpus/metrics/comparison tooling present.
- [x] Package version prepared as `0.2.0rc1`.
- [x] Zenodo metadata identifies v0.1 as the previous version rather than reusing its DOI.
- [ ] Release-mode C++ assertion guard green in CI.
- [ ] Python CI green on 3.10, 3.11, 3.12 and 3.13.
- [ ] C++ core CI green with assertions active.
- [ ] MA2A release candidate pins this routing snapshot exactly.
- [ ] Git tag / GitHub release `v0.2.0-rc1` created.
- [ ] Zenodo archival DOI minted for the exact tagged snapshot.

## Frozen responsibility boundary

`resolutive-routing` owns:

- admissibility and policy filtering;
- deterministic candidate scoring;
- route selection;
- deterministic rerouting with excluded nodes;
- explainable routing decisions;
- routing-quality evaluation.

MA2A owns:

- identity and certificates;
- authentication and authorization;
- capability-advertisement transport;
- peer discovery and sessions;
- TCP/network transport;
- job execution;
- failure detection and failure authenticity;
- signed results and receipts.

Memoria.ia owns memory/state semantics.

## Known limitations

- Node capability snapshots are trusted inputs supplied by an authorized external layer; routing does not independently attest hardware claims.
- The project is not a peer-discovery service, transport stack, scheduler, distributed database or payment system.
- Current benchmarks are diagnostic and environment-specific.
- No independent production-security audit is claimed by this release candidate.

## Release rule

The `v0.2.0-rc1` tag must be created only after the assertion-enabled CI is green and MA2A is pinned to the exact routing snapshot. The archived v0.1 DOI must not be presented as the v0.2 DOI.
