# Stock Único — Especificación funcional inicial

**Proyecto:** NovaRetail — Stock Único  
**Estado:** Baseline inicial para discovery / SDD  
**Fuente:** entrevistas de CEO, Supply Chain/Inventarios y E-commerce/Tiendas  
**Objetivo del documento:** convertir el caso de negocio en historias de usuario, requerimientos funcionales, requerimientos no funcionales y criterios de aceptación, manteniendo explícitas las decisiones todavía no cerradas.

---

## 1. Visión del producto

NovaRetail requiere una solución que consolide una interpretación operativa única de la disponibilidad de inventario, administre reservas y promesas de entrega, y soporte operaciones omnicanal como despacho a domicilio, retiro en tienda y preparación desde tienda.

El alcance inicial recomendado por negocio es tecnología y pequeños electrodomésticos en Lima. La solución debe integrarse progresivamente con los sistemas existentes, sin exigir un reemplazo masivo en una sola etapa.

### Objetivos de negocio

- Reducir cancelaciones por falta de stock.
- Reducir sobreventa.
- Mejorar el cumplimiento de la promesa de entrega.
- Aprovechar inventario de tiendas para atender pedidos digitales cuando sea conveniente y rentable.
- Mejorar exactitud de inventario y trazabilidad de diferencias.
- Reducir reservas vencidas sin conversión.
- Mantener continuidad de venta aun cuando una integración se retrase.

### KPIs iniciales

- Tasa de cancelación por falta de stock.
- Exactitud de inventario.
- Pedidos entregados dentro de la promesa.
- Porcentaje de ventas omnicanal.
- Rotación de inventario.
- Quiebres de stock.
- Costo de preparación por pedido.
- Porcentaje de reservas vencidas sin convertirse en venta.
- Tiempo de preparación.
- Reasignaciones, sustituciones y cancelaciones por causa.

---

## 2. Principios de diseño

1. **La disponibilidad para consulta y la confirmación de reserva no son la misma operación.**
2. **La consulta puede tolerar consistencia eventual controlada; la confirmación de reserva requiere control transaccional/concurrencia.**
3. **Los reintentos deben ser idempotentes.**
4. **Inventario físico, disponible, reservado, comprometido, bloqueado, dañado, en tránsito y pendiente de recepción son estados distintos.**
5. **El stock en tránsito no es vendible por defecto hasta la recepción.**
6. **Toda mutación de inventario debe ser auditable.**
7. **La solución debe soportar modo degradado y comunicar la frescura/confiabilidad del dato.**
8. **Pago, pedido y reserva deben correlacionarse de extremo a extremo y contar con compensaciones controladas ante fallas.**
9. **La IA puede recomendar, priorizar, anticipar demanda o detectar anomalías; no puede crear stock ni saltarse controles transaccionales.**
10. **La solución debe minimizar exposición de datos personales al personal operativo.**

---

## 3. Actores

- Cliente.
- Cajero / canal POS.
- Preparador de tienda.
- Supervisor de tienda.
- Operador logístico.
- E-commerce / checkout.
- Sistema de pagos.
- Sistemas de inventario heredados.
- Sistemas de almacén/centro de distribución.
- Administrador funcional.
- Auditor / analista de operaciones.
- Motor de disponibilidad y reservas.
- Motor de promesa.
- Agente IA opcional de recomendación/operaciones.

---

## 4. Épicas

- **EP-01 — Disponibilidad unificada**
- **EP-02 — Reservas y concurrencia**
- **EP-03 — Checkout, pago y pedido**
- **EP-04 — Promesa y sourcing omnicanal**
- **EP-05 — Preparación, retiro y entrega**
- **EP-06 — Inventario, conteos, ajustes y transferencias**
- **EP-07 — Integración, eventos y modo degradado**
- **EP-08 — Auditoría, seguridad y observabilidad**
- **EP-09 — Analítica operativa e IA asistiva**

---

## 5. Historias de usuario y criterios de aceptación

### HU-01 — Consultar disponibilidad omnicanal
**Como** cliente o canal de venta  
**quiero** consultar disponibilidad por SKU y modalidad  
**para** conocer opciones reales de compra, entrega o retiro.

