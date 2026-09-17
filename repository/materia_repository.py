from typing import Protocol

from domain.materia import Materia


class MateriaRepository(Protocol):
    def guardar(self, materia: Materia) -> Materia:
        """Inserta o actualiza una materia. Devuelve la materia con id asignado."""

    def existe_nombre(self, nombre: str, excluir_id: int | None = None) -> bool:
        """True si ya existe una materia con ese nombre (case-insensitive).
        `excluir_id` se usa al editar, para no comparar la materia consigo misma."""

    def listar(self) -> list[Materia]:
        """Todas las materias existentes."""

    def obtener(self, id: int) -> Materia | None:
        """Una materia por id, o None si no existe."""

    def eliminar(self, id: int) -> None:
        """Elimina la materia. El llamador ya validó que no tiene eventos asociados."""

    def tiene_eventos_asociados(self, materia_id: int) -> bool:
        """True si existe al menos una fila en `eventos` con ese materia_id."""
