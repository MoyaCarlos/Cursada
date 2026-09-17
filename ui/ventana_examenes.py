import tkinter as tk
from datetime import time
from tkinter import messagebox, ttk

from domain.examen import ModalidadExamen
from repository.examen_repository import ExamenRepository
from repository.materia_repository import MateriaRepository
from services.crear_examen import CrearExamen
from ui.formato_fecha import formatear_fecha, parsear_fecha


class VentanaExamenes(tk.Toplevel):
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
        self._materias_listadas = []

        self.title("Exámenes")
        self.geometry("420x480")

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

        ttk.Button(self, text="Crear examen", command=self._on_crear).pack(pady=8)

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
            messagebox.showinfo("Crear examen", "Primero tenés que crear una materia.")
            return
        indice = self._combo_materia.current()
        if indice < 0:
            messagebox.showinfo("Crear examen", "Elegí una materia.")
            return
        materia_id = self._materias_listadas[indice].id
        try:
            fecha = parsear_fecha(self._entrada_fecha.get())
        except ValueError:
            messagebox.showerror(
                "No se pudo crear el examen",
                "La fecha debe tener el formato DD/MM o DD/MM/AAAA.",
            )
            return
        hora_texto = self._entrada_hora.get().strip()
        try:
            hora = time.fromisoformat(hora_texto) if hora_texto else None
        except ValueError:
            messagebox.showerror(
                "No se pudo crear el examen", "La hora debe tener el formato HH:MM."
            )
            return
        modalidad_texto = self._combo_modalidad.get()
        modalidad = ModalidadExamen(modalidad_texto) if modalidad_texto else None
        try:
            self._crear_examen.ejecutar(
                materia_id=materia_id,
                tema=self._entrada_tema.get(),
                fecha=fecha,
                hora=hora,
                modalidad=modalidad,
                notas=self._entrada_notas.get(),
            )
        except ValueError as error:
            messagebox.showerror("No se pudo crear el examen", str(error))
            return
        self._entrada_tema.delete(0, tk.END)
        self._entrada_fecha.delete(0, tk.END)
        self._entrada_hora.delete(0, tk.END)
        self._combo_modalidad.set("")
        self._entrada_notas.delete(0, tk.END)
        self._refrescar_listado()

    def _refrescar_listado(self) -> None:
        self._listado.delete(0, tk.END)
        materias_por_id = {m.id: m.nombre for m in self._materias_repo.listar()}
        for examen in self._examenes_repo.listar():
            materia_nombre = materias_por_id.get(examen.materia_id, "?")
            self._listado.insert(
                tk.END,
                f"{examen.tema} - {materia_nombre} "
                f"({formatear_fecha(examen.fecha)} {examen.hora.strftime('%H:%M')}, "
                f"{examen.modalidad.value})",
            )
