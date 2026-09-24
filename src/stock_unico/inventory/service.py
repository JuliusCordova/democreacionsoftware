"""In-memory inventory ledger for the first deterministic domain increment."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from .domain import (
    DuplicateMovement,
    InventoryMovement,
    InventoryPosition,
    MovementAudit,
    OutOfOrderMovement,
)


class InventoryLedger:
    """Apply movements once and retain immutable audit evidence.

    Persistence and distributed ordering are intentionally deferred. This
    component establishes domain behavior independent from infrastructure.
    """

    def __init__(self) -> None:
        self._positions: dict[tuple[str, str], InventoryPosition] = {}
        self._processed_ids: set[str] = set()
        self._latest_occurred_at: dict[tuple[str, str], datetime] = {}
        self._audit: list[MovementAudit] = []
        self._audit_by_position: dict[tuple[str, str], list[MovementAudit]] = defaultdict(list)

    def position(self, sku: str, location_id: str) -> InventoryPosition:
        key = (sku, location_id)
        return self._positions.get(
            key, InventoryPosition(sku=sku, location_id=location_id)
        )

    def apply(self, movement: InventoryMovement) -> MovementAudit:
        if movement.movement_id in self._processed_ids:
            raise DuplicateMovement(movement.movement_id)

        key = (movement.sku, movement.location_id)
        latest = self._latest_occurred_at.get(key)
        if latest is not None and movement.occurred_at < latest:
            raise OutOfOrderMovement(
                f"{movement.movement_id} occurred at {movement.occurred_at.isoformat()} "
                f"before latest accepted movement {latest.isoformat()}"
            )

        previous = self.position(movement.sku, movement.location_id)
        previous_quantity = previous.quantity(movement.state)
        updated = previous.apply_delta(movement.state, movement.delta)

        audit = MovementAudit.from_movement(
            movement=movement,
            previous_quantity=previous_quantity,
            new_quantity=updated.quantity(movement.state),
        )

        self._positions[key] = updated
        self._processed_ids.add(movement.movement_id)
        self._latest_occurred_at[key] = movement.occurred_at
        self._audit.append(audit)
        self._audit_by_position[key].append(audit)
        return audit

    def history(self, sku: str, location_id: str) -> tuple[MovementAudit, ...]:
        return tuple(self._audit_by_position[(sku, location_id)])

    def has_processed(self, movement_id: str) -> bool:
        return movement_id in self._processed_ids

    @property
    def audit_log(self) -> tuple[MovementAudit, ...]:
        return tuple(self._audit)
