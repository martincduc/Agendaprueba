import sqlite3
from datetime import date
from pathlib import Path


DEFAULT_DATABASE_PATH = Path("agenda.sqlite3")


class PersistenceError(Exception):
    pass


def initialize_database(database_path: str | Path = DEFAULT_DATABASE_PATH) -> None:
    try:
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    fecha_de_nacimiento TEXT,
                    correo_electronico TEXT,
                    telefono TEXT,
                    direccion TEXT,
                    categoria TEXT,
                    comentarios TEXT
                )
                """
            )
    except sqlite3.Error as error:
        raise PersistenceError from error


def insert_persona(
    database_path: str | Path,
    nombre: str,
    apellidos: str,
    fecha_de_nacimiento: date | None,
    correo_electronico: str | None,
    telefono: str | None,
    direccion: str | None,
    categoria: str | None,
    comentarios: str | None,
) -> dict:
    try:
        with sqlite3.connect(database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO personas (
                    nombre, apellidos, fecha_de_nacimiento, correo_electronico,
                    telefono, direccion, categoria, comentarios
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    nombre,
                    apellidos,
                    fecha_de_nacimiento.isoformat() if fecha_de_nacimiento else None,
                    correo_electronico,
                    telefono,
                    direccion,
                    categoria,
                    comentarios,
                ),
            )
            return {
                "id": cursor.lastrowid,
                "nombre": nombre,
                "apellidos": apellidos,
                "fecha_de_nacimiento": fecha_de_nacimiento,
                "correo_electronico": correo_electronico,
                "telefono": telefono,
                "direccion": direccion,
                "categoria": categoria,
                "comentarios": comentarios,
            }
    except sqlite3.Error as error:
        raise PersistenceError from error