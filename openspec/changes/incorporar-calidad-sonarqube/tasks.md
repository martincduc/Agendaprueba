## 1. Configuración del repositorio

- [x] 1.1 Crear `requirements.txt` y `requirements-dev.txt` con las dependencias ya utilizadas, más pytest-cov.
- [x] 1.2 Crear `.coveragerc` con `relative_files`, `source = app` y `branch = True`.
- [x] 1.3 Crear `sonar-project.properties` sin tokens ni contraseñas.
- [x] 1.4 Añadir `.scannerwork/`, `reports/`, `.p13-lab/` y `.venv-sonar/` a `.gitignore`.
- [x] 1.5 Verificar localmente que pytest genera `reports/coverage.xml` con rutas relativas y supera el 80 %.

## 2. Workflows

- [x] 2.1 Crear `.github/workflows/pruebas.yml` para ejecutar pytest con cobertura en PR hacia `main`.
- [x] 2.2 Crear `.github/workflows/sonarqube.yml` para analizar `main` en el runner propio y fallar si falla el gate.
- [x] 2.3 Crear `.github/workflows/sonarqube-lab.yml` para el laboratorio manual.

## 3. Laboratorio

- [x] 3.1 Crear `docs/p13/defectuoso.py.txt`, `docs/p13/corregido.py.txt` y `docs/p13/test_demo.py.txt`.
- [x] 3.2 Simular localmente la prueba y la cobertura de ambas muestras (50 % y 100 %).

## 4. Infraestructura local (manual, fuera del repositorio)

- [ ] 4.1 Instalar SonarQube Community Build con Docker y registrar versión y digest.
- [ ] 4.2 Cambiar la contraseña de admin y comprobar la persistencia tras reiniciar.
- [ ] 4.3 Crear los proyectos `agenda` y `agenda-p13-lab`, el gate `P13 LAB` y dos Project Analysis Tokens.
- [ ] 4.4 Instalar SonarScanner CLI y ejecutar el primer análisis local de `agenda`.
- [ ] 4.5 Registrar el runner propio con la etiqueta `sonarqube-agenda`.
- [ ] 4.6 Crear `SONAR_TOKEN`, `SONAR_LAB_TOKEN` y la variable `SONAR_HOST_URL` en GitHub.

## 5. Ejecución y evidencias

- [ ] 5.1 Integrar la PR en `main` y comprobar el workflow Calidad SonarQube AGENDA.
- [ ] 5.2 Ejecutar el laboratorio con `defectuoso` (gate fallido) y con `corregido` (gate superado).
- [ ] 5.3 Completar `docs/calidad/P13_informe.md` con los datos reales.
- [ ] 5.4 Revisar los hallazgos reales de `agenda` y corregirlos mediante PR, o documentar que no los hay.

## 6. Verificación final

- [x] 6.1 Ejecutar `pytest` y confirmar que las pruebas existentes pasan sin cambios.
- [x] 6.2 Comprobar que no hay tokens, informes generados ni cambios en `app/`.
- [x] 6.3 Comprobar la conformidad con `docs/architecture.md`.
- [ ] 6.4 Archivar el cambio con `/opsx:archive incorporar-calidad-sonarqube` y cerrar la Issue con enlaces a las evidencias.
