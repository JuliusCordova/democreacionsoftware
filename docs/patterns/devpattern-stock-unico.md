# DevPattern aplicado a Stock Único

**Proyecto:** NovaRetail — Stock Único  
**Repositorio de patrones fuente:** JuliusCordova/DevPattern  
**Patrón rector:** PA-SDD — Progressive Agentic Spec-Driven Development  
**Principio:** Minimum ceremony. Maximum evidence.

---

## 1. Propósito

Este documento adopta formalmente los patrones de DevPattern para el desarrollo de Stock Único.

La solución se desarrollará bajo un enfoque progresivo:

Business Intent
→ Minimum Sufficient Specification
→ UI/UX Pattern Selection
→ Reusable Pattern Selection
→ Architecture Decision
→ Contracts / Evals
→ Implementation
→ Executable Evidence
→ Promotion
→ Observe
→ Evolve the Spec

La arquitectura, controles y nivel de formalidad crecerán con el riesgo, madurez, integraciones y criticidad del producto, no por cantidad de código ni por elapsed time.

---

## 2. Constitución de ingeniería adoptada

Se adoptan como principios obligatorios:

1. Spec before implementation.
2. Minimum sufficient ceremony.
3. Patterns before reinvention.
4. Simplicity before autonomy.
5. Single agent before multi-agent.
6. Contracts before integration.
7. Evals before trust.
8. Evidence before promotion.
9. Security and permissions by design.
10. Human control for high-risk actions.
11. Observable by default.
12. Cost is an architecture metric.
13. Reversible delivery.
14. Every meaningful failure becomes an eval.
15. Specs evolve with the product.

### Aplicación específica a Stock Único

- El inventario, reservas, pago, pedido, transferencias y auditoría permanecen bajo software determinístico.
- Los agentes se introducen solo donde razonamiento dinámico aporta valor.
- Ningún agente podrá saltarse autorización, concurrencia, idempotencia ni reglas transaccionales.
- Acciones con impacto material deberán pasar por controles determinísticos y, cuando corresponda, aprobación humana.
- Fallas relevantes de producción deberán transformarse en escenarios de regresión/evaluación.

---

## 3. Definition Pack seleccionado

Se adopta el **Minimum Sufficient Specification (MSS)**.

La especificación actual `docs/specs/stock-unico-spec.md` constituye la base de producto y deberá evolucionar para mantener al menos:

1. Business Intent
2. Scope
3. Out of Scope
4. Actors / Personas
5. User Stories
6. Functional Requirements
7. Non-Functional Requirements
8. Acceptance Criteria
9. Business Rules
10. Logical Data Model
11. Integrations
12. Edge Cases
13. Success Metrics
14. Agentic Extension cuando aplique

### Regla de trazabilidad

BUS
→ US
→ FR
→ BR
→ AC
→ TEST
→ EVIDENCE

Ninguna capacidad crítica debe quedar definida únicamente en código, prompt, SQL o interfaz.

---

## 4. Nivel de madurez inicial

### Estado recomendado: MVP orientado a validación

Stock Único ya presenta:
- múltiples sistemas externos;
- reglas de dominio significativas;
- concurrencia;
- integraciones transaccionales;
- requisitos de idempotencia;
- degradación controlada;
- auditoría;
- seguridad;
- eventos;
- capacidades IA opcionales.

Por ello, el desarrollo no debe tratarse como un FAST DEMO puramente simple para los slices críticos.

### Aplicación progresiva

| Área | Nivel inicial |
|---|---|
| Consulta de disponibilidad | MVP |
| Reservas | MVP con límites fuertes |
| Pago / pedido / compensación | MVP con límites fuertes |
| Preparación en tienda | MVP |
| Analítica | MVP |
| IA de anomalías | FAST DEMO → MVP |
| IA de redistribución | FAST DEMO → MVP |
| Multi-agent | No seleccionado inicialmente |

---

## 5. Patrón arquitectónico

