# Research: Gestión de Materias (HU-01)

## Tkinter no disponible en la máquina de desarrollo (Linux)

- **Decisión**: seguir con Tkinter (ya decidido en `CLAUDE.md` sobre
  PySide/Electron/Tauri por peso y por venir en la stdlib).
- **Hallazgo**: en esta máquina (CachyOS/Arch), Python 3.14 está instalado
  pero falta `libtk8.6.so` — el paquete `tk` no viene junto al intérprete
  por defecto en esta distro.
- **Acción requerida (usuario)**: `sudo pacman -S tk` en Linux/Arch antes de
  poder ejecutar o testear la UI localmente. En Windows no debería hacer
  falta nada extra: el instalador oficial de python.org incluye Tk.
- **Alternativas consideradas**: ninguna nueva — ya se descartaron PySide/Qt
  (peso) y Tauri/PyTauri (requieren Rust o son inmaduros) en la planificación
  inicial del proyecto.

## Ubicación del archivo SQLite

- **Decisión**: usar el directorio de datos de usuario estándar de cada SO,
  no la carpeta de instalación (evita problemas de permisos si se instala en
  `Program Files` o `/usr/`, y es la convención esperada en cada plataforma).
  - Linux: `$XDG_DATA_HOME/cursada/cursada.db`, con fallback a
    `~/.local/share/cursada/cursada.db` si `XDG_DATA_HOME` no está definida.
  - Windows: `%APPDATA%\Cursada\cursada.db`.
- **Rationale**: es el comportamiento estándar de cada plataforma para datos
  de aplicación de un solo usuario; no requiere ninguna librería externa,
  se resuelve con `os.environ` y `pathlib` de la stdlib.
- **Alternativas consideradas**: guardar el `.db` junto al ejecutable —
  descartado porque en Windows/Linux instalar en una carpeta de sistema
  suele requerir permisos de administrador solo para escribir un archivo de
  datos, y complica el empaquetado con PyInstaller (HU-18/HU-19).

## Convención de nombres: español vs. inglés en el código

- **Decisión**: identificadores de dominio (clases, funciones, módulos) en
  español, calcados de los términos de `CONTEXT.md` (`Materia`,
  `crear_materia`, `MateriaRepository`).
- **Rationale**: `CONTEXT.md` ya define el lenguaje ubicuo del proyecto en
  español; traducir al inglés en el código introduciría una capa de
  traducción innecesaria y abriría la puerta a que código y glosario se
  desalineen con el tiempo (justo lo que la skill `domain-modeling` está para
  evitar).
- **Alternativas consideradas**: inglés por convención general de la
  industria — descartado porque el proyecto es en español de punta a punta
  (specs, glosario, UI) y no hay ninguna razón externa (librería, equipo
  angloparlante) que lo justifique.

## Validación de nombre único: dónde vive cada parte de la regla

- **Decisión**: la validación de formato (nombre no vacío / solo espacios)
  vive en la factory de dominio `crear_materia(nombre)`, que no depende de
  infraestructura. La validación de unicidad (requiere consultar datos
  existentes) vive en el service (`CrearMateria`/`EditarMateria`), que
  consulta `MateriaRepository.existe_nombre(nombre)` antes de invocar la
  factory de dominio.
- **Rationale**: mantiene el dominio puro (sin I/O) tal como exige la
  arquitectura hexagonal ya definida, sin duplicar la regla de "no vacío" en
  cada service.
