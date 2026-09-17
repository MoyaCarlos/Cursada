from typing import Protocol

from domain.tarea import Tarea


class TareaRepository(Protocol):
    def guardar(self, tarea: Tarea) -> Tarea:
        """Inserta la tarea (evento + tarea). Devuelve la tarea con id asignado."""

    def listar(self) -> list[Tarea]:
        """Todas las tareas existentes."""

    def obtener(self, id: int) -> Tarea | None:
        """Una tarea por id, o None si no existe."""

    def actualizar(self, tarea: Tarea) -> Tarea:
        """Actualiza una tarea existente (tarea.id no es None)."""

    def eliminar(self, id: int) -> None:
        """Elimina la tarea y su evento asociado."""
