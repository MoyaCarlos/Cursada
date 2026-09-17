from domain.materia import Materia, NombreDuplicadoError, crear_materia
from repository.materia_repository import MateriaRepository


class CrearMateria:
    def __init__(self, repositorio: MateriaRepository) -> None:
        self._repositorio = repositorio

    def ejecutar(self, nombre: str) -> Materia:
        if self._repositorio.existe_nombre(nombre):
            raise NombreDuplicadoError(
                f"Ya existe una materia llamada '{nombre.strip()}'."
            )
        materia = crear_materia(nombre)
        return self._repositorio.guardar(materia)
