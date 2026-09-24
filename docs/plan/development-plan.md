# Plan de desarrollo — NovaRetail Stock Único

**Metodología:** PA-SDD — Progressive Agentic Spec-Driven Development  
**Modelo operativo de entrega:** GitHub → Validación → Cloud Shell → Evidencia → Merge  
**Estado:** Activo  
**Fuente de verdad funcional:** `docs/specs/stock-unico-spec.md`  
**Patrones adoptados:** `docs/patterns/devpattern-stock-unico.md`

---

## 1. Objetivo

Construir Stock Único de forma incremental, trazable y verificable, manteniendo el core transaccional determinístico y agregando capacidades agénticas únicamente cuando exista valor y evidencia que lo justifique.

## 2. Triangulación de desarrollo

```text
SPEC / DevPattern
       ↓
Issue GitHub
       ↓
feature/sprint-N-...
       ↓
Desarrollo en GitHub
       ↓
Tests + GitHub Actions
       ↓
Pull Request
       ↓
Cloud Shell
       ↓
Checkout exacto del SHA del PR
       ↓
Validación real
       ↓
docs/evidence/generated/<timestamp>/
       ↓
Commit de evidencia
       ↓
PR verde
       ↓
MERGE
       ↓
Siguiente incremento
```

**Regla principal:** GitHub construye y controla. Cloud Shell certifica.

## 3. Roadmap

| Sprint | Incremento | Resultado verificable |
|---|---|---|
| Sprint 0 | Engineering Foundation | estructura, CI, Makefile, tests, contratos base |
| Sprint 1 | Inventory Core | stock físico/utilizable/disponible + movimientos |
| Sprint 2 | Availability API | consultar disponibilidad por SKU/ubicación |
| Sprint 3 | Reservation Engine | reservar, TTL, expiración, concurrencia, idempotencia |
| Sprint 4 | Checkout / Order | pago → confirmación → pedido → compensación |
| Sprint 5 | Fulfillment | asignación, preparación, faltante, entrega |
| Sprint 6 | Event-driven | eventos, retry, DLQ, idempotencia, trazabilidad |
| Sprint 7 | Frontend operativo | experiencia tienda/operaciones con Nielsen |
| Sprint 8 | Observabilidad | métricas, auditoría, health, correlation IDs |
| Sprint 9 | IA — recomendaciones | agente gobernado sobre el core existente |
| Sprint 10 | Hardening MVP | seguridad, performance, E2E, rollback, evidencia |

## 4. Estrategia por sprint

Cada sprint debe contener:
1. Issue trazable.
2. Branch `feature/sprint-N-<nombre>`.
3. Alcance acotado.
4. Código y contratos.
5. Unit tests.
6. Integration/contract tests cuando aplique.
7. Make targets reproducibles.
8. GitHub Actions.
9. PR con criterios de aceptación.
10. Validación en Cloud Shell.
11. Evidencia generada.
12. Merge solo con gate verde.

## 5. Evidencia

Cada validación en Cloud Shell generará:

```text
docs/evidence/generated/<UTC_TIMESTAMP>/
├── README.md
├── metadata.json
├── unit_tests.json
├── compile.json
├── smoke.json
└── ...otros checks según sprint
```

Metadata mínima:
```yaml
git_sha: <sha-validado>
branch: <branch>
timestamp_utc: <timestamp>
unit_tests: PASS|FAIL
compile: PASS|FAIL
smoke: PASS|FAIL
```

## 6. Definition of Done

Un incremento está terminado cuando:
- está trazado a SPEC;
- cumple criterios de aceptación;
- tiene tests;
- compila;
- smoke test pasa;
- no rompe contratos existentes;
- es observable cuando aplica;
- registra evidencia reproducible;
- el PR refleja el SHA validado;
- Cloud Shell confirma el comportamiento;
- el merge conserva trazabilidad.

## 7. Estrategia arquitectónica

### Core determinístico
- inventario;
- disponibilidad;
- reservas;
- pago/pedido;
- compensaciones;
- transferencias;
- auditoría;
- autorización.

### IA
Se introduce después del core y mediante tools gobernadas:
- detección de anomalías;
- recomendación de redistribución;
- explicación de divergencias;
- recomendación de alternativas;
- análisis operacional.

**Regla:** la autonomía nunca reemplaza las garantías transaccionales del inventario.

## 8. Sprint 0 — Engineering Foundation

### Objetivo
Dejar lista la fábrica de desarrollo y validación antes de implementar lógica de negocio.

### Alcance
- estructura base del proyecto;
- paquete Python;
- tests;
- Makefile;
- GitHub Actions;
- script de validación Cloud Shell;
- carpeta de evidencia;
- convenciones de branches/PR;
- baseline de contracts;
- health/smoke mínimo.

### Comandos mínimos
```bash
make test
make compile
make smoke
make evidence
```

### Criterios de aceptación
- `make test` retorna PASS.
- `make compile` retorna PASS.
- `make smoke` retorna PASS.
- `make evidence` genera una carpeta versionable en `docs/evidence/generated/`.
- GitHub Actions ejecuta los checks principales en PR.
- El proyecto puede clonarse y validarse desde Cloud Shell sin pasos manuales no documentados.

## 9. Convención de branches

```text
feature/sprint-0-engineering-foundation
feature/sprint-1-inventory-core
feature/sprint-2-availability-api
...
```

## 10. Convención de PR

Cada PR debe incluir:
- objetivo;
- SPEC / HU / RF involucrados;
- alcance;
- archivos relevantes;
- tests;
- riesgos;
- Cloud Shell gate;
- SHA validado;
- ubicación de evidencia.

## 11. Regla de promoción

No se promueve por percepción. Se promueve por evidencia reproducible.
