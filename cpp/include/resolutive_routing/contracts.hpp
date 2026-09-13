#pragma once

#include <cstdint>
#include <map>
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

enum class RequestType {
    Knowledge,
    Memory,
    Compute,
    Inference,
    Storage,
    Echo,
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
    double reputation{1.0};
    double cost{};
    double credit_balance{};
    std::vector<std::string> models;
    std::vector<std::string> memory_domains;
    std::vector<Scope> supported_scopes;

    [[nodiscard]] double available_compute() const noexcept {
        const auto remaining = compute_capacity * (1.0 - current_load);
        return remaining > 0.0 ? remaining : 0.0;
    }
};

struct Request {
    std::string request_id;
    RequestType type{RequestType::Compute};
    Scope scope{Scope::Private};
    std::string source_node_id;
    std::string organization_id;
    std::optional<std::string> required_model;
    std::optional<std::string> knowledge_domain;
    double min_compute{};
    std::optional<double> max_latency_ms;
    double required_confidence{};
};

struct CandidateScore {
    std::string node_id;
    double score{};
    std::vector<std::string> reasons;
};

struct RouteDecision {
    std::optional<std::string> selected_node_id;
    double score{};
    std::vector<std::string> reasons;
    std::map<std::string, std::vector<std::string>> rejected_nodes;
    std::vector<CandidateScore> candidates;
    bool fallback{};
};

struct FailureEvent {
    std::string request_id;
    std::string failed_node_id;
    std::string reason;
    std::int64_t observed_at{};
};

} // namespace resolutive_routing
