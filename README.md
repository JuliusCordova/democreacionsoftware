# Demo Creación de Software — NovaRetail Stock Único

Este repositorio implementa el caso **Stock Único** usando **PA-SDD — Progressive Agentic Spec-Driven Development**, tomando como patrón de referencia el repositorio `JuliusCordova/DevPattern`.

## Fuente de verdad

- [Especificación funcional inicial](docs/specs/stock-unico-spec.md)
- [Patrones DevPattern aplicados al proyecto](docs/patterns/devpattern-stock-unico.md)

## Enfoque de desarrollo

```text
Business Intent
      ↓
Minimum Sufficient Specification
      ↓
UI / UX Pattern Selection
      ↓
Reusable Pattern Selection
      ↓
Architecture Decision
      ↓
Contracts / Evals
      ↓
Implementation
      ↓
Executable Evidence
      ↓
Promotion
      ↓
Observe
      ↓
Evolve the Spec
```

## Decisiones base

- Core de inventario/reservas/pago/pedido: determinístico y transaccional.
- Arquitectura: Simple Feature Slice donde baste; Hexagonal Slice en dominio crítico.
- Integración: event-driven donde el desacoplamiento sea necesario.
- IA/agentes: opcionales y progresivos.
- Single Agent first.
- Permission-aware / governed agent cuando se use IA con datos reales.
- Human approval para acciones agénticas consecuenciales.
- Evaluation + observability obligatorias para IA en MVP/Product.
- Nielsen heuristics como baseline de UI/UX.
- Cloud provider pendiente de decisión explícita.
- Cost-aware architecture: escalar con evidencia, no anticipación.

## Principio

> Minimum ceremony. Maximum evidence.
