from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from app.database import DEFAULT_DATABASE_PATH, PersistenceError, initialize_database
from app.schemas.persona import PersonaCreate, PersonaResponse, PersonaSummary
from app.services.persona_service import PersonaService


def create_app(database_path: str | Path = DEFAULT_DATABASE_PATH) -> FastAPI:
    initialize_database(database_path)
    application = FastAPI(title="AGENDA")
    service = PersonaService(database_path)

    @application.post(
        "/api/personas",
        response_model=PersonaResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_persona(persona: PersonaCreate) -> dict:
        try:
            return service.create(persona)
        except PersistenceError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo registrar la persona",
            ) from error

    @application.get(
        "/api/personas",
        response_model=list[PersonaSummary],
    )
    def list_personas() -> list[dict]:
        try:
            return service.list()
        except PersistenceError as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo cargar el listado de personas",
            ) from error

    @application.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(Path(__file__).parent / "static" / "index.html")

    return application


app = create_app()