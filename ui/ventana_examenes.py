import tkinter as tk
from datetime import time
from tkinter import messagebox, ttk

from domain.examen import ModalidadExamen
from repository.examen_repository import ExamenRepository
from repository.materia_repository import MateriaRepository
from services.crear_examen import CrearExamen
from services.editar_examen import EditarExamen
from services.eliminar_examen import EliminarExamen
from ui.formato_fecha import formatear_fecha, parsear_fecha


class PanelExamenes(ttk.Frame):
    def __init__(
        self,
        maestro: tk.Misc,
        examen_repositorio: ExamenRepository,
        materia_repositorio: MateriaRepository,
    ) -> None:
        super().__init__(maestro)
        self._examenes_repo = examen_repositorio
        self._materias_repo = materia_repositorio
        self._crear_examen = CrearExamen(examen_repositorio, materia_repositorio)
        self._editar_examen = EditarExamen(examen_repositorio, materia_repositorio)
        self._eliminar_examen = EliminarExamen(examen_repositorio)
        self._materias_listadas = []
        self._examenes_listados = []
        self._editando_id: int | None = None

        ttk.Label(self, text="Materia:").pack(anchor="w", padx=8, pady=(8, 0))
        self._combo_materia = ttk.Combobox(self, state="readonly")
        self._combo_materia.pack(fill="x", padx=8)

        ttk.Label(self, text="Tema:").pack(anchor="w", padx=8, pady=(8, 0))
        self._entrada_tema = ttk.Entry(self)
        self._entrada_tema.pack(fill="x", padx=8)

        ttk.Label(self, text="Fecha (DD/MM o DD/MM/AAAA):").pack(
            anchor="w", padx=8, pady=(8, 0)
        )
        self._entrada_fecha = ttk.Entry(self)
        self._entrada_fecha.pack(fill="x", padx=8)

        ttk.Label(self, text="Hora (HH:MM):").pack(anchor="w", padx=8, pady=(8, 0))
        self._entrada_hora = ttk.Entry(self)
        self._entrada_hora.pack(fill="x", padx=8)

        ttk.Label(self, text="Modalidad:").pack(anchor="w", padx=8, pady=(8, 0))
        self._combo_modalidad = ttk.Combobox(
            self, state="readonly", values=[m.value for m in ModalidadExamen]
        )
        self._combo_modalidad.pack(fill="x", padx=8)

        ttk.Label(self, text="Notas (opcional):").pack(anchor="w", padx=8, pady=(8, 0))
        self._entrada_notas = ttk.Entry(self)
        self._entrada_notas.pack(fill="x", padx=8)

        self._boton_guardar = ttk.Button(self, text="Crear examen", command=self._on_guardar)
        self._boton_guardar.pack(pady=8)

        self._listado = tk.Listbox(self)
        self._listado.pack(fill="both", expand=True, padx=8, pady=8)

        ttk.Button(self, text="Editar seleccionado", command=self._on_editar).pack(pady=4)
        ttk.Button(self, text="Eliminar seleccionado", command=self._on_eliminar).pack(pady=4)

        self._refrescar_materias()
        self._refrescar_listado()

    def actualizar(self) -> None:
        self._refrescar_materias()
        self._refrescar_listado()

    def _refrescar_materias(self) -> None:
        self._materias_listadas = self._materias_repo.listar()
        self._combo_materia["values"] = [m.nombre for m in self._materias_listadas]
        if self._materias_listadas and not self._combo_materia.get():
            self._combo_materia.current(0)

    def _limpiar_formulario(self) -> None:
        self._entrada_tema.delete(0, tk.END)
        self._entrada_fecha.delete(0, tk.END)
        self._entrada_hora.delete(0, tk.END)
        self._combo_modalidad.set("")
        self._entrada_notas.delete(0, tk.END)
        self._editando_id = None
        self._boton_guardar.configure(text="Crear examen")

    def _on_guardar(self) -> None:
        if not self._materias_listadas:
            messagebox.showinfo("Guardar examen", "Primero tenés que crear una materia.")
            return
        indice = self._combo_materia.current()
        if indice < 0:
            messagebox.showinfo("Guardar examen", "Elegí una materia.")
            return
        materia_id = self._materias_listadas[indice].id
        try:
            fecha = parsear_fecha(self._entrada_fecha.get())
        except ValueError:
            messagebox.showerror(
                "No se pudo guardar el examen",
                "La fecha debe tener el formato DD/MM o DD/MM/AAAA.",
            )
            return
        hora_texto = self._entrada_hora.get().strip()
        try:
            hora = time.fromisoformat(hora_texto) if hora_texto else None
        except ValueError:
            messagebox.showerror(
                "No se pudo guardar el examen", "La hora debe tener el formato HH:MM."
            )
            return
        modalidad_texto = self._combo_modalidad.get()
        modalidad = ModalidadExamen(modalidad_texto) if modalidad_texto else None
        try:
            if self._editando_id is None:
                self._crear_examen.ejecutar(
                    materia_id=materia_id,
                    tema=self._entrada_tema.get(),
                    fecha=fecha,
                    hora=hora,
                    modalidad=modalidad,
                    notas=self._entrada_notas.get(),
                )
            else:
                self._editar_examen.ejecutar(
                    id=self._editando_id,
                    materia_id=materia_id,
                    tema=self._entrada_tema.get(),
                    fecha=fecha,
                    hora=hora,
                    modalidad=modalidad,
                    notas=self._entrada_notas.get(),
                )
        except ValueError as error:
            messagebox.showerror("No se pudo guardar el examen", str(error))
            return
        self._limpiar_formulario()
        self._refrescar_listado()

    def _on_editar(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Editar examen", "Seleccioná un examen del listado.")
            return
        examen = self._examenes_listados[seleccion[0]]
        nombre_materia = next(
            (m.nombre for m in self._materias_listadas if m.id == examen.materia_id), ""
        )
        self._combo_materia.set(nombre_materia)
        self._entrada_tema.delete(0, tk.END)
        self._entrada_tema.insert(0, examen.tema)
        self._entrada_fecha.delete(0, tk.END)
        self._entrada_fecha.insert(0, formatear_fecha(examen.fecha))
        self._entrada_hora.delete(0, tk.END)
        self._entrada_hora.insert(0, examen.hora.strftime("%H:%M"))
        self._combo_modalidad.set(examen.modalidad.value)
        self._entrada_notas.delete(0, tk.END)
        self._entrada_notas.insert(0, examen.notas)
        self._editando_id = examen.id
        self._boton_guardar.configure(text="Guardar cambios")

    def _on_eliminar(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Eliminar examen", "Seleccioná un examen del listado.")
            return
        examen = self._examenes_listados[seleccion[0]]
        if not messagebox.askyesno(
            "Eliminar examen", f"¿Eliminar el examen '{examen.tema}'?"
        ):
            return
        self._eliminar_examen.ejecutar(examen.id)
        if self._editando_id == examen.id:
            self._limpiar_formulario()
        self._refrescar_listado()

    def _refrescar_listado(self) -> None:
        self._listado.delete(0, tk.END)
        materias_por_id = {m.id: m.nombre for m in self._materias_repo.listar()}
        self._examenes_listados = self._examenes_repo.listar()
        for examen in self._examenes_listados:
            materia_nombre = materias_por_id.get(examen.materia_id, "?")
            self._listado.insert(
                tk.END,
                f"{examen.tema} - {materia_nombre} "
                f"({formatear_fecha(examen.fecha)} {examen.hora.strftime('%H:%M')}, "
                f"{examen.modalidad.value})",
            )
