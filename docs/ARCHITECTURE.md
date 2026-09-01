# Architecture v0.1

## Boundaries

| Component | Responsibility |
|---|---|
| Memoria.ia | Memory, state, semantic context, episodes, provenance and confidence |
| M2A2 / MA2A | Identity, certificates, organizations, permissions, federation and transport |
| resolutive-routing | Select an admissible destination and explain the decision |

The router consumes trusted node metadata from M2A2 and capability summaries from Memoria.ia. It does not persist memories or create identities.

## Decision pipeline

1. Validate availability and privacy policy.
2. Reject nodes missing required knowledge, model, compute or latency constraints.
3. Score only admissible nodes.
4. Sort by score and then by stable node identifier.
5. Return the winner, all candidate scores and all rejection reasons.
6. Return an explicit fallback result if no M2A2 node is valid.

Policy is a hard filter. It cannot be compensated by lower cost, lower latency or higher hardware capability.

## Experimental score

The v0.1 score combines available compute, latency, reputation, advertised knowledge/model compatibility, cost and a bounded credit-balance factor. A bounded preference is added for the local node. Weights are provisional experimental constants, not an economic protocol.

## Ledger

Compute, storage and knowledge credits remain distinct. A successful contribution receives `work_units × quality`; a failed contribution receives 10% in the prototype to represent partial measurable work. This rule is deliberately simple and must be replaced only after measurement.

## Security boundary

This prototype makes routing decisions over already trusted metadata. It does not execute remote code, verify hardware claims, authenticate nodes, encrypt transport or settle payments.
