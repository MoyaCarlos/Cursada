import tkinter as tk
from tkinter import ttk

from repository.examen_repository import ExamenRepository
from repository.materia_repository import MateriaRepository
from repository.tarea_repository import TareaRepository
from services.listar_pendientes import ListarPendientes
from ui.formato_fecha import formatear_fecha


class PanelPendientes(ttk.Frame):
    def __init__(
        self,
        maestro: tk.Misc,
        tarea_repositorio: TareaRepository,
        examen_repositorio: ExamenRepository,
        materia_repositorio: MateriaRepository,
    ) -> None:
        super().__init__(maestro)
        self._listar_pendientes = ListarPendientes(
            tarea_repositorio, examen_repositorio, materia_repositorio
        )

        self._listado = tk.Listbox(self)
        self._listado.pack(fill="both", expand=True, padx=8, pady=8)

        self.actualizar()

    def actualizar(self) -> None:
        self._listado.delete(0, tk.END)
        for item in self._listar_pendientes.ejecutar():
            etiqueta = "TAREA" if item.tipo == "tarea" else "EXAMEN"
            fecha_texto = formatear_fecha(item.fecha)
            if item.hora is not None:
                fecha_texto += f" {item.hora.strftime('%H:%M')}"
            detalle = f"[{item.estado}] " if item.estado is not None else ""
            self._listado.insert(
                tk.END,
                f"[{etiqueta}] {detalle}{item.titulo} - {item.materia_nombre} ({fecha_texto})",
            )
