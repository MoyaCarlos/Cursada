from dataclasses import dataclass
from datetime import date, time

from repository.examen_repository import ExamenRepository
from repository.materia_repository import MateriaRepository
from repository.tarea_repository import TareaRepository


@dataclass
class ItemPendiente:
    tipo: str
    id: int
    materia_nombre: str
    titulo: str
    fecha: date
    hora: time | None
    estado: str | None


class ListarPendientes:
    def __init__(
        self,
        tarea_repositorio: TareaRepository,
        examen_repositorio: ExamenRepository,
        materia_repositorio: MateriaRepository,
    ) -> None:
        self._tareas = tarea_repositorio
        self._examenes = examen_repositorio
        self._materias = materia_repositorio

    def ejecutar(self) -> list[ItemPendiente]:
        materias_por_id = {m.id: m.nombre for m in self._materias.listar()}
        items = [
            ItemPendiente(
                tipo="tarea",
                id=tarea.id,
                materia_nombre=materias_por_id.get(tarea.materia_id, "?"),
                titulo=tarea.titulo,
                fecha=tarea.fecha_limite,
                hora=None,
                estado=tarea.estado.value,
            )
            for tarea in self._tareas.listar()
        ]
        items += [
            ItemPendiente(
                tipo="examen",
                id=examen.id,
                materia_nombre=materias_por_id.get(examen.materia_id, "?"),
                titulo=examen.tema,
                fecha=examen.fecha,
                hora=examen.hora,
                estado=None,
            )
            for examen in self._examenes.listar()
        ]
        items.sort(key=lambda item: (item.fecha, item.hora or time.min))
        return items
