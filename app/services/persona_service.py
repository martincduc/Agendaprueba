from pathlib import Path

from app.repositories.persona_repository import PersonaRepository
from app.schemas.persona import PersonaCreate


class PersonaService:
    def __init__(self, database_path: str | Path):
        self.repository = PersonaRepository(database_path)

    def create(self, persona: PersonaCreate) -> dict:
        return self.repository.create(**persona.model_dump())