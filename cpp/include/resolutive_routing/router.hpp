#pragma once

#include <algorithm>
#include <cmath>
#include <string>
#include <vector>

#include <resolutive_routing/contracts.hpp>

namespace resolutive_routing {

namespace detail {

inline bool contains(const std::vector<std::string>& values, const std::string& value) {
    return std::find(values.begin(), values.end(), value) != values.end();
}

inline bool supports_scope(const std::vector<Scope>& scopes, Scope scope) {
    return std::find(scopes.begin(), scopes.end(), scope) != scopes.end();
}

inline std::vector<std::string> policy_rejections(const Request& request, const NodeSnapshot& node) {
    std::vector<std::string> reasons;
    if (!node.available) reasons.emplace_back("unavailable");
    if (!supports_scope(node.supported_scopes, request.scope)) reasons.emplace_back("scope_not_supported");
    if (request.scope == Scope::LocalOnly && !node.is_local) reasons.emplace_back("local_only");
    if (request.scope == Scope::Private && !(node.is_local || node.trusted)) reasons.emplace_back("private_node_not_trusted");
    if (request.scope == Scope::Organization && node.organization_id != request.organization_id) reasons.emplace_back("organization_mismatch");
    if (request.required_model && !contains(node.models, *request.required_model)) reasons.emplace_back("model_not_available");
    if (request.knowledge_domain && !contains(node.memory_domains, *request.knowledge_domain)) reasons.emplace_back("knowledge_domain_not_available");
    if (node.available_compute() < request.min_compute) reasons.emplace_back("insufficient_available_compute");
    if (request.max_latency_ms && node.latency_ms > *request.max_latency_ms) reasons.emplace_back("latency_limit_exceeded");
    return reasons;
}

inline double round12(double value) {
    constexpr double scale = 1'000'000'000'000.0;
    return std::round(value * scale) / scale;
}

} // namespace detail

class DeterministicRouter {
public:
    [[nodiscard]] RouteDecision route(const Request& request, std::vector<NodeSnapshot> nodes) const {
        std::sort(nodes.begin(), nodes.end(), [](const auto& a, const auto& b) { return a.node_id < b.node_id; });

        RouteDecision decision;
        std::vector<NodeSnapshot> eligible;
        for (const auto& node : nodes) {
            auto failures = detail::policy_rejections(request, node);
            if (!failures.empty()) {
                decision.rejected_nodes.emplace(node.node_id, std::move(failures));
            } else {
                eligible.push_back(node);
            }
        }

        if (eligible.empty()) {
            decision.reasons = {"no_valid_m2a2_node"};
            decision.fallback = true;
            return decision;
        }

        double max_compute = 0.0;
        double max_latency = 0.0;
        for (const auto& node : eligible) {
            max_compute = std::max(max_compute, node.available_compute());
            max_latency = std::max(max_latency, node.latency_ms);
        }
        if (max_compute == 0.0) max_compute = 1.0;
        if (max_latency == 0.0) max_latency = 1.0;

        for (const auto& node : eligible) {
            const double compute_score = node.available_compute() / max_compute;
            const double latency_score = 1.0 - (node.latency_ms / (max_latency * 1.01));
            const double knowledge_score = request.knowledge_domain ? 1.0 : 0.5;
            const double model_score = request.required_model ? 1.0 : 0.5;
            const double cost_score = 1.0 / (1.0 + std::max(0.0, node.cost));
            const double credit_score = 0.5 + 0.5 * (node.credit_balance / (std::abs(node.credit_balance) + 1000.0));
            const double score =
                0.25 * compute_score + 0.20 * latency_score + 0.20 * node.reputation
                + 0.15 * knowledge_score + 0.10 * model_score + 0.05 * cost_score
                + 0.05 * credit_score + (node.is_local ? 0.15 : 0.0);

            CandidateScore candidate;
            candidate.node_id = node.node_id;
            candidate.score = detail::round12(score);
            candidate.reasons = {"scope_allowed", "available", "capability_sufficient", "latency_acceptable"};
            if (node.is_local) candidate.reasons.emplace_back("local_preference");
            if (request.required_model) candidate.reasons.emplace_back("required_model_available");
            if (request.knowledge_domain) candidate.reasons.emplace_back("knowledge_domain_available");
            candidate.reasons.emplace_back("credit_balance_considered");
            decision.candidates.push_back(std::move(candidate));
        }

        std::sort(decision.candidates.begin(), decision.candidates.end(), [](const auto& a, const auto& b) {
            if (a.score != b.score) return a.score > b.score;
            return a.node_id < b.node_id;
        });

        const auto& winner = decision.candidates.front();
        decision.selected_node_id = winner.node_id;
        decision.score = winner.score;
        decision.reasons = winner.reasons;
        return decision;
    }
};

} // namespace resolutive_routing
