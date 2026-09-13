"""Deterministic routing primitives for the M2A2 ecosystem."""

from .contracts import Node, Request, RequestType, RouteDecision, Scope
from .ledger import CreditLedger, ResourceType
from .ma2a_adapter import failure_from_ma2a_notice, node_from_ma2a_capability
from .metrics import RouteOutcome, RouteQuality, evaluate_route_quality
from .reroute import FailureEvent, RerouteDecision, reroute_after_failure
from .router import DeterministicRouter

__all__ = [
    "CreditLedger",
    "DeterministicRouter",
    "FailureEvent",
    "Node",
    "Request",
    "RequestType",
    "ResourceType",
    "RerouteDecision",
    "RouteDecision",
    "RouteOutcome",
    "RouteQuality",
    "Scope",
    "evaluate_route_quality",
    "failure_from_ma2a_notice",
    "node_from_ma2a_capability",
    "reroute_after_failure",
]
__version__ = "0.1.0"