### Patrón seleccionado: Hexagonal Slice donde el dominio es crítico

Se aplicará **Hexagonal Slice Architecture** a los slices con reglas relevantes, integraciones externas o alta criticidad.

Slices iniciales:

- Availability
- Reservation
- Order
- Payment Coordination
- Fulfillment
- Inventory Movement
- Transfer
- Audit
- Agentic Recommendations

### Simple Feature Slice

Se permitirá Simple Feature Slice para:
- prototipos;
- pantallas simples;
- componentes internos con bajo riesgo;
- experimentos IA tempranos.

### Regla anti-overengineering

No se creará un port, adapter, interface o layer solo porque el patrón lo permite.

Debe justificar al menos uno:
- aislar dependencia externa;
- permitir segunda implementación;
- aislar vendor;
- mejorar testabilidad;
- imponer separación de seguridad;
- permitir evolución independiente;
- proteger regla de negocio de infraestructura.

---

## 6. Pattern Packs seleccionados

### 6.1 Event-Driven

**Seleccionado: obligatorio para integración asíncrona relevante.**

Aplicación:
- movimientos de inventario;
- reservas;
- expiraciones;
- pago aprobado/rechazado;
- pedido confirmado;
- preparación;
- faltantes;
- transferencias;
- auditoría operacional.

Requisitos progresivos:
- event schema;
- correlation/run ID;
- deduplicación;
- idempotencia;
- retry;
- DLQ;
- outcome evidence;
- ordering cuando sea necesario.

---

### 6.2 Tool Calling

**Seleccionado para cualquier agente con acceso a capacidades externas.**

Todo tool deberá definir:
- name;
- description;
- input schema;
- output schema;
- side effect;
- reversibility;
- risk;
- timeout;
- retries;
- permissions;
- audit.

Para Stock Único:
- herramientas de lectura podrán consultar disponibilidad, eventos o históricos según permisos;
- herramientas de escritura deberán invocar servicios de dominio;
- no se expondrá escritura directa sobre tablas de inventario a un LLM.

---

### 6.3 Governed / Permission-Aware Agent

**Seleccionado para cualquier capacidad agéntica que acceda a datos reales.**

Reglas:
- identidad autenticada;
- autorización antes de retrieval o acción;
- least privilege;
- tools filtradas por permiso;
- auditoría;
- segregación de funciones cuando corresponda;
- políticas determinísticas fuera del prompt.

El agente nunca tendrá permisos más amplios que el usuario o capability delegada.

---

### 6.4 Human-in-the-Loop

**Seleccionado para acciones agénticas con impacto operacional.**

Casos iniciales:
- recomendación de redistribución;
- ajuste sugerido de inventario;
- decisiones excepcionales de sustitución;
- acciones con impacto financiero u operacional material.

Patrón:

Agent
→ Proposed Action
→ Human Approve / Reject
→ Domain Service Executes
→ Evidence

---

### 6.5 Evaluation & Observability

**Obligatorio para MVP/Product agentic systems.**

Capturar:
- model calls;
- tool calls;
- latency;
- errors;
- cost;
- guardrail outcomes;
- task/business outcome;
- prompt/model/agent version.

Para MVP:
- golden dataset versionado;
- tool-selection evals;
- trace grading;
- latency/cost monitoring;
- regression before release.

---

### 6.6 Context Engineering

**Seleccionado si se implementan asistentes/agentes.**

Reglas:
- mínimo contexto útil;
- distinguir instrucciones durables de contexto temporal;
- structured context;
- permission-aware context;
- prompt/version tracking;
- token budget;
- provenance cuando corresponda.

No se utilizará memoria persistente por defecto.

---

### 6.7 Single Agent

**Patrón agéntico inicial seleccionado.**

Un solo agente por capacidad coherente será la opción por defecto.

Ejemplo:
- Inventory Operations Assistant.

Solo podrá escalarse a Multi-Agent si aparece evidencia de:
- context isolation;
- security boundary;
- specialization;
- persistent tool-selection errors;
- ownership independiente;
- complejidad difícil de mantener en un único agente.

