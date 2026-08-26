import re
from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
HTML_PATTERN = re.compile(r"<[^>]+>")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CATEGORIAS = {"Familia", "Trabajo", "Amigos", "Otro"}


class PersonaCreate(BaseModel):
    nombre: str
    apellidos: str
    fecha_de_nacimiento: date | None = None
    correo_electronico: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    categoria: str | None = None
    comentarios: str | None = None

    @field_validator("nombre", "apellidos")
    @classmethod
    def validar_obligatorio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El campo es obligatorio")
        return value

    @field_validator("fecha_de_nacimiento", mode="before")
    @classmethod
    def validar_fecha(cls, value: date | str | None) -> date | None:
        if value is None:
            return None
        if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
            raise ValueError("La fecha debe usar el formato AAAA-MM-DD")
        parsed = date.fromisoformat(value)
        if parsed > date.today():
            raise ValueError("La fecha no puede ser futura")
        return parsed

    @field_validator("correo_electronico")
    @classmethod
    def validar_correo(cls, value: str | None) -> str | None:
        if value is not None and not EMAIL_PATTERN.fullmatch(value):
            raise ValueError("El correo electrónico no tiene un formato válido")
        return value

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value: str | None) -> str | None:
        if value is not None and value not in CATEGORIAS:
            raise ValueError("La categoría no está permitida")
        return value

    @field_validator("comentarios")
    @classmethod
    def validar_comentarios(cls, value: str | None) -> str | None:
        if value is not None:
            if len(value) > 500:
                raise ValueError("Los comentarios no pueden superar 500 caracteres")
            if HTML_PATTERN.search(value):
                raise ValueError("Los comentarios no pueden contener HTML")
        return value


class PersonaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellidos: str
    fecha_de_nacimiento: date | None = None
    correo_electronico: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    categoria: str | None = None
    comentarios: str | None = None


class PersonaSummary(BaseModel):
    id: int
    nombre: str
    apellidos: str