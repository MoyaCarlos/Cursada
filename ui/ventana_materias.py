import tkinter as tk
from tkinter import messagebox, ttk

from domain.materia import NombreDuplicadoError
from repository.materia_repository import MateriaRepository
from services.crear_materia import CrearMateria


class VentanaMaterias(tk.Tk):
    def __init__(self, repositorio: MateriaRepository) -> None:
        super().__init__()
        self._repositorio = repositorio
        self._crear_materia = CrearMateria(repositorio)

        self.title("Materias")
        self.geometry("400x300")

        self._entrada_nombre = ttk.Entry(self)
        self._entrada_nombre.pack(fill="x", padx=8, pady=8)

        ttk.Button(self, text="Crear materia", command=self._on_crear).pack(pady=4)

        self._listado = tk.Listbox(self)
        self._listado.pack(fill="both", expand=True, padx=8, pady=8)

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

    def _refrescar_listado(self) -> None:
        self._listado.delete(0, tk.END)
        for materia in self._repositorio.listar():
            self._listado.insert(tk.END, materia.nombre)
