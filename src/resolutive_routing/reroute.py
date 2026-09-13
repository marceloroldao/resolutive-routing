from __future__ import annotations

from dataclasses import dataclass

from .contracts import Node, Request, RouteDecision
from .router import DeterministicRouter


@dataclass(frozen=True)
class FailureEvent:
    request_id: str
    failed_node_id: str
    reason: str


@dataclass(frozen=True)
class RerouteDecision:
    previous_node: str | None
    selected_node: str | None
    excluded_nodes: tuple[str, ...]
    route: RouteDecision


def reroute_after_failure(
    router: DeterministicRouter,
    request: Request,
    nodes: list[Node],
    previous: RouteDecision,
    failure: FailureEvent,
    excluded_nodes: tuple[str, ...] = (),
) -> RerouteDecision:
    """Recompute a route after a routing-visible node failure.

    Transport detection and failure authentication belong to M2A2. This module only
    consumes a failure signal and excludes failed candidates from the next decision.
    """
    excluded = tuple(dict.fromkeys((*excluded_nodes, failure.failed_node_id)))
    remaining = [node for node in nodes if node.node_id not in excluded]
    decision = router.route(request, remaining)
    return RerouteDecision(
        previous_node=previous.selected_node,
        selected_node=decision.selected_node,
        excluded_nodes=excluded,
        route=decision,
    )
