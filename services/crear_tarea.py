from datetime import date

from domain.materia import Materia, MateriaInexistenteError
from domain.tarea import PrioridadTarea, Tarea, crear_tarea
from repository.materia_repository import MateriaRepository
from repository.tarea_repository import TareaRepository


class CrearTarea:
    def __init__(
        self, tarea_repositorio: TareaRepository, materia_repositorio: MateriaRepository
    ) -> None:
        self._tareas = tarea_repositorio
        self._materias = materia_repositorio

    def ejecutar(
        self,
        materia_id: int,
        titulo: str,
        fecha_limite: date,
        descripcion: str = "",
        prioridad: PrioridadTarea = PrioridadTarea.MEDIA,
    ) -> Tarea:
        materia: Materia | None = self._materias.obtener(materia_id)
        if materia is None:
            raise MateriaInexistenteError(
                f"No existe ninguna materia con id {materia_id}."
            )
        tarea = crear_tarea(
            materia_id=materia_id,
            titulo=titulo,
            fecha_limite=fecha_limite,
            descripcion=descripcion,
            prioridad=prioridad,
        )
        return self._tareas.guardar(tarea)
