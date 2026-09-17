import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from domain.materia import EventosAsociadosError, NombreDuplicadoError
from repository.materia_repository import MateriaRepository
from services.crear_materia import CrearMateria
from services.editar_materia import EditarMateria
from services.eliminar_materia import EliminarMateria


class VentanaMaterias(tk.Tk):
    def __init__(self, repositorio: MateriaRepository) -> None:
        super().__init__()
        self._repositorio = repositorio
        self._crear_materia = CrearMateria(repositorio)
        self._editar_materia = EditarMateria(repositorio)
        self._eliminar_materia = EliminarMateria(repositorio)
        self._materias_listadas = []

        self.title("Materias")
        self.geometry("400x300")

        self._entrada_nombre = ttk.Entry(self)
        self._entrada_nombre.pack(fill="x", padx=8, pady=8)

        ttk.Button(self, text="Crear materia", command=self._on_crear).pack(pady=4)

        self._listado = tk.Listbox(self)
        self._listado.pack(fill="both", expand=True, padx=8, pady=8)

        ttk.Button(self, text="Editar seleccionada", command=self._on_editar).pack(pady=4)
        ttk.Button(self, text="Eliminar seleccionada", command=self._on_eliminar).pack(pady=4)

        self._refrescar_listado()

    def _on_crear(self) -> None:
        nombre = self._entrada_nombre.get()
        try:
            self._crear_materia.ejecutar(nombre)
        except (ValueError, NombreDuplicadoError) as error:
            messagebox.showerror("No se pudo crear la materia", str(error))
            return
        self._entrada_nombre.delete(0, tk.END)
        self._refrescar_listado()

    def _on_editar(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Editar materia", "Seleccioná una materia del listado.")
            return
        materia = self._materias_listadas[seleccion[0]]
        nuevo_nombre = simpledialog.askstring(
            "Editar materia", "Nuevo nombre:", initialvalue=materia.nombre, parent=self
        )
        if nuevo_nombre is None:
            return
        try:
            self._editar_materia.ejecutar(materia.id, nuevo_nombre)
        except (ValueError, NombreDuplicadoError) as error:
            messagebox.showerror("No se pudo editar la materia", str(error))
            return
        self._refrescar_listado()

    def _on_eliminar(self) -> None:
        seleccion = self._listado.curselection()
        if not seleccion:
            messagebox.showinfo("Eliminar materia", "Seleccioná una materia del listado.")
            return
        materia = self._materias_listadas[seleccion[0]]
        if not messagebox.askyesno(
            "Eliminar materia", f"¿Eliminar la materia '{materia.nombre}'?"
        ):
            return
        try:
            self._eliminar_materia.ejecutar(materia.id)
        except EventosAsociadosError as error:
            messagebox.showerror("No se pudo eliminar la materia", str(error))
            return
        self._refrescar_listado()

    def _refrescar_listado(self) -> None:
        self._materias_listadas = self._repositorio.listar()
        self._listado.delete(0, tk.END)
        for materia in self._materias_listadas:
            self._listado.insert(tk.END, materia.nombre)
