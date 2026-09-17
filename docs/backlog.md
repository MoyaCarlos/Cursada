# Backlog

Épicas e historias de usuario (HU), formato `feature/HU-XX-nombre-corto` para
ramas. Cada HU se especifica con Spec Kit antes de implementarse (ver
`CLAUDE.md` → SDD).

## Épica 1 — Materias
- **HU-01** ✅ (`specs/001-gestion-materias/`): Como usuario quiero crear,
  editar y eliminar materias para organizar tareas y exámenes por asignatura.

## Épica 2 — Tareas
- **HU-02** ✅ (`specs/002-crear-tarea/`): Crear tarea pendiente (materia,
  título, descripción, fecha límite, prioridad).
- **HU-03** ✅ (`specs/003-editar-eliminar-tarea/`): Editar/eliminar una
  tarea existente.
- **HU-04** ✅ (`specs/004-cambiar-estado-tarea/`): Cambiar el estado de una
  tarea (pendiente / en progreso / completada).
- **HU-05**: Ver listado de tareas pendientes ordenado por fecha límite.

## Épica 3 — Exámenes
- **HU-06**: Crear examen (materia, tema, fecha, hora, modalidad, notas).
- **HU-07**: Editar/eliminar un examen existente.
- **HU-08**: Ver listado de próximos exámenes ordenado por fecha.

## Épica 4 — Recordatorios
- **HU-09**: Configurar anticipación de recordatorio al crear/editar una
  tarea o examen (ej: 3 días antes, 2 horas antes).
- **HU-10**: El motor de recordatorios revisa periódicamente los eventos y
  detecta cuáles corresponde disparar.
- **HU-11**: Registrar el envío de un recordatorio para evitar duplicados si
  el motor vuelve a correr.

## Épica 5 — Notificaciones
- **HU-12**: Recibir notificación de escritorio nativa cuando se dispara un
  recordatorio.
- **HU-13**: Configurar cuenta de email (SMTP) para el envío de recordatorios.
- **HU-14**: Recibir recordatorio por email.
- **HU-15**: Elegir qué canales de notificación están activos, desde una
  pantalla de configuración.

## Épica 6 — Interfaz
- **HU-16**: Ventana principal con vista unificada de "próximos pendientes"
  (tareas + exámenes por fecha).
- **HU-17**: Ícono en la bandeja del sistema con acceso rápido (abrir
  ventana / salir).
- **HU-22**: Filtrar el listado de pendientes por estado
  (pendiente/completado), materia y rango de fechas.

## Épica 7 — Empaquetado y distribución
- **HU-18**: Generar ejecutable standalone para Linux (PyInstaller).
- **HU-19**: Generar ejecutable standalone para Windows (PyInstaller).
- **HU-20**: Configurar autoarranque de la app al iniciar sesión, en Linux y
  Windows.

## Backlog futuro (fuera del MVP)
- **HU-21**: Enviar recordatorio vía bot de Telegram (pendiente hasta ver si
  se necesita).

## Mapeo a fases de desarrollo
| Fase | Historias |
|------|-----------|
| 1 | HU-01 a HU-08, HU-16 |
| 2 | HU-09, HU-10, HU-11, HU-12 |
| 3 | HU-13, HU-14, HU-15 |
| 4 | HU-17, HU-18, HU-19, HU-20 |
| 6 (interfaz, transversal) | HU-22 |
| Futuro | HU-21 |

## Notas de diseño relevantes para especificar (ver también CLAUDE.md y
docs/modelo-datos.md)
- HU-22: "completado" se resuelve distinto por tipo de evento — para tareas
  es `estado_id`, para exámenes se infiere por fecha (ver
  `docs/modelo-datos.md`). El filtro por materia/fecha se resuelve en el
  repositorio (SQL); el filtro por estado se aplica en memoria en el service,
  ya que es una regla de dominio, no una columna.
- Los canales de notificación (HU-12, HU-14) siguen patrón Strategy: agregar
  Telegram (HU-21) a futuro no debería requerir tocar el motor de
  recordatorios, solo un nuevo adaptador.
- **HU-14 (recibir recordatorio por email) — 2 decisiones a aplicar cuando
  se especifique esta historia:**
  - **Reintento sin cola FIFO real**: en vez de una cola dedicada para
    emails pendientes por falta de internet, aprovechar que
    `recordatorio_envios` ya registra cada intento con estado
    "enviado"/"fallido" (ver `docs/modelo-datos.md`). El motor de
    recordatorios, en cada corrida de polling, además de buscar
    recordatorios nuevos reintenta los que quedaron en "fallido". Si
    `smtplib` lanza una excepción de conexión, se marca "fallido" y el
    siguiente ciclo reintenta solo, sin necesidad de detectar conexión a
    internet explícitamente (poco confiable multiplataforma). Evita
    construir infraestructura de cola dedicada (YAGNI).
  - **Agrupar notificaciones queda fuera de HU-14**: un email por
    recordatorio, no un resumen agrupado por materia/día/corrida. Si el
    volumen real resulta molesto, se crea una historia nueva para el
    agrupamiento — no se decide el criterio de antemano sin evidencia de
    que haga falta.
