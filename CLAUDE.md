# Proyecto: Asistente de Tareas y Exámenes (Facultad)

## Objetivo
Aplicación de escritorio para Linux y Windows que permite llevar registro de tareas
pendientes y fechas de examen de la facultad, con recordatorios configurables
(notificación de escritorio y email; Telegram queda pendiente para más adelante).

Proyecto individual (no de cátedra), pero desarrollado con la misma disciplina de
proceso (SDD + BDD + TDD) usada en `seguimiento-medicion`, adaptada a un contexto
sin equipo.

## Alcance del MVP
- Gestión de materias (crear/editar/eliminar).
- Gestión de tareas (materia, título, descripción, fecha límite, estado, prioridad).
- Gestión de exámenes (materia, tema, fecha, hora, modalidad, notas).
- Recordatorios configurables por anticipación (ej: 3 días antes, 2 horas antes).
- Motor de recordatorios en background (polling periódico, no tiempo real).
- Notificaciones por escritorio (nativas) y por email (SMTP configurable).
- Selección de canales de notificación activos desde una pantalla de configuración.
- Vista unificada de "próximos pendientes" (tareas + exámenes) con filtros por
  estado (pendiente/completado), materia y rango de fechas.
- Ícono en la bandeja del sistema.
- Empaquetado standalone para Linux y Windows (PyInstaller), con autoarranque.

## Fuera de alcance del MVP
- Sincronización de datos entre dispositivos (cada máquina tiene su propia base
  de datos local).
- Multi-usuario / compartir con compañeros.
- Integración con sistemas propios de la facultad.
- **Notificaciones por Telegram**: pendiente, se evalúa sumar al final si se ve
  necesario. El diseño (Strategy de notificadores) ya lo deja contemplado sin
  requerir cambios de arquitectura.

## Metodología de desarrollo
Proyecto individual: sin roles de equipo, sin tablero Scrum obligatorio, sin
aprobación de otro integrante en PR (el "review" antes de mergear lo hace el
mismo autor sobre el diff). Se mantiene el resto del proceso de
`seguimiento-medicion` por su valor propio, independiente de tener equipo.

### SDD (Specification-Driven Development)
- Herramienta: **GitHub Spec Kit**, `specify init --here --integration claude`.
- Flujo por historia: `/speckit.constitution` (una vez) → `/speckit.specify` →
  `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`.
- Specs versionadas en `specs/<feature>/`. Reglas de negocio, casos límite y
  errores en formato **EARS** (Ubicuo / Basado en evento / Basado en estado /
  No deseado / Opcional).
- `/speckit.implement` una historia a la vez, con revisión del diff antes de
  seguir con la próxima.

### BDD (Behavior-Driven Development)
- **pytest-bdd** (no Godog, que es específico de Go) — Gherkin integrado al
  mismo runner que las pruebas unitarias, sin duplicar herramientas de testing.
- Archivos `.feature` en `/features`, con casos normales, alternativos, límite
  y de error.

### TDD (Test-Driven Development)
- **pytest**, foco en `domain/` (reglas de negocio, cálculo de recordatorios,
  regla de "completado") y `services/` (casos de uso).
- Ciclo **RED → GREEN → REFACTOR**, evidenciado en el historial de commits:
  ```
  RED: agregar test de <caso> (falla)
  GREEN: implementar <caso>, test en verde
  REFACTOR: <qué se limpió>
  ```
- No se fuerza un commit de REFACTOR vacío si no hay nada que limpiar. No
  aplica a código trivial (getters, DTOs).

### Convención de Git
- Rama por historia: `feature/HU-XX-nombre-corto`.
- Merge a `main` siempre con **"Create a merge commit"** (nunca squash), para
  conservar en el historial la evidencia del ciclo RED/GREEN/REFACTOR.

### Definition of Done
Una historia se considera terminada cuando:
- Código implementado y mergeado a `main`.
- Test unitario (TDD) y escenario BDD correspondiente, ambos en verde.
- Especificación SDD de la historia escrita en `specs/`.
- Sin defectos abiertos bloqueantes para esa historia.

