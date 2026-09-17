from repository.examen_repository import ExamenRepository


class EliminarExamen:
    def __init__(self, examen_repositorio: ExamenRepository) -> None:
        self._examenes = examen_repositorio

    def ejecutar(self, id: int) -> None:
        self._examenes.eliminar(id)
