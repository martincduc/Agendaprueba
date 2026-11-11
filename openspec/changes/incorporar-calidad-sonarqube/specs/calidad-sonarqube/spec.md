## Purpose

Esta capacidad permite al equipo de mantenimiento de AGENDA detectar defectos estáticos, revisar la cobertura de las pruebas y aplicar un umbral de calidad en la integración continua sin modificar el comportamiento funcional de la aplicación.

## ADDED Requirements

### Requirement: Analizar el código de AGENDA

El análisis SHALL inspeccionar el código de `app/` como código fuente y `tests/` como código de prueba, y SHALL publicar el resultado en el proyecto SonarQube `agenda`.

#### Scenario: Análisis local correcto

- **GIVEN** que el servidor SonarQube está operativo y existe un token de análisis válido para `agenda`
- **WHEN** el equipo ejecuta `sonar-scanner` desde la raíz del repositorio
- **THEN** el proyecto `agenda` muestra un análisis con los ficheros de `app/` como código y los de `tests/` como pruebas

#### Scenario: Servidor no disponible

- **GIVEN** que el servidor SonarQube no está operativo
- **WHEN** se ejecuta el análisis
- **THEN** el scanner termina con un error técnico y no se publica ningún informe

### Requirement: Importar la cobertura

El proceso SHALL generar `reports/coverage.xml` con pytest-cov, con rutas relativas, y SonarQube SHALL importarlo. La suite SHALL fallar si la cobertura global es inferior al 80 %.

#### Scenario: Cobertura importada

- **GIVEN** que pytest se ejecuta con `--cov=app --cov-report=xml:reports/coverage.xml`
- **WHEN** el scanner analiza el repositorio
- **THEN** SonarQube muestra la cobertura medida de AGENDA sin advertencias de rutas

#### Scenario: Cobertura insuficiente

- **GIVEN** que la cobertura global de `app/` es inferior al 80 %
- **WHEN** se ejecutan las pruebas con `--cov-fail-under=80`
- **THEN** el paso de pruebas falla

### Requirement: Aplicar el Quality Gate en GitHub Actions

Un push a `main` o una ejecución manual sobre `main` SHALL ejecutar pruebas, cobertura y análisis en el runner propio. El job SHALL fallar cuando el Quality Gate falle. Las PR hacia `main` SHALL ejecutar pytest con el umbral de cobertura.

#### Scenario: Gate superado

- **GIVEN** que el código de `main` cumple las condiciones del gate de `agenda`
- **WHEN** se ejecuta el workflow Calidad SonarQube AGENDA
- **THEN** el job termina correctamente y SonarQube registra el commit analizado

#### Scenario: Gate fallido

- **GIVEN** que el análisis no cumple las condiciones del gate
- **WHEN** el scanner espera el resultado del gate
- **THEN** el job termina con error

#### Scenario: Pull request

- **GIVEN** que se abre una PR hacia `main`
- **WHEN** se ejecuta el workflow Pruebas AGENDA
- **THEN** se ejecuta la suite pytest con el umbral del 80 %, sin análisis SonarQube

### Requirement: Proteger las credenciales

Los tokens de análisis SHALL almacenarse únicamente en GitHub Secrets o introducirse sin eco en la terminal. Ningún fichero versionado SHALL contener tokens ni contraseñas.

#### Scenario: Repositorio sin secretos

- **GIVEN** que el cambio está listo para integrarse
- **WHEN** se revisa el diff
- **THEN** no aparece ningún token, contraseña ni informe generado

### Requirement: Demostrar un fallo y su recuperación

El laboratorio SHALL analizar una muestra docente en el proyecto independiente `agenda-p13-lab`, con un gate cuya única condición es cobertura global inferior al 80 %. Las muestras SHALL permanecer como ficheros `.txt` fuera de `app/`.

#### Scenario: Muestra defectuosa

- **GIVEN** que se ejecuta el laboratorio con la muestra `defectuoso`
- **WHEN** termina el análisis
- **THEN** la prueba pasa, la cobertura queda por debajo del 80 % y el gate falla

#### Scenario: Muestra corregida

- **GIVEN** que se ejecuta el laboratorio con la muestra `corregido`
- **WHEN** termina el análisis
- **THEN** la prueba pasa, la cobertura es del 100 % y el gate se supera

### Requirement: Conservar el contrato funcional

El cambio SHALL NOT modificar los endpoints, esquemas, persistencia ni pruebas existentes de AGENDA.

#### Scenario: Suite existente

- **GIVEN** que el cambio está aplicado
- **WHEN** se ejecuta `python -m pytest`
- **THEN** todas las pruebas existentes de registrar y listar personas pasan sin modificaciones
