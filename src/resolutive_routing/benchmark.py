from __future__ import annotations

import json
from dataclasses import asdict
from time import perf_counter

from .baselines import broadcast, first_available, highest_hardware, lowest_latency, random_route
from .comparison import compare_strategies
from .corpus import scenario_corpus
from .router import DeterministicRouter
from .scenarios import demo_nodes, demo_request


def run(iterations: int = 10_000) -> dict[str, object]:
    request, nodes = demo_request(), demo_nodes()
    strategies = {
        "resolutive": lambda: DeterministicRouter().route(request, nodes).selected_node,
        "first_available": lambda: first_available(request, nodes),
        "lowest_latency": lambda: lowest_latency(request, nodes),
        "highest_hardware": lambda: highest_hardware(request, nodes),
        "random_seeded": lambda: random_route(request, nodes),
        "broadcast": lambda: broadcast(request, nodes),
    }
    results: dict[str, object] = {
        "iterations": iterations,
        "scenario": "demo_v1",
        "timings_ms": {},
    }
    for name, strategy in strategies.items():
        start = perf_counter()
        result = None
        for _ in range(iterations):
            result = strategy()
        results["timings_ms"][name] = round((perf_counter() - start) * 1000, 3)
        results[name] = result

    corpus = scenario_corpus()
    results["route_quality"] = [
        {
            **asdict(item),
            "target_hit_rate": round(item.target_hit_rate, 6),
        }
        for item in compare_strategies(corpus)
    ]
    results["route_quality_scenarios"] = [
        {
            "name": case.name,
            "expected_node": case.expected_node,
            "rationale": case.rationale,
        }
        for case in corpus
    ]
    return results


def main() -> None:
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()