**Criterios de aceptación**
- Dado un SKU y contexto de entrega/retiro, cuando se consulta disponibilidad, entonces la respuesta muestra ubicaciones candidatas y cantidad disponible calculada según reglas vigentes.
- La respuesta identifica modalidad aplicable, fecha/promesa estimada y vigencia/frescura del dato.
- Un producto no apto para venta digital no se ofrece en ese canal aunque exista físicamente.
- Si el dato está degradado o desactualizado por encima del umbral configurado, la respuesta lo marca y aplica la política de degradación definida.
- La consulta no crea una reserva.

### HU-02 — Calcular Available-to-Promise
**Como** responsable de inventarios  
**quiero** que la disponibilidad se calcule con reglas parametrizables  
**para** aplicar políticas distintas por categoría, tienda, campaña y modalidad.

**Criterios de aceptación**
- El cálculo considera como mínimo stock utilizable, reservas, compromisos y stock de seguridad.
- Las reglas pueden variar por categoría, ubicación, campaña y modalidad.
- Cada cálculo conserva versión de regla aplicada.
- El sistema permite explicar qué componentes determinaron la cantidad vendible.
- La fórmula exacta queda como decisión de negocio configurable y no codificada de forma irreversible.

### HU-03 — Crear reserva idempotente
**Como** checkout  
**quiero** reservar temporalmente unidades cuando el cliente inicia pago o confirma pedido  
**para** evitar sobreventa sin bloquear inventario indefinidamente.

**Criterios de aceptación**
- La solicitud usa una clave de idempotencia/correlación.
- Repetir la misma solicitud con la misma clave no duplica la reserva.
- Una reserva registra origen, SKU, cantidad, ubicación, creación, expiración y estado.
- La creación falla de manera controlada si ya no existe disponibilidad suficiente.
- Reservas concurrentes no pueden comprometer más stock del permitido.
- La reserva tiene expiración configurable.

### HU-04 — Confirmar, liberar o vencer reserva
**Como** motor de órdenes  
**quiero** cambiar el estado de una reserva de forma controlada  
**para** reflejar el resultado real del proceso de compra.

**Criterios de aceptación**
- Una reserva puede pasar por estados al menos: creada, confirmada, liberada, vencida y reasignada.
- Una reserva vencida libera capacidad vendible según reglas.
- Confirmar o liberar varias veces la misma reserva produce un resultado idempotente.
- Cada transición registra actor/sistema, fecha y razón.
- No se permiten transiciones inválidas de estado.

### HU-05 — Correlacionar intento, pago, pedido y reserva
**Como** operación de e-commerce  
**quiero** trazabilidad única del checkout  
**para** evitar pagos sin pedido o reservas confirmadas sin trazabilidad.

**Criterios de aceptación**
- Existe un identificador de correlación común o relaciones inequívocas entre intento, pago, pedido y reserva.
- Un callback/reintento duplicado de pago no crea un segundo pedido.
- Si el pago es aprobado y el pedido no puede confirmarse, se activa una compensación registrada.
- Si la reserva no puede confirmarse, el sistema no presenta una venta finalizada como exitosa.
- Los estados divergentes son detectables y visibles para operación.

### HU-06 — Obtener promesa antes del pago
**Como** cliente  
**quiero** conocer una promesa confiable antes de pagar  
**para** decidir entre entrega o retiro.

**Criterios de aceptación**
- La promesa incluye modalidad, ubicación relevante, fecha/ventana y vigencia.
- La promesa considera disponibilidad, capacidad, horario, costo y restricciones aplicables.
- Si la promesa cambia posteriormente, el evento queda trazado.
- El checkout puede detectar que una promesa quedó obsoleta antes de confirmar.

### HU-07 — Seleccionar ubicación de fulfillment
**Como** motor de sourcing  
**quiero** evaluar ubicaciones candidatas  
**para** asignar el pedido cumpliendo disponibilidad, costo y promesa.

