from __future__ import annotations

from collections.abc import Mapping

from .contracts import Node, Scope
from .reroute import FailureEvent


def node_from_ma2a_capability(
    capability: Mapping[str, object],
    *,
    latency_ms: float,
    trusted: bool,
    reputation: float = 1.0,
    cost: float = 0.0,
    credit_balance: float = 0.0,
    is_local: bool = False,
) -> Node:
    """Convert a verified MA2A capability advertisement into a routing candidate.

    Cryptographic verification belongs to MA2A. Observed/trust-derived values are
    supplied separately so a remote node cannot self-assert latency, trust or reputation.
    """
    required = {
        "node_id",
        "organization_id",
        "available",
        "compute_capacity",
        "current_load",
        "models",
        "memory_domains",
        "supported_scopes",
    }
    missing = required.difference(capability)
    if missing:
        raise ValueError(f"missing MA2A capability fields: {', '.join(sorted(missing))}")

    try:
        scopes = frozenset(Scope(str(value)) for value in capability["supported_scopes"])
        models = frozenset(str(value) for value in capability["models"])
        memory_domains = frozenset(str(value) for value in capability["memory_domains"])
        node_id = str(capability["node_id"])
        organization_raw = capability["organization_id"]
        organization_id = None if organization_raw is None else str(organization_raw)
        available = bool(capability["available"])
        compute_capacity = float(capability["compute_capacity"])
        current_load = float(capability["current_load"])
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid MA2A capability values") from exc

    if not node_id:
        raise ValueError("empty MA2A node_id")
    if compute_capacity < 0:
        raise ValueError("negative MA2A compute capacity")
    if not 0.0 <= current_load <= 1.0:
        raise ValueError("MA2A current_load must be between 0 and 1")
    if latency_ms < 0:
        raise ValueError("negative observed latency")
    if reputation < 0:
        raise ValueError("negative reputation")

    return Node(
        node_id=node_id,
        organization_id=organization_id,
        is_local=is_local,
        available=available,
        trusted=trusted,
        compute_capacity=compute_capacity,
        current_load=current_load,
        latency_ms=float(latency_ms),
        reputation=float(reputation),
        cost=float(cost),
        credit_balance=float(credit_balance),
        models=models,
        memory_domains=memory_domains,
        supported_scopes=scopes,
    )


def failure_from_ma2a_notice(notice: Mapping[str, object]) -> FailureEvent:
    """Convert an already verified MA2A failure notice into a routing event."""
    required = {"request_id", "failed_node_id", "reason"}
    missing = required.difference(notice)
    if missing:
        raise ValueError(f"missing MA2A failure fields: {', '.join(sorted(missing))}")
    request_id = str(notice["request_id"])
    failed_node_id = str(notice["failed_node_id"])
    reason = str(notice["reason"])
    if not request_id or not failed_node_id or not reason:
        raise ValueError("empty MA2A failure field")
    return FailureEvent(request_id, failed_node_id, reason)
