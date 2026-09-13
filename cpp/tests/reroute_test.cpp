#include <cassert>
#include <resolutive_routing/reroute.hpp>

using namespace resolutive_routing;

static NodeSnapshot make_node(const char* id, double compute, double latency) {
    return NodeSnapshot{
        .node_id = id,
        .organization_id = "org-1",
        .is_local = false,
        .trusted = true,
        .available = true,
        .compute_capacity = compute,
        .current_load = 0.0,
        .latency_ms = latency,
        .reputation = 0.95,
        .cost = 0.0,
        .credit_balance = 0.0,
        .models = {"small_llm"},
        .memory_domains = {"electronics"},
        .supported_scopes = {Scope::Organization},
    };
}

int main() {
    DeterministicRouter router;
    Request request{
        .request_id = "req-failover",
        .type = RequestType::Inference,
        .scope = Scope::Organization,
        .source_node_id = "node-a",
        .organization_id = "org-1",
        .required_model = "small_llm",
        .knowledge_domain = "electronics",
        .min_compute = 1.0,
        .max_latency_ms = 100.0,
        .required_confidence = 0.0,
    };

    auto node_b = make_node("node-b", 100.0, 10.0);
    auto node_c = make_node("node-c", 80.0, 20.0);
    auto first = router.route(request, {node_c, node_b});
    assert(first.selected_node_id.has_value());
    assert(*first.selected_node_id == "node-b");

    FailureEvent failure{
        .request_id = request.request_id,
        .failed_node_id = "node-b",
        .reason = "transport_unreachable",
        .observed_at = 1700000000,
    };

    auto rerouted = reroute_after_failure(router, request, {node_b, node_c}, first, failure);
    assert(rerouted.previous_node_id.has_value());
    assert(*rerouted.previous_node_id == "node-b");
    assert(rerouted.selected_node_id.has_value());
    assert(*rerouted.selected_node_id == "node-c");
    assert(rerouted.excluded_nodes.size() == 1);
    assert(rerouted.excluded_nodes[0] == "node-b");

    // Repeating the same failure must not duplicate exclusions.
    auto again = reroute_after_failure(router, request, {node_b, node_c}, rerouted.route, failure, rerouted.excluded_nodes);
    assert(again.excluded_nodes.size() == 1);
    assert(again.selected_node_id.has_value());
    assert(*again.selected_node_id == "node-c");
    return 0;
}
