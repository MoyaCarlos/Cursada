import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from domain.tarea import EstadoTarea, PrioridadTarea
from repository.materia_repository import MateriaRepository
from repository.tarea_repository import TareaRepository
from services.cambiar_estado_tarea import CambiarEstadoTarea
from services.crear_tarea import CrearTarea
from services.editar_tarea import EditarTarea
from services.eliminar_tarea import EliminarTarea


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
        self._editar_tarea = EditarTarea(tarea_repositorio, materia_repositorio)
        self._eliminar_tarea = EliminarTarea(tarea_repositorio)
        self._cambiar_estado_tarea = CambiarEstadoTarea(tarea_repositorio)
        self._materias_listadas = []
        self._tareas_listadas = []
        self._editando_id: int | None = None

        self.title("Tareas")
        self.geometry("420x480")

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

        self._boton_guardar = ttk.Button(self, text="Crear tarea", command=self._on_guardar)
        self._boton_guardar.pack(pady=8)

        self._listado = tk.Listbox(self)
        self._listado.pack(fill="both", expand=True, padx=8, pady=8)

        ttk.Button(self, text="Editar seleccionada", command=self._on_editar).pack(pady=4)
        ttk.Button(self, text="Eliminar seleccionada", command=self._on_eliminar).pack(pady=4)

        estado_frame = ttk.Frame(self)
        estado_frame.pack(pady=4)
        self._combo_estado = ttk.Combobox(
            estado_frame, state="readonly", values=[e.value for e in EstadoTarea]
        )
        self._combo_estado.set(EstadoTarea.PENDIENTE.value)
        self._combo_estado.pack(side="left", padx=(0, 4))
        ttk.Button(
            estado_frame, text="Cambiar estado", command=self._on_cambiar_estado
        ).pack(side="left")

        self._refrescar_materias()
        self._refrescar_listado()

    def _refrescar_materias(self) -> None:
        self._materias_listadas = self._materias_repo.listar()
        self._combo_materia["values"] = [m.nombre for m in self._materias_listadas]
        if self._materias_listadas and not self._combo_materia.get():
            self._combo_materia.current(0)

    def _limpiar_formulario(self) -> None:
        self._entrada_titulo.delete(0, tk.END)
        self._entrada_descripcion.delete(0, tk.END)
        self._entrada_fecha.delete(0, tk.END)
        self._combo_prioridad.set(PrioridadTarea.MEDIA.value)
        self._editando_id = None
        self._boton_guardar.configure(text="Crear tarea")

    def _on_guardar(self) -> None:
        if not self._materias_listadas:
            messagebox.showinfo("Guardar tarea", "Primero tenés que crear una materia.")
            return
        indice = self._combo_materia.current()
        if indice < 0:
            messagebox.showinfo("Guardar tarea", "Elegí una materia.")
            return
        materia_id = self._materias_listadas[indice].id
        try:
            fecha_limite = date.fromisoformat(self._entrada_fecha.get().strip())
        except ValueError:
            messagebox.showerror(
                "No se pudo guardar la tarea",
                "La fecha límite debe tener el formato AAAA-MM-DD.",
            )
            return
        try:
            if self._editando_id is None:
                self._crear_tarea.ejecutar(
                    materia_id=materia_id,
                    titulo=self._entrada_titulo.get(),
                    fecha_limite=fecha_limite,
                    descripcion=self._entrada_descripcion.get(),
                    prioridad=PrioridadTarea(self._combo_prioridad.get()),
                )
            else:
                self._editar_tarea.ejecutar(
                    id=self._editando_id,
                    materia_id=materia_id,
                    titulo=self._entrada_titulo.get(),
                    fecha_limite=fecha_limite,
                    descripcion=self._entrada_descripcion.get(),
                    prioridad=PrioridadTarea(self._combo_prioridad.get()),
                )
        except ValueError as error:
            messagebox.showerror("No se pudo guardar la tarea", str(error))
            return
        self._limpiar_formulario()
        self._refrescar_listado()

    def _on_editar(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Editar tarea", "Seleccioná una tarea del listado.")
            return
        tarea = self._tareas_listadas[seleccion[0]]
        nombre_materia = next(
            (m.nombre for m in self._materias_listadas if m.id == tarea.materia_id), ""
        )
        self._combo_materia.set(nombre_materia)
        self._entrada_titulo.delete(0, tk.END)
        self._entrada_titulo.insert(0, tarea.titulo)
        self._entrada_descripcion.delete(0, tk.END)
        self._entrada_descripcion.insert(0, tarea.descripcion)
        self._entrada_fecha.delete(0, tk.END)
        self._entrada_fecha.insert(0, tarea.fecha_limite.isoformat())
        self._combo_prioridad.set(tarea.prioridad.value)
        self._editando_id = tarea.id
        self._boton_guardar.configure(text="Guardar cambios")

    def _on_eliminar(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Eliminar tarea", "Seleccioná una tarea del listado.")
            return
        tarea = self._tareas_listadas[seleccion[0]]
        if not messagebox.askyesno("Eliminar tarea", f"¿Eliminar la tarea '{tarea.titulo}'?"):
            return
        self._eliminar_tarea.ejecutar(tarea.id)
        if self._editando_id == tarea.id:
            self._limpiar_formulario()
        self._refrescar_listado()

    def _on_cambiar_estado(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Cambiar estado", "Seleccioná una tarea del listado.")
            return
        tarea = self._tareas_listadas[seleccion[0]]
        self._cambiar_estado_tarea.ejecutar(
            id=tarea.id, nuevo_estado=EstadoTarea(self._combo_estado.get())
        )
        self._refrescar_listado()

    def _refrescar_listado(self) -> None:
        self._listado.delete(0, tk.END)
        materias_por_id = {m.id: m.nombre for m in self._materias_repo.listar()}
        self._tareas_listadas = self._tareas_repo.listar()
        for tarea in self._tareas_listadas:
            materia_nombre = materias_por_id.get(tarea.materia_id, "?")
            self._listado.insert(
                tk.END,
                f"[{tarea.estado.value}] {tarea.titulo} - {materia_nombre} "
                f"({tarea.fecha_limite})",
            )
