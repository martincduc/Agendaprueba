
# Proyecto agenda — Equipo 1

## Miembros
- Pablo Martínez
- Martín Sáez
- Joao Morales
- Gonzalo Anabalón
- Vicente Jiménez
- Benjamín Navarro
- Felipe Oregón

## Objetivo
Repositorio de práctica para familiarizarnos con GitHub como fábrica de software (Issues, Milestones, Projects, Copilot y GitHub Actions) antes de aplicarlo al repositorio final de HumWorld.

## Estado
Proyecto en fase inicial.

## Ejecutar AGENDA y las pruebas

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
uvicorn app.main:app --reload          # http://127.0.0.1:8000
python -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=80
```

## Calidad con SonarQube (P13)

Topología: SonarQube Community Build en Docker y un runner propio de GitHub en el **mismo equipo**.
El servidor solo escucha en `127.0.0.1:9000` y no se publica en Internet. Community Build analiza
únicamente la rama `main`: no hay análisis de PR. Las PR se protegen con el workflow `Pruebas AGENDA`.

| Workflow | Cuándo | Dónde |
|---|---|---|
| `Pruebas AGENDA` (`pruebas.yml`) | PR hacia `main` | Runner de GitHub |
| `Calidad SonarQube AGENDA` (`sonarqube.yml`) | Push a `main` y manual | Runner propio `sonarqube-agenda` |
| `Laboratorio P13 SonarQube` (`sonarqube-lab.yml`) | Manual (`defectuoso` / `corregido`) | Runner propio `sonarqube-agenda` |

### Iniciar y detener SonarQube

```bash
# Primera vez
docker pull sonarqube:community
SONAR_IMAGE=$(docker image inspect sonarqube:community --format '{{index .RepoDigests 0}}')
docker run -d --name sonarqube-agenda -p 127.0.0.1:9000:9000 \
  -v agenda_sonar_data:/opt/sonarqube/data \
  -v agenda_sonar_extensions:/opt/sonarqube/extensions \
  -v agenda_sonar_logs:/opt/sonarqube/logs \
  "$SONAR_IMAGE"

# Sesiones siguientes
docker start sonarqube-agenda
curl -fsS http://127.0.0.1:9000/api/system/status   # esperar "status":"UP"
docker stop sonarqube-agenda                         # al terminar; conserva los volúmenes
```

No usar `docker rm`, `docker volume prune` ni `docker system prune`: borran los datos.

### Análisis local

```bash
mkdir -p reports
python -m pytest -q --cov=app --cov-report=xml:reports/coverage.xml --cov-fail-under=80
export SONAR_HOST_URL=http://127.0.0.1:9000
read -rsp "Token de analisis AGENDA: " SONAR_TOKEN; printf '\n'; export SONAR_TOKEN
sonar-scanner
unset SONAR_TOKEN
```

SonarQube no ejecuta pytest: la cobertura se regenera siempre con el comando de pytest anterior.

### Configuración de GitHub

- Runner propio: Settings → Actions → Runners, Linux, etiqueta adicional `sonarqube-agenda`. Arrancar con `./run.sh`.
  Debe tener `git`, `python3.11`, `sonar-scanner` y `curl` en el PATH.
- Secrets: `SONAR_TOKEN` (proyecto `agenda`) y `SONAR_LAB_TOKEN` (proyecto `agenda-p13-lab`).
- Variable: `SONAR_HOST_URL=http://127.0.0.1:9000`.
- Usar el runner propio solo con un repositorio privado y colaboradores de confianza.

### Leer los resultados

Un job rojo puede deberse a un **fallo técnico** (servidor caído, token inválido, runner offline) o a un
**Quality Gate fallido** (el análisis se publicó, pero no supera las condiciones). Revisar el log del paso
del scanner y el proyecto en SonarQube. Las versiones, el digest, el perfil, el gate y los resultados se
registran en [`docs/calidad/P13_informe.md`](docs/calidad/P13_informe.md).
