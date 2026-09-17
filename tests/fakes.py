from domain.examen import Examen
from domain.materia import Materia
from domain.tarea import Tarea


class MateriaRepositoryFake:
    def __init__(self) -> None:
        self._materias: dict[int, Materia] = {}
        self._siguiente_id = 1
        self._materias_con_eventos: set[int] = set()

    def guardar(self, materia: Materia) -> Materia:
        if materia.id is None:
            materia = Materia(id=self._siguiente_id, nombre=materia.nombre)
            self._siguiente_id += 1
        self._materias[materia.id] = materia
        return materia

    def existe_nombre(self, nombre: str, excluir_id: int | None = None) -> bool:
        normalizado = nombre.strip().lower()
        return any(
            materia.nombre.strip().lower() == normalizado
            for materia in self._materias.values()
            if materia.id != excluir_id
        )

    def listar(self) -> list[Materia]:
        return list(self._materias.values())

    def obtener(self, id: int) -> Materia | None:
        return self._materias.get(id)

    def eliminar(self, id: int) -> None:
        del self._materias[id]

    def tiene_eventos_asociados(self, materia_id: int) -> bool:
        return materia_id in self._materias_con_eventos

    def marcar_con_eventos(self, materia_id: int) -> None:
        """Helper de test: simula que la materia tiene tareas/exámenes asociados."""
        self._materias_con_eventos.add(materia_id)


class TareaRepositoryFake:
    def __init__(self) -> None:
        self._tareas: dict[int, Tarea] = {}
        self._siguiente_id = 1

    def guardar(self, tarea: Tarea) -> Tarea:
        tarea = Tarea(
            id=self._siguiente_id,
            materia_id=tarea.materia_id,
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            fecha_limite=tarea.fecha_limite,
            prioridad=tarea.prioridad,
            estado=tarea.estado,
        )
        self._tareas[tarea.id] = tarea
        self._siguiente_id += 1
        return tarea

    def listar(self) -> list[Tarea]:
        return list(self._tareas.values())

    def obtener(self, id: int) -> Tarea | None:
        return self._tareas.get(id)

    def actualizar(self, tarea: Tarea) -> Tarea:
        self._tareas[tarea.id] = tarea
        return tarea

    def eliminar(self, id: int) -> None:
        del self._tareas[id]


class ExamenRepositoryFake:
    def __init__(self) -> None:
        self._examenes: dict[int, Examen] = {}
        self._siguiente_id = 1

    def guardar(self, examen: Examen) -> Examen:
        examen = Examen(
            id=self._siguiente_id,
            materia_id=examen.materia_id,
            tema=examen.tema,
            fecha=examen.fecha,
            hora=examen.hora,
            modalidad=examen.modalidad,
            notas=examen.notas,
        )
        self._examenes[examen.id] = examen
        self._siguiente_id += 1
        return examen

    def listar(self) -> list[Examen]:
        return list(self._examenes.values())
