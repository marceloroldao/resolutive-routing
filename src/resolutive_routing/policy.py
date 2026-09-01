from .contracts import Node, Request, Scope


def policy_rejections(request: Request, node: Node) -> list[str]:
    reasons: list[str] = []
    if not node.available:
        reasons.append("unavailable")
    if request.scope not in node.supported_scopes:
        reasons.append("scope_not_supported")
    if request.scope is Scope.LOCAL_ONLY and not node.is_local:
        reasons.append("local_only")
    if request.scope is Scope.PRIVATE and not (node.is_local or node.trusted):
        reasons.append("private_node_not_trusted")
    if request.scope is Scope.ORGANIZATION and node.organization_id != request.organization_id:
        reasons.append("organization_mismatch")
    if request.required_model and request.required_model not in node.models:
        reasons.append("model_not_available")
    if request.knowledge_domain and request.knowledge_domain not in node.memory_domains:
        reasons.append("knowledge_domain_not_available")
    if node.available_compute < request.min_compute:
        reasons.append("insufficient_available_compute")
    if request.max_latency_ms is not None and node.latency_ms > request.max_latency_ms:
        reasons.append("latency_limit_exceeded")
    return reasons

