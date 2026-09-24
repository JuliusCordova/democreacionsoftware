# Sprint 1 — Inventory Core

**Issue:** #3  
**Branch:** `feature/sprint-1-inventory-core`  
**Estado:** Candidate

## Trazabilidad

- HU-11 — Registrar movimientos de inventario
- HU-12 — Conteo y ajuste autorizado
- HU-13 — Gestionar transferencias
- RF-001, RF-018..023
- RNF-008, RNF-011

## Implementado en este incremento

- posición operacional por SKU + ubicación;
- estados separados: physical, reserved, committed, blocked, damaged, in_transit, pending_receipt;
- movimientos tipados;
- aplicación determinística de deltas;
- rechazo de cantidades negativas;
- idempotencia/deduplicación por movement_id;
- detección explícita de movimientos fuera de orden;
- auditoría inmutable en memoria con before/after, razón, actor, fuente, documento y correlación;
- historial por SKU/ubicación;
- tests unitarios de invariantes;
- smoke ejecutable de Inventory Core.

## Decisiones deliberadamente diferidas

- fórmula ATP/disponibilidad vendible: Sprint 2 y decisión configurable;
- persistencia definitiva: adapter posterior;
- concurrencia distribuida: Sprint 3;
- Pub/Sub, retry y DLQ: Sprint 6;
- autorización de ajustes: boundary de aplicación/seguridad posterior;
- IA: Sprint 9.

## Gate

El candidato debe pasar GitHub Actions y posteriormente validarse en Cloud Shell sobre el SHA exacto del PR.
