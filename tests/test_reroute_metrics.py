import unittest

from resolutive_routing.contracts import Node, Request, RequestType, Scope
from resolutive_routing.metrics import RouteOutcome, evaluate_route_quality
from resolutive_routing.reroute import FailureEvent, reroute_after_failure
from resolutive_routing.router import DeterministicRouter


class RerouteAndMetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = DeterministicRouter()
        self.request = Request(
            request_id="req-1",
            type=RequestType.COMPUTE_REQUEST,
            scope=Scope.PUBLIC,
            origin_node_id="origin",
            min_compute=1.0,
        )
        self.nodes = [
            Node(
                node_id="node-a",
                organization_id=None,
                compute_capacity=10.0,
                current_load=0.0,
                latency_ms=5.0,
                reputation=1.0,
            ),
            Node(
                node_id="node-b",
                organization_id=None,
                compute_capacity=8.0,
                current_load=0.0,
                latency_ms=10.0,
                reputation=1.0,
            ),
        ]

    def test_reroute_excludes_failed_node(self) -> None:
        first = self.router.route(self.request, self.nodes)
        self.assertEqual(first.selected_node, "node-a")

        rerouted = reroute_after_failure(
            self.router,
            self.request,
            self.nodes,
            first,
            FailureEvent("req-1", "node-a", "unavailable"),
        )

        self.assertEqual(rerouted.previous_node, "node-a")
        self.assertEqual(rerouted.selected_node, "node-b")
        self.assertEqual(rerouted.excluded_nodes, ("node-a",))

    def test_route_quality_aggregates_observed_results(self) -> None:
        first = self.router.route(self.request, self.nodes)
        fallback_request = Request(
            request_id="req-2",
            type=RequestType.COMPUTE_REQUEST,
            scope=Scope.LOCAL_ONLY,
            origin_node_id="origin",
            min_compute=100.0,
        )
        second = self.router.route(fallback_request, self.nodes)
        quality = evaluate_route_quality(
            [first, second],
            [
                RouteOutcome(first.selected_node, True, latency_ms=10.0, cost=2.0, attempts=1),
                RouteOutcome(second.selected_node, False, latency_ms=30.0, cost=0.0, attempts=2),
            ],
        )

        self.assertEqual(quality.success_rate, 0.5)
        self.assertEqual(quality.mean_latency_ms, 20.0)
        self.assertEqual(quality.mean_cost, 1.0)
        self.assertEqual(quality.mean_attempts, 1.5)
        self.assertEqual(quality.fallback_rate, 0.5)

    def test_quality_rejects_misaligned_inputs(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_route_quality([], [RouteOutcome(None, False)])


if __name__ == "__main__":
    unittest.main()
