import unittest

from resolutive_routing import DeterministicRouter, Request, RequestType, Scope
from resolutive_routing.ma2a_adapter import failure_from_ma2a_notice, node_from_ma2a_capability
from resolutive_routing.reroute import reroute_after_failure


class MA2AAdapterTests(unittest.TestCase):
    def capability(self, node_id: str, compute: float, load: float, models: list[str]) -> dict[str, object]:
        return {
            "node_id": node_id,
            "organization_id": "org-1",
            "available": True,
            "compute_capacity": compute,
            "current_load": load,
            "models": models,
            "memory_domains": ["electronics"],
            "supported_scopes": ["ORGANIZATION", "PUBLIC", "PRIVATE"],
        }

    def test_verified_advertisements_can_feed_router(self) -> None:
        node_a = node_from_ma2a_capability(
            self.capability("node-a", 40, 0.40, ["small_llm"]),
            latency_ms=18,
            trusted=True,
            reputation=0.95,
        )
        node_b = node_from_ma2a_capability(
            self.capability("node-b", 80, 0.10, ["small_llm"]),
            latency_ms=8,
            trusted=True,
            reputation=0.97,
        )
        request = Request(
            "req-1", RequestType.INFERENCE_REQUEST, Scope.ORGANIZATION,
            "node-a", "org-1", required_model="small_llm", min_compute=10,
        )
        decision = DeterministicRouter().route(request, [node_a, node_b])
        self.assertEqual(decision.selected_node, "node-b")

    def test_failure_notice_drives_reroute(self) -> None:
        node_a = node_from_ma2a_capability(
            self.capability("node-a", 40, 0.20, ["small_llm"]),
            latency_ms=12,
            trusted=True,
        )
        node_b = node_from_ma2a_capability(
            self.capability("node-b", 90, 0.05, ["small_llm"]),
            latency_ms=4,
            trusted=True,
        )
        request = Request(
            "req-2", RequestType.INFERENCE_REQUEST, Scope.ORGANIZATION,
            "node-a", "org-1", required_model="small_llm", min_compute=10,
        )
        router = DeterministicRouter()
        first = router.route(request, [node_a, node_b])
        self.assertEqual(first.selected_node, "node-b")

        failure = failure_from_ma2a_notice({
            "request_id": "req-2",
            "failed_node_id": "node-b",
            "reason": "transport_timeout",
        })
        second = reroute_after_failure(router, request, [node_a, node_b], first, failure)
        self.assertEqual(second.selected_node, "node-a")

    def test_remote_node_cannot_self_assert_trust_or_latency(self) -> None:
        payload = self.capability("node-a", 10, 0.1, ["small_llm"])
        payload["trusted"] = True
        payload["latency_ms"] = 0
        node = node_from_ma2a_capability(payload, latency_ms=55, trusted=False)
        self.assertFalse(node.trusted)
        self.assertEqual(node.latency_ms, 55)


if __name__ == "__main__":
    unittest.main()
