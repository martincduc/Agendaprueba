from datetime import date, timedelta
from pathlib import Path
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app import database


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(tmp_path / "test.sqlite3"))


def test_registro_completo_devuelve_201_y_datos(client):
    payload = {
        "nombre": "Ana",
        "apellidos": "García López",
        "fecha_de_nacimiento": "1990-05-12",
        "correo_electronico": "ana@example.com",
        "telefono": "555123",
        "direccion": "Calle Principal 1",
        "categoria": "Familia",
        "comentarios": "Contacto principal",
    }

    response = client.post("/api/personas", json=payload)

    assert response.status_code == 201
    assert response.json() == {"id": 1, **payload}


def test_registro_minimo_genera_id(client):
    response = client.post(
        "/api/personas", json={"nombre": "Luis", "apellidos": "Pérez"}
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["nombre"] == "Luis"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("nombre", "   "),
        ("apellidos", ""),
        ("fecha_de_nacimiento", "12/05/1990"),
        ("fecha_de_nacimiento", (date.today() + timedelta(days=1)).isoformat()),
        ("correo_electronico", "correo-invalido"),
        ("categoria", "Conocidos"),
        ("comentarios", "<b>HTML</b>"),
        ("comentarios", "x" * 501),
    ],
)
def test_datos_invalidos_devuelven_422_y_no_persisten(client, field, value):
    payload = {"nombre": "Ana", "apellidos": "García", field: value}
    if field == "apellidos" and value == "":
        payload.pop("apellidos")

    response = client.post("/api/personas", json=payload)

    assert response.status_code == 422
    assert client.post(
        "/api/personas", json={"nombre": "Correcto", "apellidos": "Válido"}
    ).json()["id"] == 1


def test_se_permiten_duplicados_con_ids_distintos(client):
    payload = {"nombre": "Ana", "apellidos": "García"}

    first = client.post("/api/personas", json=payload)
    second = client.post("/api/personas", json=payload)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]


def test_datos_persisten_al_recrear_la_aplicacion(tmp_path):
    database_path = tmp_path / "persistent.sqlite3"
    first_client = TestClient(create_app(database_path))
    created = first_client.post(
        "/api/personas", json={"nombre": "Ana", "apellidos": "García"}
    )

    second_client = TestClient(create_app(database_path))
    assert second_client.get("/docs").status_code == 200
    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            "SELECT id, nombre, apellidos FROM personas"
        ).fetchone()
    assert row == (created.json()["id"], "Ana", "García")


def test_formulario_envia_datos_a_la_api():
    html = (Path(__file__).parents[1] / "app" / "static" / "index.html").read_text()

    assert 'fetch("/api/personas"' in html
    assert "sqlite" not in html.lower()


def test_error_de_persistencia_devuelve_respuesta_controlada(client, monkeypatch):
    def fail_insert(*args, **kwargs):
        raise database.PersistenceError

    monkeypatch.setattr(database, "insert_persona", fail_insert)
    response = client.post(
        "/api/personas", json={"nombre": "Ana", "apellidos": "García"}
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo registrar la persona"}


def test_listado_vacio_devuelve_200_y_lista_vacia(client):
    response = client.get("/api/personas")

    assert response.status_code == 200
    assert response.json() == []


def test_listado_devuelve_todas_las_personas_con_campos_basicos(client):
    client.post("/api/personas", json={"nombre": "Ana", "apellidos": "García"})
    client.post("/api/personas", json={"nombre": "Luis", "apellidos": "Pérez"})

    response = client.get("/api/personas")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "nombre": "Ana", "apellidos": "García"},
        {"id": 2, "nombre": "Luis", "apellidos": "Pérez"},
    ]


def test_listado_se_ordena_por_apellidos_y_nombre(client):
    for nombre, apellidos in [("Zoe", "Alonso"), ("Ana", "López"), ("Luis", "Alonso")]:
        client.post(
            "/api/personas", json={"nombre": nombre, "apellidos": apellidos}
        )

    response = client.get("/api/personas")

    assert [(item["apellidos"], item["nombre"]) for item in response.json()] == [
        ("Alonso", "Luis"),
        ("Alonso", "Zoe"),
        ("López", "Ana"),
    ]


def test_listado_se_actualiza_despues_de_registrar(client):
    client.post("/api/personas", json={"nombre": "Ana", "apellidos": "García"})

    response = client.get("/api/personas")

    assert response.json() == [{"id": 1, "nombre": "Ana", "apellidos": "García"}]


def test_error_de_consulta_devuelve_respuesta_controlada(client, monkeypatch):
    def fail_list(*args, **kwargs):
        raise database.PersistenceError

    monkeypatch.setattr(database, "list_personas", fail_list)
    response = client.get("/api/personas")

    assert response.status_code == 500
    assert response.json() == {"detail": "No se pudo cargar el listado de personas"}


def test_interfaz_muestra_listado_vacio_y_actualiza_despues_del_alta():
    html = (Path(__file__).parents[1] / "app" / "static" / "index.html").read_text()

    assert 'fetch("/api/personas")' in html
    assert "La agenda no contiene personas." in html
    assert "await loadPersonas()" in html