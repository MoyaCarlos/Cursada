from domain.tarea import EstadoTarea, cambiar_estado_tarea
from repository.tarea_repository import TareaRepository


class CambiarEstadoTarea:
    def __init__(self, tarea_repositorio: TareaRepository) -> None:
        self._tareas = tarea_repositorio

    def ejecutar(self, id: int, nuevo_estado: EstadoTarea) -> None:
        tarea_actual = self._tareas.obtener(id)
        tarea_cambiada = cambiar_estado_tarea(tarea_actual, nuevo_estado)
        self._tareas.actualizar(tarea_cambiada)
