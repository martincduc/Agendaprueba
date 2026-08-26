## Why

El propietario de la agenda necesita consultar de forma rápida qué personas están registradas y acceder a su información básica. HU-02 completa el flujo inicial de AGENDA ofreciendo un listado ordenado, incluido el caso de una agenda vacía.

## What Changes

- Añadir la capacidad de listar personas mediante `GET /api/personas`.
- Devolver para cada persona únicamente su ID, nombre y apellidos, ordenados por apellidos y nombre.
- Devolver `200` y `[]` cuando no existan personas, sin paginación.
- Mostrar el listado en la interfaz web y un mensaje específico cuando la agenda esté vacía.
- Actualizar el listado después de registrar una persona.
- Tratar los errores de consulta de forma controlada, sin exponer trazas internas.
- No modificar `docs/architecture.md`; la historia implementa un endpoint ya previsto por la arquitectura.

Quedan fuera de este cambio la autenticación, la autorización, los roles, la modificación y eliminación de personas, la búsqueda avanzada, los filtros, la paginación, la importación y exportación, la detección de duplicados y cualquier tecnología o dependencia nueva.

## Capabilities

### New Capabilities

- `listar-personas`: consultar y mostrar todas las personas registradas, ordenadas por apellidos y nombre, incluyendo el estado de agenda vacía.

### Modified Capabilities

- Ninguna.

## Impact

- API FastAPI: completar `GET /api/personas` con respuesta de listado, ordenación y errores HTTP controlados.
- Servicios y repositorios: añadir el caso de uso de consulta y la operación de lectura desde SQLite, manteniendo el SQL en la persistencia definida por la arquitectura.
- Interfaz web: presentar ID, nombre y apellidos, mensaje de agenda vacía y actualización tras un registro, consumiendo la API.
- Pruebas pytest: cubrir listado ordenado, listado vacío, actualización tras alta y errores controlados.
- No se requieren nuevas dependencias ni cambios arquitectónicos.