---

### 6.8 Multi-Agent

**No seleccionado inicialmente.**

No se implementará multi-agent por anticipación.

Se requiere ADR y evidencia que justifique:
- especialización;
- seguridad;
- aislamiento de contexto;
- escala;
- orquestación compleja.

---

### 6.9 RAG / GraphRAG

**No seleccionado para el core transaccional.**

Puede incorporarse únicamente si una capacidad IA necesita conocimiento documental.

Regla de escalamiento:
RAG
→ benchmark demuestra brecha relacional/global
→ GraphRAG

GraphRAG no será introducido por defecto.

---

### 6.10 Long-Running Agent

**No seleccionado inicialmente.**

Usar únicamente si aparece trabajo agéntico durable que necesite:
- resume;
- cancel;
- checkpoint;
- espera prolongada.

---

## 7. UI / UX Pattern Packs

### Nielsen baseline — obligatorio

Toda interfaz debe cumplir, de forma observable:

1. Visibility of system status.
2. Match with real-world language.
3. User control and freedom.
4. Consistency and standards.
5. Error prevention.
6. Recognition rather than recall.
7. Flexibility and efficiency.
8. Aesthetic and minimalist design.
9. Error diagnosis and recovery.
10. Help/documentation where necessary.

### Stock Único

Ejemplos:
- reservas en proceso deben mostrar estado;
- una falla no debe mostrarse como silencio;
- acciones irreversibles deben mostrar consecuencia;
- faltantes deben mostrar siguiente acción;
- personal de tienda debe ver lenguaje operacional, no terminología técnica;
- estados de stock deben ser consistentes en todas las pantallas.

### Feedback states

Mínimo:

IDLE
→ LOADING / PROCESSING
→ SUCCESS / WARNING / ERROR
→ RETRY / RECOVER

Para tareas largas:
- queued;
- running;
- waiting-for-user;
- waiting-for-system;
- cancelled;
- partially-completed.

---

## 8. Agentic UI

Si se expone una interfaz agéntica, debe indicar claramente si el agente está:

- interpretando;
- recuperando información;
- usando una herramienta;
- recomendando;
- esperando aprobación;
- ejecutando;
- entregando evidencia.

Debe distinguir:
- respuesta;
- recomendación;
- acción ejecutada.

Las acciones consecuenciales deberán mostrar antes de aprobación:
- acción propuesta;
- entidad afectada;
- motivo;
- inputs materiales;
- flags de riesgo/política;
- reversibilidad.

Después de ejecutar:
- estado;
- outcome;
- evidence/audit identifier.

---

## 9. Contratos obligatorios

### API / domain contracts

Los contratos deberán ser explícitos para:
- availability;
- reservation;
- order;
- payment coordination;
- fulfillment;
- inventory movement;
- transfer;
- audit.

### Event contracts

Cada evento deberá definir:
- event_id;
- event_type;
- version;
- occurred_at;
- correlation_id;
- producer;
- entity identifiers;
- payload;
- idempotency semantics cuando corresponda.

### Agent contract

Si existe agente:

```yaml
agent:
  purpose:
  inputs:
  outputs:
  tools:
  forbidden_actions:
  exit_conditions:
  max_turns:
  evals:
```

### Tool contract

```yaml
tool:
  name:
  description:
  input_schema:
  output_schema:
  side_effect:
  reversible:
  risk:
  timeout:
  retries:
  permissions:
  audit:
```

---

## 10. Evals antes de confianza

Toda capacidad agéntica debe definir casos antes de promoción.

### Escenarios mínimos

- resultado correcto con información suficiente;
- información faltante;
- datos conflictivos;
- tool no disponible;
- timeout;
- permiso denegado;
- intento de acción prohibida;
- recomendación insegura;
- retry;
- respuesta sin suficiente evidencia.

### Regla

