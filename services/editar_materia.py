from domain.materia import Materia, NombreDuplicadoError, crear_materia
from repository.materia_repository import MateriaRepository


class EditarMateria:
    def __init__(self, repositorio: MateriaRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, id: int, nuevo_nombre: str) -> Materia:
        if self._repositorio.existe_nombre(nuevo_nombre, excluir_id=id):
            raise NombreDuplicadoError(
                f"Ya existe otra materia llamada '{nuevo_nombre.strip()}'."
            )
        materia = crear_materia(nuevo_nombre)
        materia.id = id
        return self._repositorio.guardar(materia)