**Criterios de aceptación**
- Se consideran al menos disponibilidad, distancia, capacidad de preparación, horario, costo, prioridad, fecha prometida y restricciones del producto.
- Una tienda no habilitada para preparación en una franja no es seleccionada para esa modalidad.
- La decisión registra reglas y factores aplicados.
- Para carritos multi-SKU se soporta la decisión de consolidar o dividir el pedido según política configurable.

### HU-08 — Generar tarea de preparación
**Como** preparador de tienda  
**quiero** recibir una cola priorizada de pedidos  
**para** preparar unidades dentro del tiempo objetivo.

**Criterios de aceptación**
- Tras confirmar un pedido se genera una tarea asociada a pedido, ubicación y líneas.
- La cola soporta priorización.
- El preparador puede iniciar, validar SKU/cantidad, reportar faltante/daño y finalizar.
- Cuando exista ubicación interna del producto, puede mostrarse.
- El preparador no visualiza datos personales no necesarios.

### HU-09 — Gestionar faltante durante preparación
**Como** preparador o sistema de operaciones  
**quiero** reportar que una unidad reservada no fue encontrada  
**para** activar alternativas en lugar de cancelar automáticamente.

**Criterios de aceptación**
- El faltante registra SKU, ubicación, cantidad, usuario/sistema, momento y motivo.
- El sistema busca otras ubicaciones elegibles según reglas.
- La promesa puede recalcularse.
- Se generan alternativas posibles: nueva fecha, otra tienda, sustitución o devolución, según configuración.
- Toda reasignación conserva trazabilidad con la reserva/pedido original.

### HU-10 — Retiro en tienda
**Como** cliente  
**quiero** retirar un pedido preparado en una tienda  
**para** completar una compra omnicanal.

**Criterios de aceptación**
- El cliente puede seleccionar una tienda elegible al comprar.
- Cuando el pedido está listo se genera una notificación/código de recojo.
- La entrega valida el mecanismo de identificación definido.
- El retiro queda registrado.
- Si vence el plazo de recojo, se aplica la política de liberación/compensación configurada.

### HU-11 — Registrar movimientos de inventario
**Como** sistema de inventario  
**quiero** registrar movimientos provenientes de múltiples orígenes  
**para** mantener una vista operativa consolidada.

**Criterios de aceptación**
- Se soportan como mínimo ventas, pedidos web, recepciones, transferencias, devoluciones, anulaciones, conteos, ajustes, daños, robos y cambios de estado.
- Cada evento tiene identificador único/origen.
- Eventos duplicados no se aplican dos veces.
- Eventos fuera de orden son detectados y gestionados según política.
- La mutación resultante conserva saldo anterior, saldo nuevo, razón y documento relacionado cuando aplique.

### HU-12 — Conteo y ajuste autorizado
**Como** supervisor de inventario  
**quiero** registrar conteos y ajustes con evidencia  
**para** corregir diferencias sin perder trazabilidad.

**Criterios de aceptación**
- Un ajuste requiere usuario autorizado.
- Se registra motivo y evidencia/referencia.
- El valor anterior y nuevo quedan auditados.
- El sistema distingue conteo físico de ajuste contable/operativo.
- Los ajustes generan un evento consumible por el resto de componentes.

### HU-13 — Gestionar transferencias
**Como** Supply Chain  
**quiero** administrar transferencias entre ubicaciones  
**para** conocer unidades solicitadas, despachadas, en tránsito y recibidas.

**Criterios de aceptación**
- La transferencia registra origen, destino y cantidades solicitadas, despachadas y recibidas.
- Se registran diferencias.
- Stock en tránsito no se publica como disponible por defecto.
- La recepción produce el cambio de estado correspondiente.
- Una futura promesa sobre stock en tránsito solo puede habilitarse mediante regla explícita.

### HU-14 — Operar en modo degradado
**Como** canal de venta  
**quiero** continuar operando de forma segura cuando una integración se retrasa  
**para** evitar detener ventas o mostrar información engañosa.

**Criterios de aceptación**
- El sistema identifica dependencia degradada y edad del dato.
- La política puede restringir cantidades, ubicaciones o modalidades según nivel de confianza.
- La confirmación de reserva no usa silenciosamente una vista que exceda el umbral permitido.
- El usuario/canal recibe un estado interpretable y no un dato presentado falsamente como exacto.
- Al restablecerse la integración se reconcilian eventos pendientes.

