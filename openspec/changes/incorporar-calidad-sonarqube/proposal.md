## Why

Las pruebas automáticas comprueban el comportamiento de AGENDA, pero no detectan por sí solas problemas de fiabilidad, seguridad o mantenibilidad del código. El equipo de mantenimiento necesita un análisis estático que revise el código Python de forma repetible y un umbral de calidad (Quality Gate) que se aplique en la integración continua. Corresponde a la Issue P13 – Analizar y controlar la calidad de AGENDA con SonarQube.

## What Changes

- Configurar el análisis de `app/` y `tests/` con SonarQube Community Build local mediante `sonar-project.properties`.
- Generar el informe de cobertura con pytest-cov (`reports/coverage.xml`) y configurarlo en `.coveragerc` para que SonarQube lo importe.
- Declarar las dependencias en `requirements.txt` (ejecución) y `requirements-dev.txt` (pruebas y cobertura), que hasta ahora no estaban versionadas.
- Añadir el workflow `.github/workflows/pruebas.yml`, que ejecuta pytest con un umbral de cobertura del 80 % en cada PR hacia `main`.
- Añadir el workflow `.github/workflows/sonarqube.yml`, que analiza `main` en un runner propio y falla si el Quality Gate falla.
- Añadir un laboratorio independiente (`docs/p13/` y `.github/workflows/sonarqube-lab.yml`) que analiza una muestra docente defectuosa y otra corregida en el proyecto `agenda-p13-lab`.
- Documentar la instalación, el uso y los resultados en `README.md` y `docs/calidad/P13_informe.md`.
- No modificar `docs/architecture.md`: GitHub Actions ya figura entre las tecnologías aprobadas y el cambio no altera la arquitectura funcional. SonarQube y SonarScanner son herramientas externas de proceso, no dependencias de la aplicación.

Quedan fuera de este cambio: cualquier cambio en endpoints, esquemas o persistencia de AGENDA; autenticación o API-Key; el análisis de PR y de ramas múltiples (no disponible en Community Build); la publicación del servidor SonarQube en Internet; y los tokens o contraseñas en el repositorio.

## Capabilities

### New Capabilities

- `calidad-sonarqube`: análisis estático de AGENDA con SonarQube, importación de cobertura y aplicación de un Quality Gate en GitHub Actions, con un laboratorio que demuestra un fallo y su recuperación.

### Modified Capabilities

- Ninguna. `registrar-persona` y `listar-personas` conservan su contrato.

## Impact

- Ficheros nuevos: `sonar-project.properties`, `.coveragerc`, `requirements.txt`, `requirements-dev.txt`, tres workflows, muestras de `docs/p13/` y `docs/calidad/P13_informe.md`.
- Ficheros modificados: `.gitignore` y `README.md`.
- Infraestructura local: contenedor Docker `sonarqube-agenda`, SonarScanner CLI y runner propio con la etiqueta `sonarqube-agenda`.
- Secretos de GitHub: `SONAR_TOKEN` y `SONAR_LAB_TOKEN`; variable `SONAR_HOST_URL`.
- No se modifica el código de `app/` ni las pruebas existentes.
