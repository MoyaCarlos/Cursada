# language: es
Característica: Crear tarea pendiente

  Escenario: Crear una tarea con datos válidos
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario crea una tarea "TP1" para "Bases de Datos" con fecha límite "2026-12-31"
    Entonces la tarea "TP1" aparece en el listado de tareas con estado "pendiente"

  Escenario: Rechazar una tarea sin título
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario intenta crear una tarea sin título para "Bases de Datos" con fecha límite "2026-12-31"
    Entonces el sistema rechaza la creación de la tarea por título obligatorio

  Escenario: Rechazar una tarea con fecha límite pasada
    Dado que existe una materia llamada "Bases de Datos"
    Cuando el usuario intenta crear una tarea "TP1" para "Bases de Datos" con fecha límite "2020-01-01"
    Entonces el sistema rechaza la creación de la tarea por fecha pasada

  Escenario: Rechazar la creación sin ninguna materia cargada
    Cuando el usuario intenta crear una tarea "TP1" para una materia inexistente con fecha límite "2026-12-31"
    Entonces el sistema rechaza la creación de la tarea por materia inexistente
