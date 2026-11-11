# P13 – Informe de calidad con SonarQube

> Completar con datos reales. No escribir métricas de ejecuciones que no se han realizado.
> No incluir tokens, contraseñas ni capturas que los muestren.

## 1. Instalación

| Dato | Valor |
|---|---|
| Versión de SonarQube | Completar |
| Digest de la imagen (`sonarqube@sha256:...`) | Completar |
| Versión de SonarScanner CLI | Completar |
| Python del runner (`python3.11 --version`) | Completar |
| Topología | Servidor Docker y runner propio en el mismo host; `SONAR_HOST_URL=http://127.0.0.1:9000` |
| Modo de experiencia (Standard / MQR) | Completar |

## 2. Configuración

| Proyecto | Clave | Quality Profile | Quality Gate y condiciones | Código nuevo |
|---|---|---|---|---|
| AGENDA | `agenda` | Python Sonar way | Completar (gate por defecto) | Completar |
| AGENDA P13 LAB | `agenda-p13-lab` | Completar | P13 LAB: cobertura global < 80 % → error | No se usa |

Reglas del laboratorio (comprobar si están activas en el perfil):

| Hipótesis | Regla | ¿Activa? |
|---|---|---|
| Comparación de una expresión consigo misma | Completar | Completar |
| Variable local sin uso | Completar | Completar |
| Código sin cobertura | Condición del gate | Sí |

## 3. Comparación

| Dato | AGENDA inicial | LAB defectuoso | LAB corregido |
|---|---|---|---|
| Commit o run ID | Completar | Completar | Completar |
| Fecha | Completar | Completar | Completar |
| Pruebas y resultado | Completar | 1 correcta | 1 correcta |
| Cobertura importada | Completar | Menor que 80 % | 100 % esperado |
| Hallazgos y reglas | Completar | Medidos | Medidos |
| Gate y motivo | Completar | Fallo por cobertura | Superado esperado |
| Perfil y versión | Completar | Completar | Mismos que antes |

Referencia local antes del análisis (pytest-cov, 2026-11-11): AGENDA 20 pruebas correctas y 94 % de cobertura de líneas y ramas; muestra defectuosa 50 %; muestra corregida 100 %. El porcentaje de SonarQube puede diferir según su cómputo.

## 4. Línea base de AGENDA

| Métrica | Valor |
|---|---|
| Líneas de código | Completar |
| Cobertura | Completar |
| Duplicación | Completar |
| Fiabilidad | Completar |
| Seguridad / hotspots | Completar |
| Mantenibilidad | Completar |
| Quality Gate | Completar |

## 5. Hallazgos revisados

| Archivo | Línea | Regla | Impacto | Decisión | Comprobación |
|---|---|---|---|---|---|
| Completar | | | | | |

Si no hubo hallazgos reales en AGENDA, indicarlo aquí y no introducir cambios artificiales.

## 6. Explicación del laboratorio

Completar: por qué ambas muestras pasan pytest y solo la corregida supera el gate.
