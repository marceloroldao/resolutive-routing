#pragma once

#include <algorithm>
#include <optional>
#include <string>
#include <vector>

#include <resolutive_routing/contracts.hpp>
#include <resolutive_routing/router.hpp>

namespace resolutive_routing {

struct RerouteDecision {
    std::optional<std::string> previous_node_id;
    std::optional<std::string> selected_node_id;
    std::vector<std::string> excluded_nodes;
    RouteDecision route;
};

inline RerouteDecision reroute_after_failure(
    const DeterministicRouter& router,
    const Request& request,
    const std::vector<NodeSnapshot>& nodes,
    const RouteDecision& previous,
    const FailureEvent& failure,
    std::vector<std::string> excluded_nodes = {}
) {
    if (std::find(excluded_nodes.begin(), excluded_nodes.end(), failure.failed_node_id) == excluded_nodes.end()) {
        excluded_nodes.push_back(failure.failed_node_id);
    }

    std::vector<NodeSnapshot> remaining;
    remaining.reserve(nodes.size());
    for (const auto& node : nodes) {
        if (std::find(excluded_nodes.begin(), excluded_nodes.end(), node.node_id) == excluded_nodes.end()) {
            remaining.push_back(node);
        }
    }

    auto decision = router.route(request, std::move(remaining));
    return RerouteDecision{
        .previous_node_id = previous.selected_node_id,
        .selected_node_id = decision.selected_node_id,
        .excluded_nodes = std::move(excluded_nodes),
        .route = std::move(decision),
    };
}

} // namespace resolutive_routing
