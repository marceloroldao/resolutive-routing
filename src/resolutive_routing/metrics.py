from __future__ import annotations

from dataclasses import dataclass

from .contracts import RouteDecision


@dataclass(frozen=True)
class RouteOutcome:
    selected_node: str | None
    success: bool
    latency_ms: float | None = None
    cost: float = 0.0
    attempts: int = 1


@dataclass(frozen=True)
class RouteQuality:
    success_rate: float
    mean_latency_ms: float | None
    mean_cost: float
    mean_attempts: float
    fallback_rate: float


def evaluate_route_quality(
    decisions: list[RouteDecision], outcomes: list[RouteOutcome]
) -> RouteQuality:
    """Aggregate routing quality without owning execution semantics.

    Callers supply observed outcomes from M2A2 or a simulator. The router only
    measures whether its route choices were effective.
    """
    if len(decisions) != len(outcomes):
        raise ValueError("decisions and outcomes must have the same length")
    if not decisions:
        return RouteQuality(0.0, None, 0.0, 0.0, 0.0)

    total = len(outcomes)
    successes = sum(1 for item in outcomes if item.success)
    latencies = [item.latency_ms for item in outcomes if item.latency_ms is not None]
    return RouteQuality(
        success_rate=successes / total,
        mean_latency_ms=(sum(latencies) / len(latencies)) if latencies else None,
        mean_cost=sum(item.cost for item in outcomes) / total,
        mean_attempts=sum(item.attempts for item in outcomes) / total,
        fallback_rate=sum(1 for item in decisions if item.fallback) / total,
    )
