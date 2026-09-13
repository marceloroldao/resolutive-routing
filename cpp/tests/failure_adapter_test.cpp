#include <cassert>
#include <stdexcept>

#include <resolutive_routing/failure_adapter.hpp>

int main() {
    using namespace resolutive_routing;

    AuthenticatedFailureNoticeView notice{
        .request_id = "job-42",
        .failed_node_id = "node-b",
        .reason = "transport_timeout",
        .observed_at = 1800000100,
        .authenticated = true,
    };
    const auto event = failure_event_from_authenticated_notice(notice);
    assert(event.request_id == "job-42");
    assert(event.failed_node_id == "node-b");
    assert(event.reason == "transport_timeout");
    assert(event.observed_at == 1800000100);

    bool rejected = false;
    try {
        notice.authenticated = false;
        (void)failure_event_from_authenticated_notice(notice);
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    assert(rejected);
    return 0;
}
