from datetime import date
from pathlib import Path

from app import database


class PersonaRepository:
    def __init__(self, database_path: str | Path):
        self.database_path = database_path

    def create(
        self,
        nombre: str,
        apellidos: str,
        fecha_de_nacimiento: date | None,
        correo_electronico: str | None,
        telefono: str | None,
        direccion: str | None,
        categoria: str | None,
        comentarios: str | None,
    ) -> dict:
        return database.insert_persona(
            self.database_path,
            nombre,
            apellidos,
            fecha_de_nacimiento,
            correo_electronico,
            telefono,
            direccion,
            categoria,
            comentarios,
        )