### HU-15 — Auditar inventario extremo a extremo
**Como** auditor o responsable de Supply Chain  
**quiero** reconstruir la secuencia de cambios de un SKU/ubicación  
**para** investigar diferencias y duplicidades.

**Criterios de aceptación**
- Cada cambio registra evento de origen, documento relacionado cuando aplique, actor, timestamp, cantidad anterior, cantidad nueva y razón.
- La secuencia permite detectar duplicados y eventos fuera de orden.
- Se puede consultar el historial por SKU, ubicación, pedido/reserva o correlación.
- Los registros de auditoría no pueden ser modificados por usuarios operativos ordinarios.

### HU-16 — Métricas operativas
**Como** responsable de negocio  
**quiero** medir desempeño omnicanal  
**para** identificar causas de cancelación, incumplimiento y pérdida de conversión.

**Criterios de aceptación**
- Se exponen eventos/datos para calcular cancelación por stock, exactitud, cumplimiento de promesa, conversión, abandono, no disponibilidad, tiempo de preparación, reasignaciones, cancelaciones y sustituciones.
- Las causas pueden atribuirse al menos a inventario, pago, logística o tienda.
- La analítica histórica no bloquea transacciones operativas.

### HU-17 — Detectar anomalías con IA (opcional)
**Como** responsable de inventarios  
**quiero** recibir alertas de patrones anómalos  
**para** priorizar investigación de posibles errores, pérdidas o desincronización.

**Criterios de aceptación**
- El agente/modelo solo recomienda o alerta; no modifica inventario por sí mismo.
- Cada recomendación muestra evidencia/contexto mínimo que permita revisión humana.
- Una recomendación puede aceptarse, descartarse o escalarse.
- Las decisiones humanas quedan registradas.
- El fallo del componente IA no impide reservas, ventas ni movimientos transaccionales.

### HU-18 — Recomendar redistribución con IA (opcional)
**Como** Supply Chain  
**quiero** recomendaciones de redistribución considerando demanda e inventario  
**para** mejorar disponibilidad omnicanal.

**Criterios de aceptación**
- La recomendación identifica SKU, origen, destino, cantidad sugerida y fundamentos.
- No crea automáticamente una transferencia operativa sin aprobación/regla explícita.
- Las recomendaciones usan solo datos autorizados.
- Se puede medir adopción e impacto de la recomendación.

---

## 6. Requerimientos funcionales

| ID | Requerimiento |
|---|---|
| RF-001 | Mantener una vista operacional de inventario por SKU y ubicación diferenciando estados relevantes. |
| RF-002 | Calcular disponibilidad vendible mediante reglas configurables por categoría, ubicación, campaña y modalidad. |
| RF-003 | Consultar disponibilidad sin generar reserva. |
| RF-004 | Crear reservas temporales con expiración. |
| RF-005 | Garantizar idempotencia en creación y transición de reservas. |
| RF-006 | Aplicar control de concurrencia al confirmar disponibilidad/reserva. |
| RF-007 | Confirmar, liberar, vencer y reasignar reservas mediante transiciones válidas. |
| RF-008 | Correlacionar checkout, intento de pago, pago, pedido y reserva. |
| RF-009 | Ejecutar compensaciones ante inconsistencias entre pago, pedido y reserva. |
| RF-010 | Calcular una promesa de entrega/retiro con vigencia. |
| RF-011 | Seleccionar ubicaciones candidatas usando disponibilidad, distancia, capacidad, horario, costo, prioridad, promesa y restricciones. |
| RF-012 | Soportar pedidos abastecidos desde una o varias ubicaciones según reglas. |
| RF-013 | Generar y priorizar tareas de preparación. |
| RF-014 | Permitir validación por escaneo de SKU cuando el dispositivo/canal lo soporte. |
| RF-015 | Registrar faltantes, daños y excepciones durante preparación. |
| RF-016 | Rebuscar stock y recalcular promesa ante una excepción. |
| RF-017 | Gestionar retiro en tienda y expiración del plazo de recojo. |
| RF-018 | Ingerir movimientos desde canales en tiempo real y sistemas batch. |
| RF-019 | Detectar y neutralizar eventos duplicados. |
| RF-020 | Detectar eventos fuera de orden y aplicar una política definida. |
| RF-021 | Registrar conteos y ajustes autorizados con motivo y evidencia. |
| RF-022 | Gestionar transferencias origen-destino y estado en tránsito. |
| RF-023 | Mantener trazabilidad/auditoría de toda mutación de inventario. |
| RF-024 | Exponer frescura/edad de los datos usados para disponibilidad. |
| RF-025 | Aplicar políticas de operación degradada. |
| RF-026 | Reconciliar eventos/saldos luego de interrupciones o retrasos de integración. |
| RF-027 | Exponer eventos/datos operativos para analítica histórica y KPIs. |
| RF-028 | Aplicar control de acceso según rol para operaciones sensibles. |
| RF-029 | Limitar exposición de datos personales en interfaces de preparación. |
| RF-030 | Permitir configurar parámetros sin despliegues para TTL de reserva, stock de seguridad, reglas de sourcing y umbrales de frescura cuando sea técnicamente seguro. |
| RF-031 | Soportar productos serializados y permitir evolucionar a reserva por unidad exacta. |
| RF-032 | Permitir integración opcional con agentes/modelos IA de recomendación y anomalías sin otorgarles autoridad sobre transacciones de stock. |

