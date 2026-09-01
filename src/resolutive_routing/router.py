from __future__ import annotations

from .contracts import CandidateScore, Node, Request, RouteDecision
from .policy import policy_rejections


class DeterministicRouter:
    """Policy-first router with normalized, deterministic scoring."""

    def route(self, request: Request, nodes: list[Node]) -> RouteDecision:
        rejected: dict[str, tuple[str, ...]] = {}
        eligible: list[Node] = []
        for node in sorted(nodes, key=lambda item: item.node_id):
            failures = policy_rejections(request, node)
            if failures:
                rejected[node.node_id] = tuple(failures)
            else:
                eligible.append(node)

        if not eligible:
            return RouteDecision(None, 0.0, ("no_valid_m2a2_node",), rejected, (), fallback=True)

        max_compute = max((node.available_compute for node in eligible), default=1.0) or 1.0
        max_latency = max((node.latency_ms for node in eligible), default=1.0) or 1.0
        candidates: list[CandidateScore] = []
        for node in eligible:
            compute_score = node.available_compute / max_compute
            latency_score = 1.0 - (node.latency_ms / (max_latency * 1.01))
            knowledge_score = 1.0 if request.knowledge_domain else 0.5
            model_score = 1.0 if request.required_model else 0.5
            cost_score = 1.0 / (1.0 + max(0.0, node.cost))
            credit_score = 0.5 + 0.5 * (node.credit_balance / (abs(node.credit_balance) + 1000.0))
            score = (
                0.25 * compute_score + 0.20 * latency_score + 0.20 * node.reputation
                + 0.15 * knowledge_score + 0.10 * model_score + 0.05 * cost_score
                + 0.05 * credit_score
                + (0.15 if node.is_local else 0.0)
            )
            reasons = ["scope_allowed", "available", "capability_sufficient", "latency_acceptable"]
            if node.is_local:
                reasons.append("local_preference")
            if request.required_model:
                reasons.append("required_model_available")
            if request.knowledge_domain:
                reasons.append("knowledge_domain_available")
            reasons.append("credit_balance_considered")
            candidates.append(CandidateScore(node.node_id, round(score, 12), tuple(reasons)))

        candidates.sort(key=lambda item: (-item.score, item.node_id))
        winner = candidates[0]
        return RouteDecision(winner.node_id, winner.score, winner.reasons, rejected, tuple(candidates))
