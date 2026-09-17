from domain.materia import Materia


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