## Principios de diseño
- **Clean Code:** nombres claros, funciones pequeñas, sin comentarios que
  expliquen el "qué".
- **SOLID:** SRP (un service por caso de uso) y Dependency Inversion (los
  services dependen de interfaces de repositorio, no de `sqlite3` directo).
- **KISS:** el motor de recordatorios hace polling cada N minutos en vez de
  un mecanismo en tiempo real; el filtro por estado se resuelve en memoria
  (Python) en vez de en SQL, dado el volumen chico de datos de una app personal.
- **YAGNI:** sin sync entre dispositivos, sin Telegram todavía, sin estado
  explícito de "rendido" en exámenes (se infiere por fecha).
- **DRY:** la regla de "cuándo corresponde disparar un recordatorio" y la
  regla de "qué cuenta como completado" viven una sola vez en `domain/`, sin
  duplicarse entre repositorio, servicios y UI.

## Arquitectura
Clean/Hexagonal liviana (Ports & Adapters), igual criterio que en
`seguimiento-medicion`:

```
asistente_facultad/
  domain/          -> entidades (Materia, Tarea, Examen, Evento, Recordatorio)
                      y reglas de negocio (cálculo de disparo de recordatorio,
                      regla de "completado" por tipo de evento)
  services/        -> casos de uso (CrearTarea, CrearExamen, ProgramarRecordatorios,
                      RevisarPendientesYNotificar, ListarEventos con FiltroEventos)
  repository/      -> interfaces (Protocol) + implementación SQLite
  notifications/   -> adaptadores por canal (NotificadorEmail, NotificadorEscritorio)
  ui/              -> Tkinter (ventana principal) + pystray (bandeja)
  tests/           -> unitarios (pytest)
  features/        -> escenarios BDD (pytest-bdd)
  specs/           -> especificaciones SDD versionadas (generadas con Spec Kit)
  main.py          -> wiring de dependencias, arranque de la app
```

La dependencia siempre apunta hacia adentro: `domain` no conoce SQLite, Tkinter
ni cómo se envía un email.

## Patrones de diseño aplicados
- **Repository:** interfaces (`MateriaRepository`, `EventoRepository`, etc.)
  que abstraen la persistencia, permiten testear casos de uso con fakes en
  memoria sin tocar disco.
- **Strategy:** cada canal de notificación implementa una interfaz común
  `Notificador.enviar(mensaje)` (email, escritorio, y Telegram cuando se
  sume). El motor de recordatorios itera los canales activos sin conocer el
  detalle de cada uno.
- **Factory function:** constructores (`crear_tarea(...)`, `crear_examen(...)`)
  que validan invariantes al crear la entidad (ej: fecha no puede ser pasada,
  la materia debe existir).

## Modelo de datos
Ver [`docs/modelo-datos.md`](docs/modelo-datos.md) — esquema normalizado a 3FN.

## Backlog
Ver [`docs/backlog.md`](docs/backlog.md) — épicas, historias de usuario y
mapeo a fases de desarrollo.

## Stack tecnológico
- **Lenguaje:** Python.
- **UI:** Tkinter (incluido en la stdlib) + `pystray` (ícono de bandeja).
- **Persistencia:** SQLite vía `sqlite3` (stdlib).
- **Notificaciones:** `smtplib` (email), `plyer`/`win10toast`/`notify-send`
  según SO (escritorio).
- **Testing BDD:** `pytest-bdd`.
- **Testing TDD:** `pytest`.
- **Empaquetado:** PyInstaller (ejecutables standalone Linux/Windows).
- **Control de versiones:** Git.

## Roadmap por fases
1. CRUD de materias/tareas/exámenes + SQLite + ventana Tkinter (sin notificaciones).
2. Motor de recordatorios + notificación de escritorio.
3. Notificación por email (SMTP) + selección de canales activos.
4. Ícono de bandeja + empaquetado (PyInstaller, Linux y Windows) + autoarranque.
5. (Futuro, si se ve necesario) Notificaciones por Telegram.
