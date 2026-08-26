## Context

HU-02 completa el primer incremento de AGENDA con la consulta de personas registradas. La motivación y el alcance funcional están en `proposal.md`; los contratos observables están en `specs/listar-personas/spec.md`. La solución debe respetar `docs/architecture.md`, el contexto de `openspec/config.yaml` y la separación en capas, sin añadir tecnologías ni dependencias.

## Goals / Non-Goals

**Goals:**

- Exponer el listado completo de personas con los campos básicos solicitados y orden estable por apellidos y nombre.
- Representar correctamente una agenda vacía y actualizar la interfaz tras un registro exitoso.
- Propagar errores de consulta como respuestas controladas, sin trazas internas.
- Mantener el acceso a SQLite aislado y cubrir HU-02 con pruebas automatizadas.

**Non-Goals:**

- Añadir paginación, búsqueda, filtros, ordenación configurable, edición o eliminación de personas.
- Incorporar autenticación, autorización, roles, importación, exportación, nuevas capas o nuevas dependencias.

## Decisions

### Participación de las capas

- **Interfaz:** `app/static/index.html` solicitará `GET /api/personas`, representará ID, nombre y apellidos, mostrará el mensaje de agenda vacía y gestionará el error de carga. Tras un alta exitosa de HU-01, volverá a solicitar el listado o actualizará su estado mediante la API. No accederá a SQLite ni contendrá reglas de negocio.
- **API:** `app/main.py` expondrá `GET /api/personas`, invocará el servicio, construirá la respuesta JSON con los campos básicos y traducirá fallos conocidos a códigos HTTP coherentes. No contendrá sentencias SQL.
- **Servicios:** `app/services/persona_service.py` coordinará la consulta del listado y devolverá el resultado al endpoint. No dependerá de la interfaz.
- **Repositorios:** `app/repositories/persona_repository.py` encapsulará la operación de lectura y solicitará a persistencia todas las personas en el orden requerido. No contendrá sentencias SQL.
- **Persistencia:** `app/database.py` mantendrá la consulta SQLite que obtiene ID, nombre y apellidos de todas las personas, aplicando el orden ascendente por apellidos y nombre. Devolverá una colección vacía cuando no haya filas y tratará los fallos de acceso de forma controlable.

### Contrato y actualización

El endpoint devolverá una lista JSON, incluso cuando esté vacía, sin paginación ni metadatos adicionales. La respuesta de cada elemento se limitará a ID, nombre y apellidos para cumplir el contrato de información básica. La interfaz reutilizará la misma ruta de listado después de un registro correcto para evitar divergencias entre el estado mostrado y el almacenado.

### Ficheros afectados

- Modificar o crear `app/main.py`, `app/database.py`, `app/services/persona_service.py`, `app/repositories/persona_repository.py`, los esquemas o modelos existentes en `app/schemas/` y `app/models/`, `app/static/index.html` y `tests/test_agenda.py`.
- Mantener las sentencias SQL únicamente en `app/database.py` y no concentrar el flujo en un único fichero.

### Estrategia de pruebas

- Pruebas de API para `200`, campos básicos, inclusión de todas las personas y orden por apellidos y nombre.
- Prueba de agenda vacía que verifique exactamente `200` y `[]`.
- Prueba de persistencia o integración que confirme que las personas registradas por HU-01 aparecen en el listado.
- Prueba de interfaz o integración que confirme el mensaje de agenda vacía y la actualización posterior al registro.
- Prueba de error de acceso a datos que confirme un código controlado, ausencia de trazas y mensaje de interfaz adecuado.
- Ejecutar `pytest` y revisar la conformidad con `docs/architecture.md`.

### Alternativas consideradas

- Ordenar en JavaScript: descartado porque la ordenación pertenece al resultado del caso de uso y no debe convertirse en regla de negocio de la interfaz.
- Devolver todos los campos de Persona: descartado porque HU-02 solicita solo ID, nombre y apellidos como información básica.
- Añadir paginación o filtros: descartado porque están fuera del alcance aprobado.
- Acceder a SQLite desde el endpoint o la interfaz: descartado porque viola la arquitectura.

## Risks / Trade-offs

- **[Riesgo]** La ordenación puede variar si se define de forma distinta entre capas. **Mitigación:** establecerla en la consulta de persistencia y cubrir apellidos iguales con una prueba de desempate por nombre.
- **[Riesgo]** Una actualización incompleta tras el registro puede dejar la interfaz desactualizada. **Mitigación:** reutilizar `GET /api/personas` tras una respuesta exitosa y probar el flujo de integración.
- **[Riesgo]** Un fallo de SQLite podría exponer detalles internos. **Mitigación:** traducir la excepción en la API a una respuesta controlada y mostrar en la interfaz un mensaje genérico.