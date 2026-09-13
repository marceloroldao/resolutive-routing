#pragma once

#include <cstdint>
#include <stdexcept>
#include <string>

#include <resolutive_routing/contracts.hpp>

namespace resolutive_routing {

struct AuthenticatedFailureNoticeView {
    std::string request_id;
    std::string failed_node_id;
    std::string reason;
    std::int64_t observed_at{};
    bool authenticated{};
};

inline FailureEvent failure_event_from_authenticated_notice(const AuthenticatedFailureNoticeView& notice) {
    if (!notice.authenticated) {
        throw std::invalid_argument("failure notice must be authenticated by transport layer");
    }
    if (notice.request_id.empty() || notice.failed_node_id.empty() || notice.reason.empty()) {
        throw std::invalid_argument("failure notice missing routing field");
    }
    return FailureEvent{
        .request_id = notice.request_id,
        .failed_node_id = notice.failed_node_id,
        .reason = notice.reason,
        .observed_at = notice.observed_at,
    };
}

} // namespace resolutive_routing
