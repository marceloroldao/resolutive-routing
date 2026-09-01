from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RequestType(str, Enum):
    KNOWLEDGE_REQUEST = "KNOWLEDGE_REQUEST"
    MEMORY_REQUEST = "MEMORY_REQUEST"
    COMPUTE_REQUEST = "COMPUTE_REQUEST"
    INFERENCE_REQUEST = "INFERENCE_REQUEST"
    STORAGE_REQUEST = "STORAGE_REQUEST"
    ECHO_REQUEST = "ECHO_REQUEST"


class Scope(str, Enum):
    LOCAL_ONLY = "LOCAL_ONLY"
    PRIVATE = "PRIVATE"
    ORGANIZATION = "ORGANIZATION"
    PUBLIC = "PUBLIC"


@dataclass(frozen=True)
class Request:
    request_id: str
    type: RequestType
    scope: Scope
    origin_node_id: str
    organization_id: str | None = None
    knowledge_domain: str | None = None
    required_model: str | None = None
    min_compute: float = 0.0
    max_latency_ms: float | None = None
    required_confidence: float = 0.0


@dataclass(frozen=True)
class Node:
    node_id: str
    organization_id: str | None
    is_local: bool = False
    available: bool = True
    trusted: bool = False
    compute_capacity: float = 0.0
    current_load: float = 0.0
    latency_ms: float = 0.0
    reputation: float = 1.0
    cost: float = 0.0
    credit_balance: float = 0.0
    models: frozenset[str] = field(default_factory=frozenset)
    memory_domains: frozenset[str] = field(default_factory=frozenset)
    supported_scopes: frozenset[Scope] = field(default_factory=lambda: frozenset(Scope))

    @property
    def available_compute(self) -> float:
        return max(0.0, self.compute_capacity * (1.0 - self.current_load))


@dataclass(frozen=True)
class CandidateScore:
    node_id: str
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class RouteDecision:
    selected_node: str | None
    score: float
    reasons: tuple[str, ...]
    rejected_nodes: dict[str, tuple[str, ...]]
    candidates: tuple[CandidateScore, ...]
    fallback: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "selected_node": self.selected_node,
            "score": round(self.score, 6),
            "reasons": list(self.reasons),
            "rejected_nodes": {key: list(value) for key, value in self.rejected_nodes.items()},
            "candidates": [
                {"node_id": item.node_id, "score": round(item.score, 6), "reasons": list(item.reasons)}
                for item in self.candidates
            ],
            "fallback": self.fallback,
        }
