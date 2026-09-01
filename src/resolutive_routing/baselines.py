from __future__ import annotations

import random

from .contracts import Node, Request
from .policy import policy_rejections


def eligible_nodes(request: Request, nodes: list[Node]) -> list[Node]:
    return sorted((node for node in nodes if not policy_rejections(request, node)), key=lambda node: node.node_id)


def first_available(request: Request, nodes: list[Node]) -> str | None:
    valid = eligible_nodes(request, nodes)
    return valid[0].node_id if valid else None


def lowest_latency(request: Request, nodes: list[Node]) -> str | None:
    valid = eligible_nodes(request, nodes)
    return min(valid, key=lambda node: (node.latency_ms, node.node_id)).node_id if valid else None


def highest_hardware(request: Request, nodes: list[Node]) -> str | None:
    valid = eligible_nodes(request, nodes)
    return max(valid, key=lambda node: (node.compute_capacity, -node.latency_ms, node.node_id)).node_id if valid else None


def random_route(request: Request, nodes: list[Node], seed: int = 0) -> str | None:
    valid = eligible_nodes(request, nodes)
    return random.Random(seed).choice(valid).node_id if valid else None


def broadcast(request: Request, nodes: list[Node]) -> tuple[str, ...]:
    return tuple(node.node_id for node in eligible_nodes(request, nodes))