---

## 7. Requerimientos no funcionales

| ID | Categoría | Requerimiento |
|---|---|---|
| RNF-001 | Rendimiento | Las consultas de disponibilidad deben responder con baja latencia; el SLO exacto debe cerrarse en discovery mediante prueba de carga. |
| RNF-002 | Rendimiento | La plataforma debe soportar picos de miles de consultas por segundo y al menos el orden de magnitud informado de 12,000 pedidos/hora. |
| RNF-003 | Consistencia | La confirmación de reserva debe evitar sobrecompromiso bajo concurrencia. |
| RNF-004 | Consistencia | Las vistas de catálogo/disponibilidad pueden usar consistencia eventual únicamente bajo umbrales explícitos de frescura. |
| RNF-005 | Idempotencia | Operaciones mutantes expuestas a reintentos deben aceptar identificador idempotente o equivalente. |
| RNF-006 | Disponibilidad | Una falla de una integración no debe causar una caída total si existe una política segura de degradación. |
| RNF-007 | Resiliencia | Debe existir retry controlado, circuit breaking o mecanismo equivalente y manejo de DLQ/eventos fallidos cuando aplique. |
| RNF-008 | Auditabilidad | Toda mutación crítica debe dejar evidencia suficiente para reconstrucción posterior. |
| RNF-009 | Seguridad | Autenticación y autorización deben seguir principio de mínimo privilegio. |
| RNF-010 | Privacidad | Interfaces operativas deben minimizar datos personales y registrar accesos sensibles cuando aplique. |
| RNF-011 | Integridad | Los mensajes/eventos deben incorporar identificadores que permitan deduplicación y correlación. |
| RNF-012 | Observabilidad | Métricas, logs y trazas deben permitir seguir una operación desde consulta/reserva hasta pago/pedido/preparación. |
| RNF-013 | Observabilidad | Deben existir alertas por lag, errores de integración, divergencia de estados, reservas huérfanas y tasas anómalas de cancelación. |
| RNF-014 | Escalabilidad | Los componentes de lectura y transacción deben poder escalar independientemente. |
| RNF-015 | Evolutividad | La solución debe integrarse con sistemas actuales y permitir migración gradual. |
| RNF-016 | Configurabilidad | Reglas de negocio variables deben externalizarse/configurarse cuando sea razonable. |
| RNF-017 | Recuperación | Deben definirse RTO/RPO por componente; los valores exactos son una decisión pendiente del negocio/arquitectura. |
| RNF-018 | Pruebas | Deben existir pruebas automatizadas de concurrencia, idempotencia, expiración, compensación y degradación. |
| RNF-019 | Datos | La analítica histórica debe desacoplarse del camino transaccional crítico. |
| RNF-020 | IA responsable | Componentes IA opcionales deben ser fail-open respecto de recomendaciones: su indisponibilidad no debe detener la operación transaccional. |
| RNF-021 | IA responsable | Las salidas IA deben ser observables, evaluables y sujetas a aprobación humana cuando impliquen acciones operativas. |
| RNF-022 | Usabilidad | Interfaces de tienda deben priorizar simplicidad, cola de trabajo clara, feedback inmediato y prevención de errores operativos. |

