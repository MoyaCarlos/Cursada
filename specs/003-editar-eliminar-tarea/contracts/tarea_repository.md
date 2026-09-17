# Contrato: TareaRepository (actualizado en HU-03)

Se agregan 3 métodos al contrato definido en HU-02
(`specs/002-crear-tarea/contracts/tarea_repository.md`):

```python
class TareaRepository(Protocol):
    def guardar(self, tarea: Tarea) -> Tarea: ...   # ya existía (HU-02)
    def listar(self) -> list[Tarea]: ...             # ya existía (HU-02)

    def obtener(self, id: int) -> Tarea | None:
        """Una tarea por id, o None si no existe."""

    def actualizar(self, tarea: Tarea) -> Tarea:
        """Actualiza una tarea existente (tarea.id no es None). Devuelve
        la tarea actualizada."""

    def eliminar(self, id: int) -> None:
        """Elimina la tarea y su evento asociado (borrado real, sin rastro)."""
```

**Implementación de producción**: se agrega a `SqliteTareaRepository`.

**Implementación para tests**: se agrega a `TareaRepositoryFake`.
