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

    NodeSnapshot b{
        .node_id = "node-b", .organization_id = "org-1", .is_local = false,
        .trusted = true, .available = true, .compute_capacity = 100.0,
        .current_load = 0.10, .latency_ms = 10.0, .reputation = 0.95,
        .cost = 0.1, .credit_balance = 100.0,
        .models = {"small_llm"}, .memory_domains = {"electronics"},
        .supported_scopes = {Scope::Organization},
    };
    NodeSnapshot c = b;
    c.node_id = "node-c";
    c.compute_capacity = 70.0;
    c.current_load = 0.20;
    c.latency_ms = 30.0;
    c.reputation = 0.90;

    const auto d = router.route(request, {c, b});
    assert(d.selected_node_id && *d.selected_node_id == "node-b");
    assert(d.candidates.size() == 2);

    // Golden scores produced by the Python reference implementation.
    assert(std::abs(d.candidates[0].score - 0.896720672067) < 1e-12);
    assert(std::abs(d.candidates[1].score - 0.660263026303) < 1e-12);
    return 0;
}
