from __future__ import annotations

import json
from time import perf_counter

from .baselines import broadcast, first_available, highest_hardware, lowest_latency, random_route
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
    results: dict[str, object] = {"iterations": iterations, "scenario": "demo_v1", "timings_ms": {}}
    for name, strategy in strategies.items():
        start = perf_counter()
        result = None
        for _ in range(iterations):
            result = strategy()
        results["timings_ms"][name] = round((perf_counter() - start) * 1000, 3)
        results[name] = result
    return results


def main() -> None:
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()