Una capacidad no se considera confiable solo porque "funciona en una demo".

---

## 11. Evidence-Driven Delivery

### Evidencia mínima por cambio crítico

- unit tests;
- integration tests;
- concurrency test;
- idempotency test;
- contract tests;
- smoke;
- security checks;
- evals si hay IA;
- latency/cost data cuando aplique.

### Promotion

FAST DEMO
→ demo acceptance

MVP
→ evidence gate

PRODUCT
→ production promotion gate + rollback

---

## 12. Observabilidad

### Core tradicional

Medir al menos:
- throughput;
- latency;
- errors;
- event lag;
- retry;
- DLQ;
- stale inventory;
- reservation conflicts;
- orphan reservations;
- payment/order divergence;
- preparation failures;
- cancellations by cause.

### IA

Medir:
- tool selection;
- recommendation acceptance;
- invalid/blocked actions;
- eval score;
- latency;
- cost per successful outcome;
- business impact.

---

## 13. Reversible delivery

Los despliegues deberán soportar:
- versionado;
- rollback;
- controlled promotion.

Cambios de contrato incompatibles deben utilizar estrategia explícita de versionado/migración.

---

## 14. Cost-aware architecture

El costo se considera métrica arquitectónica.

Principios:
- no pagar por escala antes de necesitarla;
- no escoger una opción barata que genere un migration trap evitable;
- escalar solo el componente que presenta evidencia de limitación;
- medir costo por outcome exitoso para capacidades IA.

Antes de seleccionar cloud components deberá definirse un Cost Envelope por ambiente/madurez.

---

## 15. Cloud-neutral first

La especificación de dominio y los Pattern Packs permanecerán vendor-neutral.

El proveedor se seleccionará después mediante Component Architecture Profile.

Flujo:

Definition
→ Architecture Pattern
→ Pattern Packs
→ Component Architecture Profile
→ Implementation

No se fijará Azure, GCP, AWS o Fabric sin una decisión explícita.

---

## 16. Criterios de escalamiento arquitectónico

Una capacidad puede incrementar complejidad cuando exista evidencia de:

- mayor tráfico;
- requisitos de disponibilidad más fuertes;
- aislamiento/seguridad;
- nuevas integraciones;
- ejecución asíncrona o long-running;
- sensibilidad de datos;
- governance;
- operación 24x7;
- limitaciones comprobadas de latencia/costo;
- necesidad real de múltiples agentes.

---

## 17. Decisiones actuales

| Decisión | Estado |
|---|---|
| PA-SDD | Adoptado |
| MSS | Adoptado |
| Hexagonal Slice para dominio crítico | Adoptado |
| Simple Slice para capacidades simples | Adoptado |
| Event-driven | Adoptado |
| Deterministic core | Adoptado |
| Single Agent first | Adoptado |
| Multi-Agent | No seleccionado |
| Governed Agent | Adoptado si hay IA |
| Tool Calling | Adoptado si hay IA |
| Human Approval | Adoptado para acciones IA consecuenciales |
| Eval + Observability | Adoptado |
| RAG | Condicional |
| GraphRAG | No seleccionado |
| Long-running agent | No seleccionado |
| Nielsen UI baseline | Adoptado |
| Cost-aware selection | Adoptado |
| Cloud provider | Pendiente |

---

## 18. Definition of Done ampliada

Una funcionalidad estará lista cuando:

- tiene especificación suficiente;
- usa solo los Pattern Packs necesarios;
- arquitectura está justificada;
- cumple aceptación;
- tiene contracts;
- tiene tests;
- tiene evidencia;
- es observable;
- respeta permisos;
- permite rollback cuando aplica;
- actualiza spec si el comportamiento cambió;
- una falla significativa agrega test/eval de regresión.

---

## 19. Regla rectora

> Build from explicit intent. Start simple. Add architecture, autonomy and controls only when they protect something measurable.

Para Stock Único:

> La autonomía nunca reemplaza las garantías transaccionales del inventario.
