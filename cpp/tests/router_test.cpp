#include <cassert>
#include <cmath>
#include <resolutive_routing/router.hpp>

using namespace resolutive_routing;

int main() {
    DeterministicRouter router;
    Request request{
        .request_id = "req-1",
        .type = RequestType::Inference,
        .scope = Scope::Organization,
        .source_node_id = "node-a",
        .organization_id = "org-1",
        .required_model = "small_llm",
        .knowledge_domain = "electronics",
        .min_compute = 10.0,
        .max_latency_ms = 100.0,
        .required_confidence = 0.0,
    };

    NodeSnapshot fast{
        .node_id = "node-b",
        .organization_id = "org-1",
        .is_local = false,
        .trusted = true,
        .available = true,
        .compute_capacity = 100.0,
        .current_load = 0.10,
        .latency_ms = 10.0,
        .reputation = 0.95,
        .cost = 0.1,
        .credit_balance = 100.0,
        .models = {"small_llm"},
        .memory_domains = {"electronics"},
        .supported_scopes = {Scope::Organization},
    };
    NodeSnapshot slower = fast;
    slower.node_id = "node-c";
    slower.compute_capacity = 70.0;
    slower.current_load = 0.20;
    slower.latency_ms = 30.0;
    slower.reputation = 0.90;

    auto decision = router.route(request, {slower, fast});
    assert(decision.selected_node_id.has_value());
    assert(*decision.selected_node_id == "node-b");
    assert(!decision.fallback);
    assert(decision.candidates.size() == 2);
    assert(decision.candidates[0].node_id == "node-b");

    auto rejected = fast;
    rejected.node_id = "node-x";
    rejected.organization_id = "org-2";
    auto with_rejection = router.route(request, {rejected, fast});
    assert(*with_rejection.selected_node_id == "node-b");
    assert(with_rejection.rejected_nodes.at("node-x").front() == "organization_mismatch");

    fast.available = false;
    slower.available = false;
    auto fallback = router.route(request, {fast, slower});
    assert(!fallback.selected_node_id.has_value());
    assert(fallback.fallback);
    assert(fallback.reasons.size() == 1);
    assert(fallback.reasons[0] == "no_valid_m2a2_node");
    return 0;
}