---

## 8. Criterios de aceptación end-to-end del MVP

### CA-E2E-01 — Reserva concurrente
Dado un SKU con una cantidad vendible limitada, cuando múltiples solicitudes concurrentes intentan reservar más unidades que las disponibles, entonces solo se confirman reservas hasta el límite permitido y no existe sobreventa por condición de carrera.

### CA-E2E-02 — Reintento idempotente
Dado un checkout que reintenta la misma creación de reserva por timeout, cuando se repite la operación con la misma clave idempotente, entonces se devuelve la reserva original o un resultado equivalente sin descontar inventario dos veces.

### CA-E2E-03 — Reserva vencida
Dada una reserva no confirmada cuyo TTL expiró, cuando corre el mecanismo de expiración, entonces cambia a vencida, libera inventario conforme a regla y registra el evento.

### CA-E2E-04 — Pago aprobado con error posterior
Dado un pago aprobado y una falla posterior al crear/confirmar el pedido, cuando el proceso detecta la inconsistencia, entonces ejecuta o agenda una compensación controlada, preserva trazabilidad y genera alerta operativa.

### CA-E2E-05 — Faltante en tienda
Dado un pedido asignado a tienda y una unidad no encontrada, cuando el preparador reporta faltante, entonces el sistema registra la excepción, intenta sourcing alternativo y recalcula la promesa antes de cancelar definitivamente cuando existan opciones configuradas.

### CA-E2E-06 — Integración atrasada
Dado un feed de inventario cuya frescura excede el umbral, cuando un canal consulta disponibilidad, entonces el sistema aplica la política de degradación y no presenta el dato como plenamente confiable.

### CA-E2E-07 — Auditoría
Dada cualquier modificación crítica de inventario, cuando un auditor consulta el historial, entonces puede identificar origen, documento/correlación, actor, momento, valor anterior, valor nuevo y motivo.

### CA-E2E-08 — Privacidad en preparación
Dado un preparador de tienda, cuando abre una tarea, entonces solo visualiza los datos necesarios para preparar/entregar el pedido según su rol.

### CA-E2E-09 — IA sin autoridad transaccional
Dada una recomendación de redistribución o anomalía generada por IA, cuando se produce la recomendación, entonces no se modifica saldo, reserva ni transferencia sin pasar por una operación autorizada y determinística.

---

## 9. Decisión: solución agéntica vs software tradicional

### Núcleo que debe ser software determinístico/transaccional
- Ledger/saldo operacional de inventario.
- Reservas y expiración.
- Control de concurrencia.
- Idempotencia.
- Confirmación/liberación de inventario.
- Correlación pago-pedido-reserva.
- Compensaciones.
- Transferencias y recepciones.
- Auditoría.
- Autorización.

### Capacidades apropiadas para agente/IA
- Detección de anomalías de inventario.
- Recomendaciones de redistribución.
- Explicación asistida de causas de divergencia.
- Priorización sugerida de excepciones.
- Recomendación de alternativas ante faltantes.
- Análisis de patrones de reservas vencidas/cancelaciones.

### Patrón recomendado
**Arquitectura híbrida:** servicios transaccionales gobernados + eventos + agente(s) asistivos con herramientas restringidas.  
El agente consume contexto y APIs autorizadas, puede proponer acciones, pero cualquier mutación crítica pasa por servicios de dominio con validaciones, autorización, idempotencia y auditoría.

---

## 10. Decisiones abiertas / preguntas de discovery

Estas preguntas no deben cerrarse por inferencia; requieren decisión explícita del negocio/arquitectura:

