from repository.tarea_repository import TareaRepository


class EliminarTarea:
    def __init__(self, tarea_repositorio: TareaRepository) -> None:
        self._tareas = tarea_repositorio

    def ejecutar(self, id: int) -> None:
        self._tareas.eliminar(id)
