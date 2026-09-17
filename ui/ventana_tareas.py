import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from domain.tarea import PrioridadTarea
from repository.materia_repository import MateriaRepository
from repository.tarea_repository import TareaRepository
from services.crear_tarea import CrearTarea


class VentanaTareas(tk.Toplevel):
    def __init__(
        self,
        maestro: tk.Misc,
        tarea_repositorio: TareaRepository,
        materia_repositorio: MateriaRepository,
    ) -> None:
        super().__init__(maestro)
        self._tareas_repo = tarea_repositorio
        self._materias_repo = materia_repositorio
        self._crear_tarea = CrearTarea(tarea_repositorio, materia_repositorio)
        self._materias_listadas = []

        self.title("Tareas")
        self.geometry("420x420")

        ttk.Label(self, text="Materia:").pack(anchor="w", padx=8, pady=(8, 0))
        self._combo_materia = ttk.Combobox(self, state="readonly")
        self._combo_materia.pack(fill="x", padx=8)

        ttk.Label(self, text="Título:").pack(anchor="w", padx=8, pady=(8, 0))
        self._entrada_titulo = ttk.Entry(self)
        self._entrada_titulo.pack(fill="x", padx=8)

        ttk.Label(self, text="Descripción (opcional):").pack(anchor="w", padx=8, pady=(8, 0))
        self._entrada_descripcion = ttk.Entry(self)
        self._entrada_descripcion.pack(fill="x", padx=8)

        ttk.Label(self, text="Fecha límite (AAAA-MM-DD):").pack(anchor="w", padx=8, pady=(8, 0))
        self._entrada_fecha = ttk.Entry(self)
        self._entrada_fecha.pack(fill="x", padx=8)

        ttk.Label(self, text="Prioridad:").pack(anchor="w", padx=8, pady=(8, 0))
        self._combo_prioridad = ttk.Combobox(
            self, state="readonly", values=[p.value for p in PrioridadTarea]
        )
        self._combo_prioridad.set(PrioridadTarea.MEDIA.value)
        self._combo_prioridad.pack(fill="x", padx=8)

        ttk.Button(self, text="Crear tarea", command=self._on_crear).pack(pady=8)

        self._listado = tk.Listbox(self)
        self._listado.pack(fill="both", expand=True, padx=8, pady=8)

        self._refrescar_materias()
        self._refrescar_listado()

    def _refrescar_materias(self) -> None:
        self._materias_listadas = self._materias_repo.listar()
        self._combo_materia["values"] = [m.nombre for m in self._materias_listadas]
        if self._materias_listadas and not self._combo_materia.get():
            self._combo_materia.current(0)

    def _on_crear(self) -> None:
        if not self._materias_listadas:
            messagebox.showinfo("Crear tarea", "Primero tenés que crear una materia.")
            return
        indice = self._combo_materia.current()
        if indice < 0:
            messagebox.showinfo("Crear tarea", "Elegí una materia.")
            return
        materia_id = self._materias_listadas[indice].id
        try:
            fecha_limite = date.fromisoformat(self._entrada_fecha.get().strip())
        except ValueError:
            messagebox.showerror(
                "No se pudo crear la tarea",
                "La fecha límite debe tener el formato AAAA-MM-DD.",
            )
            return
        try:
            self._crear_tarea.ejecutar(
                materia_id=materia_id,
                titulo=self._entrada_titulo.get(),
                fecha_limite=fecha_limite,
                descripcion=self._entrada_descripcion.get(),
                prioridad=PrioridadTarea(self._combo_prioridad.get()),
            )
        except ValueError as error:
            messagebox.showerror("No se pudo crear la tarea", str(error))
            return
        self._entrada_titulo.delete(0, tk.END)
        self._entrada_descripcion.delete(0, tk.END)
        self._entrada_fecha.delete(0, tk.END)
        self._refrescar_listado()

    def _refrescar_listado(self) -> None:
        self._listado.delete(0, tk.END)
        for tarea in self._tareas_repo.listar():
            self._listado.insert(
                tk.END, f"[{tarea.estado.value}] {tarea.titulo} ({tarea.fecha_limite})"
            )
