from typing import Protocol

from domain.tarea import Tarea


class TareaRepository(Protocol):
    def guardar(self, tarea: Tarea) -> Tarea:
        """Inserta la tarea (evento + tarea). Devuelve la tarea con id asignado."""

    def listar(self) -> list[Tarea]:
        """Todas las tareas existentes."""
