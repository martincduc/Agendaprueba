## Why

El propietario de la agenda necesita registrar personas para conservar su información y consultarla posteriormente. HU-01 habilita el primer flujo funcional de AGENDA mediante el alta de personas con los datos acordados y validaciones claras.

## What Changes

- Añadir la capacidad de registrar una persona mediante `POST /api/personas`.
- Aceptar nombre y apellidos obligatorios, y fecha de nacimiento, correo electrónico, teléfono, dirección, categoría y comentarios opcionales.
- Validar la fecha de nacimiento (`AAAA-MM-DD` y no futura), el formato del correo cuando se proporcione, la categoría permitida y el límite de 500 caracteres de los comentarios sin HTML.
- Generar un identificador único para cada persona y permitir registros duplicados.
- Mantener los datos registrados en SQLite y mostrar el formulario web correspondiente.
- No modificar `docs/architecture.md`; la historia respeta la arquitectura y las tecnologías aprobadas.

Quedan fuera de este cambio la autenticación, la autorización, la gestión de roles, la modificación y eliminación de personas, la búsqueda, los filtros, la paginación, la importación y exportación, la detección de duplicados y cualquier despliegue o tecnología adicional.

## Capabilities

### New Capabilities

- `registrar-persona`: registrar personas de la agenda mediante la API y el formulario web, aplicando las validaciones de HU-01 y persistiendo sus datos.

### Modified Capabilities

- Ninguna.

## Impact

- API FastAPI: nuevo endpoint `POST /api/personas`, sus esquemas, validaciones y respuestas HTTP.
- Servicios y repositorios: caso de uso de registro y acceso a SQLite, manteniendo el SQL en la capa de persistencia definida por la arquitectura.
- Interfaz web: formulario de alta que consume la API y presenta errores de validación sin acceder directamente a SQLite.
- Pruebas pytest: cobertura de los escenarios correctos y de error de HU-01.
- No se requieren nuevas dependencias ni cambios arquitectónicos.