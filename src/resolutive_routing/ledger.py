from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class ResourceType(str, Enum):
    COMPUTE = "COMPUTE_CREDIT"
    STORAGE = "STORAGE_CREDIT"
    KNOWLEDGE = "KNOWLEDGE_CREDIT"


@dataclass(frozen=True)
class LedgerEntry:
    node_id: str
    resource: ResourceType
    amount: float
    reason: str


class CreditLedger:
    def __init__(self) -> None:
        self._balances: dict[str, dict[ResourceType, float]] = defaultdict(lambda: defaultdict(float))
        self._entries: list[LedgerEntry] = []

    def contribute(self, node_id: str, resource: ResourceType, work_units: float, *, quality: float = 1.0, success: bool = True) -> float:
        if work_units < 0 or not 0 <= quality <= 1:
            raise ValueError("work_units must be non-negative and quality must be between 0 and 1")
        success_factor = 1.0 if success else 0.1
        credit = work_units * quality * success_factor
        self._record(node_id, resource, credit, "contribution" if success else "failed_contribution")
        return credit

    def consume(self, node_id: str, resource: ResourceType, work_units: float) -> float:
        if work_units < 0:
            raise ValueError("work_units must be non-negative")
        self._record(node_id, resource, -work_units, "consumption")
        return -work_units

    def balance(self, node_id: str, resource: ResourceType) -> float:
        return self._balances[node_id][resource]

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def _record(self, node_id: str, resource: ResourceType, amount: float, reason: str) -> None:
        self._balances[node_id][resource] += amount
        self._entries.append(LedgerEntry(node_id, resource, amount, reason))

