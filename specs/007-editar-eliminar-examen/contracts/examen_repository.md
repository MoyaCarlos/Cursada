# Contrato: ExamenRepository (actualizado en HU-07)

Se agregan 3 métodos al contrato de HU-06:

```python
class ExamenRepository(Protocol):
    def guardar(self, examen: Examen) -> Examen: ...   # ya existía
    def listar(self) -> list[Examen]: ...               # ya existía

    def obtener(self, id: int) -> Examen | None: ...
    def actualizar(self, examen: Examen) -> Examen: ...
    def eliminar(self, id: int) -> None: ...
```

Mismo criterio que `TareaRepository` en HU-03.
