import unittest

from resolutive_routing import DeterministicRouter, Node, Request, RequestType, Scope


ALL = frozenset(Scope)


def node(node_id: str, **kwargs) -> Node:
    defaults = dict(organization_id="org", compute_capacity=50, current_load=0.1, latency_ms=10,
                    reputation=0.9, models=frozenset({"small"}), memory_domains=frozenset({"electronics"}),
                    supported_scopes=ALL, trusted=True)
    defaults.update(kwargs)
    return Node(node_id, **defaults)


def request(**kwargs) -> Request:
    defaults = dict(request_id="r", type=RequestType.INFERENCE_REQUEST, scope=Scope.ORGANIZATION,
                    origin_node_id="local", organization_id="org", required_model="small", max_latency_ms=100)
    defaults.update(kwargs)
    return Request(**defaults)


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.router = DeterministicRouter()

    def test_local_node_preferred_when_capable(self):
        decision = self.router.route(request(), [node("local", is_local=True), node("remote")])
        self.assertEqual(decision.selected_node, "local")

    def test_forbidden_node_rejected_by_scope(self):
        decision = self.router.route(request(scope=Scope.LOCAL_ONLY), [node("remote")])
        self.assertTrue(decision.fallback)
        self.assertIn("local_only", decision.rejected_nodes["remote"])

    def test_overloaded_powerful_node_loses_to_smaller_idle_node(self):
        big = node("big", compute_capacity=100, current_load=0.95)
        small = node("small", compute_capacity=40, current_load=0.0)
        self.assertEqual(self.router.route(request(min_compute=1), [big, small]).selected_node, "small")

    def test_lower_latency_wins_when_other_capability_equal(self):
        self.assertEqual(self.router.route(request(), [node("slow", latency_ms=60), node("fast", latency_ms=5)]).selected_node, "fast")

    def test_unavailable_node_excluded(self):
        decision = self.router.route(request(), [node("down", available=False), node("up")])
        self.assertEqual(decision.selected_node, "up")
        self.assertIn("unavailable", decision.rejected_nodes["down"])

    def test_public_knowledge_routes_to_advertised_domain(self):
        req = request(type=RequestType.ECHO_REQUEST, scope=Scope.PUBLIC, required_model=None,
                      knowledge_domain="ESP32 ADC")
        decision = self.router.route(req, [node("generic"), node("expert", memory_domains=frozenset({"ESP32 ADC"}))])
        self.assertEqual(decision.selected_node, "expert")
        self.assertIn("knowledge_domain_not_available", decision.rejected_nodes["generic"])

    def test_fallback_when_no_valid_node(self):
        decision = self.router.route(request(required_model="large"), [node("small")])
        self.assertTrue(decision.fallback)
        self.assertIsNone(decision.selected_node)

    def test_decision_is_explainable(self):
        decision = self.router.route(request(), [node("selected"), node("rejected", available=False)])
        self.assertIn("scope_allowed", decision.reasons)
        self.assertIn("rejected", decision.as_dict()["rejected_nodes"])

    def test_same_state_same_route(self):
        nodes = [node("b"), node("a")]
        self.assertEqual(self.router.route(request(), nodes), self.router.route(request(), list(reversed(nodes))))

    def test_credit_balance_breaks_equal_capability_tie(self):
        decision = self.router.route(request(), [node("debtor", credit_balance=-500), node("contributor", credit_balance=500)])
        self.assertEqual(decision.selected_node, "contributor")


if __name__ == "__main__":
    unittest.main()
