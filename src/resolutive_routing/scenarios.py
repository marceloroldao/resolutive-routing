from .contracts import Node, Request, RequestType, Scope


def demo_nodes() -> list[Node]:
    org_scopes = frozenset({Scope.LOCAL_ONLY, Scope.PRIVATE, Scope.ORGANIZATION, Scope.PUBLIC})
    return [
        Node("node_a", "org_1", compute_capacity=100, current_load=0.80, latency_ms=80, reputation=0.98, credit_balance=-3100,
             models=frozenset({"qwen_14b"}), memory_domains=frozenset({"engineering"}), supported_scopes=org_scopes, trusted=True),
        Node("node_b", "org_1", compute_capacity=60, current_load=0.10, latency_ms=10, reputation=0.95, credit_balance=8400,
             models=frozenset({"small_llm", "qwen_7b"}), memory_domains=frozenset({"electronics", "ESP32 ADC"}), supported_scopes=org_scopes, trusted=True),
        Node("node_c", "org_1", is_local=True, compute_capacity=20, current_load=0.05, latency_ms=3, reputation=0.90, credit_balance=400,
             models=frozenset({"small_llm", "llama_3b"}), memory_domains=frozenset({"local_context"}), supported_scopes=org_scopes, trusted=True),
    ]


def demo_request() -> Request:
    return Request("req_1", RequestType.INFERENCE_REQUEST, Scope.ORGANIZATION, "node_c", "org_1",
                   required_model="small_llm", min_compute=10, max_latency_ms=100)
