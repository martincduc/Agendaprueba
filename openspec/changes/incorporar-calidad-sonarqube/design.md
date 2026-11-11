## Context

AGENDA dispone de una API FastAPI con SQLite, una interfaz web y una suite pytest de 20 pruebas con una cobertura global del 94 % (líneas y ramas). El repositorio no tenía workflows de GitHub Actions ni ficheros de dependencias. Este cambio incorpora el análisis estático con SonarQube Community Build sin alterar el código de la aplicación. La motivación y el alcance están en `proposal.md`, y los criterios en `specs/calidad-sonarqube/spec.md`.

## Goals / Non-Goals

**Goals:**

- Analizar `app/` y `tests/` con SonarQube e importar la cobertura de pytest-cov.
- Aplicar un Quality Gate en `main` mediante un runner propio.
- Mantener pytest con umbral del 80 % en las PR.
- Demostrar con un laboratorio aislado un gate fallido y su recuperación.

**Non-Goals:**

- Cambiar endpoints, esquemas, persistencia o pruebas de AGENDA.
- Configurar análisis de PR o de múltiples ramas (no disponible en Community Build).
- Añadir API-Key, autenticación o nuevas dependencias de ejecución.

## Decisions

### Topología

- **Servidor:** SonarQube Community Build en Docker (`sonarqube-agenda`), publicado solo en `127.0.0.1:9000`, con volúmenes `agenda_sonar_data`, `agenda_sonar_extensions` y `agenda_sonar_logs`. Base de datos H2 integrada, solo para evaluación.
- **Runner:** runner propio de GitHub instalado en el mismo host que el contenedor, con las etiquetas `self-hosted`, `linux` y `sonarqube-agenda`. Así `127.0.0.1:9000` apunta al servidor. Un runner alojado por GitHub no puede alcanzarlo.
- **Scanner:** SonarScanner CLI con runtime incluido, instalado en el PATH de la cuenta del runner.

### Proyectos, perfiles y gates

- `agenda`: perfil Python Sonar way y gate por defecto, sin modificar.
- `agenda-p13-lab`: gate `P13 LAB` con una única condición, cobertura global inferior al 80 %. No se usa cobertura de código nuevo.

### Ficheros

- `requirements.txt`: dependencias de ejecución (fastapi, uvicorn), que ya se usaban y no estaban declaradas.
- `requirements-dev.txt`: incluye `requirements.txt` y añade pytest, pytest-cov y httpx (necesario para `TestClient`). Los workflows usan este fichero en lugar de instalar pytest-cov por separado, como permite la guía.
- `.coveragerc`: `relative_files`, `source = app` y `branch = True`.
- `sonar-project.properties`: clave `agenda`, fuentes `app`, pruebas `tests`, Python 3.11, cobertura `reports/coverage.xml` y espera del gate (`sonar.qualitygate.wait=true`, 300 s).
- `.gitignore`: `.scannerwork/`, `reports/`, `.p13-lab/` y `.venv-sonar/` (`.coverage` ya estaba excluido).
- `.github/workflows/pruebas.yml`: pytest con cobertura en PR hacia `main`, en un runner de GitHub (no ejecuta código de PR en el runner propio).
- `.github/workflows/sonarqube.yml`: push a `main` y ejecución manual; pruebas, cobertura, scanner y artefacto de cobertura.
- `.github/workflows/sonarqube-lab.yml`: ejecución manual con la muestra `defectuoso` o `corregido`, aislada de la configuración de AGENDA.
- `docs/p13/*.py.txt`: muestras docentes, no importadas por la aplicación.
- `docs/calidad/P13_informe.md` y `README.md`: registro de resultados y guía de uso.

### Seguridad

- Tokens de análisis de proyecto con caducidad, guardados como `SONAR_TOKEN` y `SONAR_LAB_TOKEN` en GitHub Secrets. La URL del servidor se guarda como variable `SONAR_HOST_URL`.
- `persist-credentials: false` y `permissions: contents: read` en todos los workflows.
- Los workflows del runner propio se limitan a `main` y no usan `pull_request` ni `pull_request_target`.
- El repositorio es público: antes de registrar el runner propio, hacerlo privado o limitar los runners para que no ejecuten código de forks.

### Alternativas consideradas

- SonarQube Cloud: descartado porque la práctica exige un servidor local Community Build.
- Runner alojado por GitHub con el servidor expuesto: descartado porque obligaría a publicar el servidor local en Internet.
- Excluir ficheros o bajar umbrales para obtener un gate verde: descartado expresamente.

## Risks / Trade-offs

- **[Riesgo]** El runner propio ejecuta código del repositorio en el equipo del equipo. **Mitigación:** repositorio privado, solo `main` y revisión de los workflows antes de fusionarlos.
- **[Riesgo]** Elasticsearch puede no arrancar por memoria o `vm.max_map_count`. **Mitigación:** revisar `docker logs` y los requisitos oficiales del host.
- **[Riesgo]** Confundir un fallo técnico con un gate fallido. **Mitigación:** registrar en el informe el motivo de cada ejecución roja.
- **[Trade-off]** Community Build solo analiza `main`; las PR se protegen con pytest y cobertura.

## Estrategia de pruebas

- Ejecutar `python -m pytest -q --cov=app --cov-report=xml:reports/coverage.xml --cov-fail-under=80` y comprobar que el XML usa rutas relativas.
- Simular localmente el laboratorio: la muestra defectuosa da 50 % y la corregida 100 %, y la prueba pasa en ambas.
- Verificar en SonarQube el análisis de `agenda` y las dos ejecuciones del laboratorio.
