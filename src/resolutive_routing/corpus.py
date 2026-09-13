from __future__ import annotations

from dataclasses import dataclass

from .contracts import Node, Request, RequestType, Scope


@dataclass(frozen=True)
class RoutingScenario:
    name: str
    request: Request
    nodes: tuple[Node, ...]
    expected_node: str | None
    rationale: str


def scenario_corpus() -> tuple[RoutingScenario, ...]:
    all_scopes = frozenset(Scope)

    local = Node(
        "node_local", "org_1", is_local=True, trusted=True,
        compute_capacity=24, current_load=0.10, latency_ms=2, reputation=0.92,
        models=frozenset({"small_llm"}), memory_domains=frozenset({"local_context"}),
        supported_scopes=all_scopes,
    )
    fast = Node(
        "node_fast", "org_1", trusted=True,
        compute_capacity=64, current_load=0.20, latency_ms=7, reputation=0.96,
        models=frozenset({"small_llm", "qwen_7b"}), memory_domains=frozenset({"electronics"}),
        supported_scopes=all_scopes,
    )
    heavy = Node(
        "node_heavy", "org_1", trusted=True,
        compute_capacity=160, current_load=0.15, latency_ms=28, reputation=0.98,
        models=frozenset({"qwen_14b", "vision_large"}), memory_domains=frozenset({"engineering", "vision"}),
        supported_scopes=all_scopes,
    )
    foreign = Node(
        "node_foreign", "org_2", trusted=True,
        compute_capacity=220, current_load=0.05, latency_ms=5, reputation=0.99,
        models=frozenset({"small_llm", "qwen_14b"}), memory_domains=frozenset({"electronics", "engineering"}),
        supported_scopes=all_scopes,
    )
    untrusted = Node(
        "node_untrusted", None, trusted=False,
        compute_capacity=300, current_load=0.0, latency_ms=1, reputation=0.80,
        models=frozenset({"small_llm"}), memory_domains=frozenset({"public"}),
        supported_scopes=all_scopes,
    )

    return (
        RoutingScenario(
            "local_only",
            Request("case_local", RequestType.INFERENCE_REQUEST, Scope.LOCAL_ONLY, "node_local", "org_1", required_model="small_llm"),
            (local, fast, heavy),
            "node_local",
            "LOCAL_ONLY must remain on the local node.",
        ),
        RoutingScenario(
            "organization_boundary",
            Request("case_org", RequestType.INFERENCE_REQUEST, Scope.ORGANIZATION, "node_local", "org_1", required_model="small_llm", min_compute=20),
            (fast, foreign),
            "node_fast",
            "A faster foreign-organization node is inadmissible despite attractive hardware.",
        ),
        RoutingScenario(
            "model_requirement",
            Request("case_model", RequestType.INFERENCE_REQUEST, Scope.ORGANIZATION, "node_local", "org_1", required_model="qwen_14b", min_compute=40),
            (fast, heavy),
            "node_heavy",
            "The required model is available only on the heavy node.",
        ),
        RoutingScenario(
            "knowledge_domain",
            Request("case_knowledge", RequestType.KNOWLEDGE_REQUEST, Scope.ORGANIZATION, "node_local", "org_1", knowledge_domain="electronics", max_latency_ms=20),
            (fast, heavy),
            "node_fast",
            "Domain and latency constraints select the electronics node.",
        ),
        RoutingScenario(
            "private_trust",
            Request("case_private", RequestType.INFERENCE_REQUEST, Scope.PRIVATE, "node_local", "org_1", required_model="small_llm", min_compute=10),
            (fast, untrusted),
            "node_fast",
            "PRIVATE rejects an untrusted node even when it has lower latency and more compute.",
        ),
        RoutingScenario(
            "public_multi_candidate",
            Request("case_public", RequestType.COMPUTE_REQUEST, Scope.PUBLIC, "node_local", "org_1", min_compute=10, max_latency_ms=50),
            (fast, heavy, foreign),
            "node_foreign",
            "Several nodes are admissible; resolutive routing should choose one rather than flood all candidates.",
        ),
        RoutingScenario(
            "no_valid_route",
            Request("case_none", RequestType.INFERENCE_REQUEST, Scope.ORGANIZATION, "node_local", "org_1", required_model="vision_large", max_latency_ms=10),
            (fast, heavy, foreign),
            None,
            "No node satisfies organization, model and latency constraints simultaneously.",
        ),
    )
