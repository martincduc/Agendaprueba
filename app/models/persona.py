from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Persona:
    id: int
    nombre: str
    apellidos: str
    fecha_de_nacimiento: date | None
    correo_electronico: str | None
    telefono: str | None
    direccion: str | None
    categoria: str | None
    comentarios: str | None