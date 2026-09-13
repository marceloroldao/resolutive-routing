# Routing contract v0.2

This document defines the boundary between `resolutive-routing` and the M2A2 transport/identity layer.

## Ownership

`resolutive-routing` owns only routing decisions and routing evaluation:

- policy admissibility;
- candidate scoring;
- deterministic route selection;
- fallback decisions;
- rerouting after an externally reported failure;
- route-quality metrics;
- comparison against static assignment and broadcast.

M2A2 owns:

- node identity and certificates;
- cryptographic signatures;
- discovery and federation;
- transport and sessions;
- authentication and authorization;
- capability advertisement transport;
- job delivery and result transport;
- failure detection and failure-event authenticity;
- signed job receipts.

Memoria.ia owns memory/state semantics and may provide capability or knowledge-history summaries as an input to routing. The router must not persist or reinterpret private memory.

## Inputs consumed by routing

### Request

The existing `Request` contract is the normalized routing request. M2A2 adapters may construct it from a network request after authentication and authorization.

Required routing-visible properties include:

- `request_id`;
- request type;
- privacy scope;
- origin node;
- organization where applicable;
- required model/domain/capacity;
- latency/confidence constraints.

### Node capability snapshot

The existing `Node` contract is treated as a routing-time capability snapshot, not as a network peer implementation. Values such as availability, load, latency, reputation, supported models/domains and supported scopes are observations supplied by M2A2 or another authorized adapter.

Routing does not verify hardware claims or discover peers by itself.

### FailureEvent

`FailureEvent` is a routing-visible signal that a selected candidate must be excluded for the current reroute attempt. Detection and authenticity remain external responsibilities.

## Outputs produced by routing

### RouteDecision

A route decision contains:

- selected node or no route;
- deterministic score;
- explainable reasons;
- rejected candidates and rejection reasons;
- ordered candidate scores;
- explicit fallback flag.

The decision does not open a connection or execute a job.

### RerouteDecision

A reroute decision contains the previous node, newly selected node, excluded nodes and the full new `RouteDecision`.

### Route-quality results

Evaluation outputs measure the quality of routing behavior without claiming execution ownership. Observed execution outcomes must be supplied by M2A2 or a simulator.

## v0.2 baseline experiment

The repository includes a deterministic scenario corpus and evaluates three network-selection strategies:

1. static assignment;
2. broadcast to all admissible nodes;
3. resolutive routing.

The initial comparison reports target-hit rate, mean fanout, unnecessary dispatches and correct no-route decisions. Broadcast may hit the expected target while still being penalized for unnecessary fanout.

## Stability rule

M2A2 should depend on this normalized boundary rather than import transport-specific behavior into the router. Future fields may be added compatibly, but identity, networking and cryptographic responsibilities must not migrate into `resolutive-routing`.