1. Fórmula exacta de Available-to-Promise por categoría/modalidad.
2. Duración/TTL de reserva por flujo y medio de pago.
3. Momento preciso de creación de reserva: inicio de pago vs confirmación de pedido, o política híbrida.
4. Política de partición de carrito multi-SKU.
5. Autoridad de datos por operación y sistema.
6. Estrategia exacta de compensación ante pago aprobado sin pedido.
7. Umbrales de frescura para modo normal/degradado.
8. Reglas de overselling controlado, si alguna categoría lo permite.
9. SLO de latencia por consulta y confirmación.
10. SLA/SLO, RTO y RPO.
11. Política de serialización por SKU/categoría.
12. Cuándo una reserva puede reasignarse de ubicación.
13. Identificación requerida para retiro en tienda.
14. Reglas de sustitución de producto.
15. Política futura para prometer stock en tránsito.
16. Retención de auditoría y evidencia.
17. Qué decisiones del agente IA requieren aprobación humana obligatoria.

---

## 11. Definition of Done funcional del MVP

Una historia se considera terminada cuando:
- Cumple sus criterios de aceptación.
- Tiene pruebas unitarias y de integración.
- Tiene pruebas de error/reintento cuando aplica.
- Emite logs/métricas/trazas suficientes.
- Respeta autorización y minimización de datos.
- Es idempotente si modifica estado y puede recibir reintentos.
- Tiene evidencia de prueba de concurrencia si toca stock/reservas.
- Documenta eventos/API y estados involucrados.
- No introduce dependencia obligatoria de IA en el camino transaccional.
- Mantiene trazabilidad hacia HU, RF/RNF y criterio de aceptación.

---

## 12. Trazabilidad mínima

| Épica | Historias principales | RF relacionados | RNF críticos |
|---|---|---|---|
| EP-01 Disponibilidad | HU-01, HU-02 | RF-001..003, RF-024, RF-030 | RNF-001..004, RNF-014 |
| EP-02 Reservas | HU-03, HU-04 | RF-004..007 | RNF-003, RNF-005, RNF-008, RNF-018 |
| EP-03 Checkout/pago | HU-05 | RF-008, RF-009 | RNF-005, RNF-007, RNF-012, RNF-013 |
| EP-04 Promesa/sourcing | HU-06, HU-07 | RF-010..012 | RNF-001, RNF-016 |
| EP-05 Preparación/retiro | HU-08..10 | RF-013..017, RF-029 | RNF-009, RNF-010, RNF-022 |
| EP-06 Inventario/transferencias | HU-11..13 | RF-018..023, RF-031 | RNF-008, RNF-011 |
| EP-07 Integración/degradación | HU-14 | RF-024..026 | RNF-006, RNF-007, RNF-017 |
| EP-08 Auditoría/seguridad | HU-15 | RF-023, RF-028, RF-029 | RNF-008..013 |
| EP-09 Analítica/IA | HU-16..18 | RF-027, RF-032 | RNF-019..021 |

---

## 13. Eventos de dominio iniciales

- InventoryReceived
- SaleRegistered
- InventoryAdjusted
- InventoryCounted
- InventoryDamaged
- TransferDispatched
- TransferReceived
- ReservationCreated
- ReservationConfirmed
- ReservationReleased
- ReservationExpired
- ReservationReassigned
- PaymentApproved
- PaymentRejected
- OrderConfirmed
- FulfillmentAssigned
- PickingStarted
- StockShortageReported
- PromiseRecalculated
- OrderReadyForPickup
- OrderDelivered

> Los nombres son una propuesta inicial de especificación y deberán alinearse al lenguaje ubicuo definitivo del equipo.

---

## 14. Notas para arquitectura

El documento fuente exige tomar decisiones explícitas sobre consistencia fuerte vs eventual, disponibilidad vs reserva, inventario agregado vs serializado, transacciones distribuidas entre reserva/pago/pedido, expiración/compensación, operación degradada y separación entre datos operativos y analítica histórica. Esta especificación mantiene esas decisiones visibles para que la arquitectura posterior las resuelva de forma trazable.
