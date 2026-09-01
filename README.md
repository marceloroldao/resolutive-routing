# resolutive-routing

Experimental routing layer for the M2A2 / Resolutive ecosystem.

## Purpose

`resolutive-routing` is intended to decide **where a request should be resolved** across a network of heterogeneous nodes.

The router must eventually consider two distinct but related questions:

1. **Who knows the answer?**
2. **Who can process the request most efficiently now?**

The project is not yet a general distributed-compute implementation. Its first role is to formalize the contracts, metrics and routing rules required before multi-node experiments begin.

## Initial architecture

```text
request
  |
  v
Resolutive Router
  |
  +--> local memory / Memoria.ia
  +--> organization memory
  +--> public M2A2 knowledge
  +--> remote local-LLM node
  +--> remote compute node
  +--> optional cloud fallback
```

The router should avoid global broadcast when a sufficiently good route is known.

## ECHO routing

The future public-network query primitive is provisionally called `ECHO` / `ECHO_REQ`.

An ECHO should represent a public or otherwise authorized knowledge request, not a dump of private conversation context.

A router may use learned knowledge-density/capability information to decide which nodes are promising candidates for an ECHO.

Conceptually:

```text
ESP32
  -> microcontrollers
  -> electronics
  -> candidate nodes
```

## Compute routing

The router may also select nodes according to available compute capacity.

Potential inputs include:

- model/capability available;
- CPU/GPU/NPU class;
- free RAM/VRAM;
- current load;
- expected tokens/second or equivalent throughput;
- latency/network distance;
- privacy scope;
- organization policy;
- node reputation;
- current credit/debt balance;
- energy/cost policy.

A simple request may be routed to a small local model while a harder request may require a larger remote model. Cloud LLMs remain an optional fallback, not the default assumption.

## M2A2 reciprocity / credit ledger

A node may consume resources from the M2A2 network and later compensate the network by contributing resources when its hardware is idle.

Examples of contributions:

- local LLM inference;
- CPU/GPU/NPU processing;
- authorized storage;
- public-memory retrieval;
- validated public knowledge;
- other measurable network services.

Do **not** equate network credits directly with OpenAI/Gemini prompt tokens. A model token is not a stable unit of computational work across models and hardware.

Initial accounting should use an internal ledger rather than cryptocurrency or a financial token.

Suggested logical balances:

```text
compute_credit
storage_credit
knowledge_credit
```

A future unified balance may be derived from those dimensions, but the underlying measurements should remain auditable.

### Example

```text
Node A

compute used        -5000
knowledge used      -1200
storage used         -300

compute contributed +4200
knowledge supplied  +1500
storage supplied     +400
```

The node can therefore be a consumer at one time and a producer at another, similar to bidirectional balancing in an electrical grid.

## Credit valuation

A future compute-credit formula should reflect real work rather than token count alone. Candidate factors include:

```text
credit = work_units
       * capability_factor
       * quality_factor
       * availability_factor
       * reputation_factor
```

Any normalization formula must be benchmarked before becoming a protocol rule.

## Knowledge contribution

Validated knowledge discovered from public sources may contribute value to the network if it prevents repeated searches or repeated inference.

Public knowledge should retain provenance and may have states such as:

- `candidate`
- `confirmed`
- `contested`
- `deprecated`

Private/personal memory must not be converted into public credit merely because similar private information exists on multiple nodes.

## Reputation

Routing and compensation should eventually consider verifiable service quality, including:

- uptime;
- latency;
- completed jobs;
- failed jobs;
- correctness/validation results;
- integrity;
- dispute rate.

Claims about hardware or capability should not be trusted solely because a node advertises them.

## Privacy scopes

Resource routing must respect scope before cost or credit optimization.

Suggested scopes:

```text
PUBLIC
ORGANIZATION
PRIVATE
LOCAL_ONLY
```

Possible policy:

```text
PUBLIC       -> eligible for federated routing
ORGANIZATION -> only authorized organization nodes
PRIVATE      -> trusted/private nodes only
LOCAL_ONLY   -> never leaves the device
```

A cheaper route must never override privacy policy.

## Relationship with Memoria.ia and M2A2

```text
Memoria.ia
  -> owns memory/state semantics

M2A2 / MA2A
  -> owns network identity, federation and authorized exchange

resolutive-routing
  -> selects the best admissible route for knowledge or compute
```

`resolutive-routing` should not duplicate Memoria.ia or become the database itself.

## Development trigger

The repository is being initialized now to preserve the architecture and contracts.

Implementation should remain incremental. The first serious routing implementation should begin when at least two real nodes can exchange requests/jobs and we can measure whether routing beats global broadcast or fixed static assignment.

## First experiments

Recommended initial experiments:

1. two local nodes with different capabilities;
2. deterministic capability advertisement;
3. route selection without broadcast;
4. job accounting and receipt generation;
5. compute-credit ledger simulation;
6. privacy-scope enforcement;
7. node failure and rerouting;
8. compare static routing vs resolutive routing;
9. later add public-knowledge ECHO routing.

## Non-goals for the first version

Do not begin with:

- cryptocurrency;
- blockchain consensus;
- real-money settlement;
- anonymous public compute marketplace;
- unrestricted execution of arbitrary code on third-party nodes;
- global network flooding;
- replacement of M2A2 identity/security contracts.

The immediate objective is simpler:

> Prove that heterogeneous M2A2 nodes can advertise spare capacity, receive authorized work, return verifiable results, and maintain a fair auditable resource balance while the router selects an efficient admissible path.


## Prototype v0.1

The first executable prototype is intentionally small and dependency-free. It includes:

- typed request and node contracts;
- policy-first deterministic routing;
- explainable decisions and explicit fallback;
- separate compute, storage and knowledge credit accounting;
- five routing baselines;
- a deterministic three-node simulator;
- tests and a reproducible microbenchmark.

### Run locally

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m resolutive_routing.simulator
python -m resolutive_routing.benchmark
```

Python 3.10 or newer is required. See [architecture](docs/ARCHITECTURE.md), [benchmark protocol](docs/BENCHMARKS.md), [roadmap](docs/ROADMAP.md) and [changelog](CHANGELOG.md).

### Current status

Version 0.1 is a research baseline, not a distributed network or production scheduler. Identity and transport remain M2A2 responsibilities; memory remains a Memoria.ia responsibility. Timing measurements are diagnostic and must not be interpreted as unsupported performance claims.
