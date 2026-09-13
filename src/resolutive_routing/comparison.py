from __future__ import annotations

from dataclasses import dataclass

from .baselines import broadcast
from .corpus import RoutingScenario
from .policy import policy_rejections
from .router import DeterministicRouter


@dataclass(frozen=True)
class StrategyResult:
    strategy: str
    scenarios: int
    target_hits: int
    no_route_correct: int
    mean_fanout: float
    unnecessary_dispatches: int

    @property
    def target_hit_rate(self) -> float:
        return self.target_hits / self.scenarios if self.scenarios else 0.0


def _static_route(scenario: RoutingScenario, preferred_node: str) -> tuple[str, ...]:
    node = next((item for item in scenario.nodes if item.node_id == preferred_node), None)
    if node is None or policy_rejections(scenario.request, node):
        return ()
    return (node.node_id,)


def _resolutive_route(scenario: RoutingScenario) -> tuple[str, ...]:
    decision = DeterministicRouter().route(scenario.request, list(scenario.nodes))
    return (decision.selected_node,) if decision.selected_node is not None else ()


def compare_strategies(
    corpus: tuple[RoutingScenario, ...],
    static_node_id: str = "node_fast",
) -> tuple[StrategyResult, ...]:
    """Compare routing selection behavior without executing remote work.

    Broadcast is considered a hit when the expected node is among recipients, but
    its fanout and unnecessary dispatches are accounted separately. This avoids
    treating flooding as equivalent to a single targeted route.
    """

    strategies = {
        "static": lambda case: _static_route(case, static_node_id),
        "broadcast": lambda case: broadcast(case.request, list(case.nodes)),
        "resolutive": _resolutive_route,
    }

    results: list[StrategyResult] = []
    for name, strategy in strategies.items():
        hits = 0
        no_route_correct = 0
        total_fanout = 0
        unnecessary = 0

        for case in corpus:
            selected = strategy(case)
            total_fanout += len(selected)

            if case.expected_node is None:
                if not selected:
                    hits += 1
                    no_route_correct += 1
                else:
                    unnecessary += len(selected)
                continue

            if case.expected_node in selected:
                hits += 1
            unnecessary += max(0, len(selected) - 1)

        count = len(corpus)
        results.append(
            StrategyResult(
                strategy=name,
                scenarios=count,
                target_hits=hits,
                no_route_correct=no_route_correct,
                mean_fanout=(total_fanout / count) if count else 0.0,
                unnecessary_dispatches=unnecessary,
            )
        )

    return tuple(results)
