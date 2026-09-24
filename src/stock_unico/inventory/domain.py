"""Deterministic inventory domain model.

Traceability: HU-11..13, RF-001, RF-018..023, RNF-008, RNF-011.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum


class InventoryState(str, Enum):
    PHYSICAL = "physical"
    RESERVED = "reserved"
    COMMITTED = "committed"
    BLOCKED = "blocked"
    DAMAGED = "damaged"
    IN_TRANSIT = "in_transit"
    PENDING_RECEIPT = "pending_receipt"


class MovementType(str, Enum):
    RECEIPT = "receipt"
    SALE = "sale"
    RETURN = "return"
    CANCELLATION = "cancellation"
    COUNT = "count"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    THEFT = "theft"
    TRANSFER_DISPATCH = "transfer_dispatch"
    TRANSFER_RECEIPT = "transfer_receipt"
    STATE_CHANGE = "state_change"


class InventoryError(ValueError):
    """Base error for inventory invariant violations."""


class InsufficientInventory(InventoryError):
    """A movement would produce a negative quantity."""


class DuplicateMovement(InventoryError):
    """Movement ID has already been processed."""


class OutOfOrderMovement(InventoryError):
    """Movement occurred before the latest accepted movement for the position."""


@dataclass(frozen=True, slots=True)
class InventoryPosition:
    sku: str
    location_id: str
    physical: int = 0
    reserved: int = 0
    committed: int = 0
    blocked: int = 0
    damaged: int = 0
    in_transit: int = 0
    pending_receipt: int = 0

    def quantity(self, state: InventoryState) -> int:
        return getattr(self, state.value)

    def apply_delta(self, state: InventoryState, delta: int) -> "InventoryPosition":
        current = self.quantity(state)
        new_value = current + delta
        if new_value < 0:
            raise InsufficientInventory(
                f"{self.sku}@{self.location_id} {state.value}: "
                f"{current} + ({delta}) would be negative"
            )
        return replace(self, **{state.value: new_value})


@dataclass(frozen=True, slots=True)
class InventoryMovement:
    movement_id: str
    sku: str
    location_id: str
    state: InventoryState
    delta: int
    movement_type: MovementType
    reason: str
    occurred_at: datetime
    source: str
    actor: str
    document_ref: str | None = None
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.movement_id.strip():
            raise ValueError("movement_id is required")
        if not self.sku.strip() or not self.location_id.strip():
            raise ValueError("sku and location_id are required")
        if self.delta == 0:
            raise ValueError("movement delta cannot be zero")
        if not self.reason.strip() or not self.source.strip() or not self.actor.strip():
            raise ValueError("reason, source and actor are required")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class MovementAudit:
    movement_id: str
    sku: str
    location_id: str
    state: InventoryState
    previous_quantity: int
    new_quantity: int
    delta: int
    movement_type: MovementType
    reason: str
    source: str
    actor: str
    occurred_at: datetime
    recorded_at: datetime
    document_ref: str | None
    correlation_id: str | None

    @classmethod
    def from_movement(
        cls,
        movement: InventoryMovement,
        previous_quantity: int,
        new_quantity: int,
    ) -> "MovementAudit":
        return cls(
            movement_id=movement.movement_id,
            sku=movement.sku,
            location_id=movement.location_id,
            state=movement.state,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            delta=movement.delta,
            movement_type=movement.movement_type,
            reason=movement.reason,
            source=movement.source,
            actor=movement.actor,
            occurred_at=movement.occurred_at,
            recorded_at=datetime.now(timezone.utc),
            document_ref=movement.document_ref,
            correlation_id=movement.correlation_id,
        )
