from datetime import datetime, timedelta, timezone

import pytest

from stock_unico.inventory import (
    DuplicateMovement,
    InsufficientInventory,
    InventoryLedger,
    InventoryMovement,
    InventoryState,
    MovementType,
    OutOfOrderMovement,
)


NOW = datetime(2026, 9, 24, 20, 0, tzinfo=timezone.utc)


def movement(
    movement_id: str,
    delta: int,
    *,
    state: InventoryState = InventoryState.PHYSICAL,
    occurred_at: datetime = NOW,
    movement_type: MovementType = MovementType.RECEIPT,
) -> InventoryMovement:
    return InventoryMovement(
        movement_id=movement_id,
        sku="SKU-001",
        location_id="LIM-STORE-01",
        state=state,
        delta=delta,
        movement_type=movement_type,
        reason="test movement",
        occurred_at=occurred_at,
        source="unit-test",
        actor="inventory-system",
        document_ref="DOC-001",
        correlation_id="CORR-001",
    )


def test_applies_movement_and_keeps_audit_before_after() -> None:
    ledger = InventoryLedger()

    audit = ledger.apply(movement("MOV-001", 10))

    position = ledger.position("SKU-001", "LIM-STORE-01")
    assert position.physical == 10
    assert audit.previous_quantity == 0
    assert audit.new_quantity == 10
    assert audit.reason == "test movement"
    assert audit.document_ref == "DOC-001"


def test_keeps_inventory_states_separate() -> None:
    ledger = InventoryLedger()
    ledger.apply(movement("MOV-001", 10))
    ledger.apply(
        movement(
            "MOV-002",
            3,
            state=InventoryState.IN_TRANSIT,
            occurred_at=NOW + timedelta(seconds=1),
            movement_type=MovementType.TRANSFER_DISPATCH,
        )
    )

    position = ledger.position("SKU-001", "LIM-STORE-01")
    assert position.physical == 10
    assert position.in_transit == 3
    assert position.reserved == 0


def test_duplicate_movement_is_not_applied_twice() -> None:
    ledger = InventoryLedger()
    item = movement("MOV-001", 10)
    ledger.apply(item)

    with pytest.raises(DuplicateMovement):
        ledger.apply(item)

    assert ledger.position("SKU-001", "LIM-STORE-01").physical == 10
    assert len(ledger.audit_log) == 1


def test_rejects_negative_inventory_state() -> None:
    ledger = InventoryLedger()

    with pytest.raises(InsufficientInventory):
        ledger.apply(
            movement(
                "MOV-001",
                -1,
                movement_type=MovementType.SALE,
            )
        )

    assert ledger.position("SKU-001", "LIM-STORE-01").physical == 0
    assert not ledger.has_processed("MOV-001")
    assert ledger.audit_log == ()


def test_detects_out_of_order_movement_without_mutating_position() -> None:
    ledger = InventoryLedger()
    ledger.apply(movement("MOV-NEW", 10, occurred_at=NOW + timedelta(minutes=2)))

    with pytest.raises(OutOfOrderMovement):
        ledger.apply(movement("MOV-OLD", 5, occurred_at=NOW))

    assert ledger.position("SKU-001", "LIM-STORE-01").physical == 10
    assert not ledger.has_processed("MOV-OLD")


def test_history_is_scoped_to_sku_and_location() -> None:
    ledger = InventoryLedger()
    ledger.apply(movement("MOV-001", 10))
    ledger.apply(movement("MOV-002", -2, occurred_at=NOW + timedelta(seconds=1), movement_type=MovementType.SALE))

    history = ledger.history("SKU-001", "LIM-STORE-01")

    assert [item.movement_id for item in history] == ["MOV-001", "MOV-002"]
    assert history[-1].previous_quantity == 10
    assert history[-1].new_quantity == 8
