from datetime import date

from domain.tarea import EstadoTarea, Tarea
from services.cambiar_estado_tarea import CambiarEstadoTarea
from tests.fakes import TareaRepositoryFake


def test_cambiar_estado_tarea_persiste_el_nuevo_estado():
    tareas = TareaRepositoryFake()
    tarea = tareas.guardar(
        Tarea(materia_id=1, titulo="TP1", fecha_limite=date(2026, 12, 31))
    )
    servicio = CambiarEstadoTarea(tareas)

    servicio.ejecutar(id=tarea.id, nuevo_estado=EstadoTarea.EN_PROGRESO)

    assert tareas.obtener(tarea.id).estado == EstadoTarea.EN_PROGRESO
