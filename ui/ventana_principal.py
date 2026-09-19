import tkinter as tk
from tkinter import ttk

from repository.examen_repository import ExamenRepository
from repository.materia_repository import MateriaRepository
from repository.tarea_repository import TareaRepository
from ui.panel_pendientes import PanelPendientes
from ui.ventana_examenes import PanelExamenes
from ui.ventana_materias import PanelMaterias
from ui.ventana_tareas import PanelTareas


class VentanaPrincipal(tk.Tk):
    def __init__(
        self,
        materia_repositorio: MateriaRepository,
        tarea_repositorio: TareaRepository,
        examen_repositorio: ExamenRepository,
    ) -> None:
        super().__init__()
        self.title("Cursada")
        self.geometry("480x560")

        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill="both", expand=True)

        self._panel_pendientes = PanelPendientes(
            self._notebook, tarea_repositorio, examen_repositorio, materia_repositorio
        )
        self._panel_materias = PanelMaterias(self._notebook, materia_repositorio)
        self._panel_tareas = PanelTareas(
            self._notebook, tarea_repositorio, materia_repositorio
        )
        self._panel_examenes = PanelExamenes(
            self._notebook, examen_repositorio, materia_repositorio
        )

        self._notebook.add(self._panel_pendientes, text="Pendientes")
        self._notebook.add(self._panel_materias, text="Materias")
        self._notebook.add(self._panel_tareas, text="Tareas")
        self._notebook.add(self._panel_examenes, text="Exámenes")

        self._notebook.bind("<<NotebookTabChanged>>", self._on_cambiar_pestana)

    def _on_cambiar_pestana(self, _evento: tk.Event) -> None:
        panel = self._notebook.nametowidget(self._notebook.select())
        panel.actualizar()
