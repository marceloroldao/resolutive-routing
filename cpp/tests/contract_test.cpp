#include <cassert>
#include <resolutive_routing/contracts.hpp>

int main() {
    resolutive_routing::NodeSnapshot node{
        .node_id = "node-b",
        .organization_id = "org-1",
        .is_local = false,
        .trusted = true,
        .available = true,
        .compute_capacity = 64.0,
        .current_load = 0.20,
        .latency_ms = 7.0,
        .reputation = 0.96,
        .models = {"small_llm"},
        .memory_domains = {"electronics"},
        .supported_scopes = {resolutive_routing::Scope::Organization},
    };

    assert(node.available);
    assert(node.trusted);
    assert(node.current_load >= 0.0 && node.current_load <= 1.0);

    resolutive_routing::Request request{
        .request_id = "job-1",
        .scope = resolutive_routing::Scope::Organization,
        .source_node_id = "node-a",
        .organization_id = "org-1",
        .required_model = "small_llm",
        .knowledge_domain = std::nullopt,
        .min_compute = 20.0,
        .max_latency_ms = 50.0,
    };

    assert(request.required_model.has_value());
    return 0;
}
