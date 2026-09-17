# language: es
Característica: Cambiar estado de una tarea

  Escenario: Marcar una tarea como en progreso
    Dado que existe una tarea "TP1" con estado "pendiente"
    Cuando el usuario cambia el estado de "TP1" a "en_progreso"
    Entonces la tarea "TP1" tiene estado "en_progreso"

  Escenario: Marcar una tarea como completada
    Dado que existe una tarea "TP1" con estado "en_progreso"
    Cuando el usuario cambia el estado de "TP1" a "completada"
    Entonces la tarea "TP1" tiene estado "completada"

  Escenario: Volver una tarea completada a pendiente
    Dado que existe una tarea "TP1" con estado "completada"
    Cuando el usuario cambia el estado de "TP1" a "pendiente"
    Entonces la tarea "TP1" tiene estado "pendiente"
