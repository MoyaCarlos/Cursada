from domain.materia import EventosAsociadosError
from repository.materia_repository import MateriaRepository


class EliminarMateria:
    def __init__(self, repositorio: MateriaRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, id: int) -> None:
        if self._repositorio.tiene_eventos_asociados(id):
            raise EventosAsociadosError(
                "No se puede eliminar: la materia tiene tareas o exámenes asociados."
            )
        self._repositorio.eliminar(id)
