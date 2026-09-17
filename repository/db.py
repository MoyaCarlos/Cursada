import os
import sqlite3
from pathlib import Path


def _ruta_base_datos() -> Path:
    if os.name == "nt":
        base = Path(os.environ["APPDATA"]) / "Cursada"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "cursada"
    base.mkdir(parents=True, exist_ok=True)
    return base / "cursada.db"


def conectar(ruta: Path | str | None = None) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta or _ruta_base_datos())
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas(conexion: sqlite3.Connection) -> None:
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            nombre_normalizado TEXT NOT NULL UNIQUE
        )
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia_id INTEGER NOT NULL REFERENCES materias(id),
            titulo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT
        )
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS estados (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE
        )
        """
    )
    conexion.execute(
        """
        INSERT OR IGNORE INTO estados (id, nombre) VALUES
            (1, 'pendiente'), (2, 'en_progreso'), (3, 'completada')
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS prioridades (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE
        )
        """
    )
    conexion.execute(
        """
        INSERT OR IGNORE INTO prioridades (id, nombre) VALUES
            (1, 'baja'), (2, 'media'), (3, 'alta')
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
            evento_id INTEGER PRIMARY KEY REFERENCES eventos(id),
            descripcion TEXT NOT NULL DEFAULT '',
            estado_id INTEGER NOT NULL REFERENCES estados(id),
            prioridad_id INTEGER NOT NULL REFERENCES prioridades(id)
        )
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS modalidades (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE
        )
        """
    )
    conexion.execute(
        """
        INSERT OR IGNORE INTO modalidades (id, nombre) VALUES
            (1, 'presencial'), (2, 'virtual')
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS examenes (
            evento_id INTEGER PRIMARY KEY REFERENCES eventos(id),
            modalidad_id INTEGER NOT NULL REFERENCES modalidades(id),
            notas TEXT NOT NULL DEFAULT ''
        )
        """
    )
    conexion.commit()
