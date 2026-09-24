"""Executable Inventory Core smoke scenario."""

from datetime import datetime, timedelta, timezone

from stock_unico.inventory import (
    DuplicateMovement,
    InventoryLedger,
    InventoryMovement,
    InventoryState,
    MovementType,
)


def sample(
    movement_id: str,
    delta: int,
    when: datetime,
    movement_type: MovementType,
) -> InventoryMovement:
    return InventoryMovement(
        movement_id=movement_id,
        sku="SKU-DEMO-001",
        location_id="LIM-STORE-01",
        state=InventoryState.PHYSICAL,
        delta=delta,
        movement_type=movement_type,
        reason="Sprint 1 smoke",
        occurred_at=when,
        source="smoke",
        actor="stock-unico",
        correlation_id="SPRINT-1-SMOKE",
    )


def main() -> None:
    ledger = InventoryLedger()
    now = datetime.now(timezone.utc)

    receipt = sample("SMOKE-RECEIPT", 10, now, MovementType.RECEIPT)
    sale = sample("SMOKE-SALE", -2, now + timedelta(seconds=1), MovementType.SALE)

    ledger.apply(receipt)
    ledger.apply(sale)

    duplicate_blocked = False
    try:
        ledger.apply(receipt)
    except DuplicateMovement:
        duplicate_blocked = True

    position = ledger.position("SKU-DEMO-001", "LIM-STORE-01")
    assert position.physical == 8
    assert duplicate_blocked
    assert len(ledger.audit_log) == 2

    print(
        {
            "status": "ok",
            "component": "inventory-core",
            "physical": position.physical,
            "duplicate_blocked": duplicate_blocked,
            "audit_records": len(ledger.audit_log),
        }
    )


if __name__ == "__main__":
    main()
