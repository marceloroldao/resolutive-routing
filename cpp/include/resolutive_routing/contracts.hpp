#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <vector>

namespace resolutive_routing {

enum class Scope {
    LocalOnly,
    Private,
    Organization,
    Public,
};

struct NodeSnapshot {
    std::string node_id;
    std::string organization_id;
    bool is_local{};
    bool trusted{};
    bool available{};
    double compute_capacity{};
    double current_load{};
    double latency_ms{};
    double reputation{};
    std::vector<std::string> models;
    std::vector<std::string> memory_domains;
    std::vector<Scope> supported_scopes;
};

struct Request {
    std::string request_id;
    Scope scope{Scope::Private};
    std::string source_node_id;
    std::string organization_id;
    std::optional<std::string> required_model;
    std::optional<std::string> knowledge_domain;
    double min_compute{};
    std::optional<double> max_latency_ms;
};

struct RouteDecision {
    std::optional<std::string> selected_node_id;
    std::string reason;
    double score{};
};

struct FailureEvent {
    std::string request_id;
    std::string failed_node_id;
    std::string reason;
    std::int64_t observed_at{};
};

} // namespace resolutive_routing
