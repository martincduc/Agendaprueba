## Context

HU-01 añade el alta de la entidad Persona al primer incremento de AGENDA. La solución debe respetar la arquitectura en capas de `docs/architecture.md`, usar únicamente tecnologías aprobadas y mantener el SQL en `app/database.py`. La motivación y el alcance funcional están en `proposal.md`; los contratos observables están en `specs/registrar-persona/spec.md`.

## Goals / Non-Goals

**Goals:**

- Implementar el flujo de alta con validaciones de entrada y errores HTTP controlados.
- Conservar cada persona en SQLite con un identificador generado por el sistema.
- Mantener la interfaz web separada de la API y de la persistencia.
- Cubrir HU-01 con pruebas automatizadas de éxito, validación, duplicados y persistencia.

**Non-Goals:**

- Añadir autenticación, autorización, roles, búsqueda, filtros, paginación, edición, eliminación, importación o exportación.
- Cambiar `docs/architecture.md` o introducir nuevas tecnologías, dependencias o capas.

## Decisions

### Participación de las capas

- **Interfaz:** `app/static/index.html` mostrará el formulario de alta, enviará JSON a `POST /api/personas` y presentará la respuesta o los errores. No accederá a SQLite ni implementará reglas de negocio.
- **API:** `app/main.py` expondrá `POST /api/personas`, recibirá y validará la estructura de la petición, invocará el servicio y construirá respuestas `201` o `422`. No contendrá SQL.
- **Servicios:** `app/services/persona_service.py` coordinará el caso de uso, las reglas de negocio que no sean validación estructural y el repositorio. No dependerá de la interfaz.
- **Repositorios:** `app/repositories/persona_repository.py` traducirá el caso de uso a operaciones de almacenamiento y devolverá la persona creada. No contendrá sentencias SQL; delegará el acceso a persistencia.
- **Persistencia:** `app/database.py` gestionará conexiones, esquema y sentencias SQL mediante `sqlite3`, incluyendo la generación o recuperación del identificador y la inserción de los campos de Persona. Los datos vivirán en SQLite para sobrevivir a reinicios.

### Modelo y validación

Se representará Persona con `id`, `nombre`, `apellidos`, `fecha_de_nacimiento`, `correo_electronico`, `telefono`, `direccion`, `categoria` y `comentarios`, usando los nombres de proyecto que se concreten al implementar. Los campos obligatorios y opcionales, la fecha, el correo, la categoría y los comentarios seguirán exactamente la especificación. No se añadirá una restricción de unicidad sobre los datos de Persona.

La validación de forma se declarará en el esquema de entrada de la API y las reglas que requieran contexto, como que la fecha no sea futura, se comprobarán antes de persistir. El rechazo de HTML se hará como validación de entrada; los comentarios no se renderizarán como HTML en la interfaz.

### Ficheros afectados

- Crear o modificar `app/main.py`, `app/database.py`, `app/services/persona_service.py`, `app/repositories/persona_repository.py`, los esquemas o modelos de Persona dentro de `app/schemas/` y `app/models/`, `app/static/index.html` y `tests/test_agenda.py`.
- Mantener la organización prevista por la arquitectura y no concentrar la funcionalidad en un único fichero.

### Estrategia de pruebas

- Pruebas de API para registro completo, registro mínimo y respuesta `201` con identificador.
- Pruebas de rechazo `422` para obligatorios ausentes, fecha inválida o futura, correo inválido, categoría no permitida y comentarios con HTML o de más de 500 caracteres.
- Prueba de duplicados para comprobar que se crean dos identificadores distintos.
- Prueba de persistencia usando una base SQLite de pruebas y reinicialización de la aplicación.
- Prueba de interfaz o integración suficiente para verificar que el formulario usa la API, sin acceso directo a SQLite.
- Ejecutar `pytest` y revisar la conformidad con `docs/architecture.md`.

### Alternativas consideradas

- Acceder a SQLite desde `app/main.py`: descartado porque viola la separación de capas.
- Permitir SQL en el repositorio: descartado porque la configuración exige que las sentencias estén únicamente en `app/database.py`.
- Añadir una librería de validación o un framework de interfaz: descartado porque no están aprobados y no son necesarios para HU-01.

## Risks / Trade-offs

- **[Riesgo]** La detección de HTML puede rechazar texto que contenga símbolos usados de forma literal. **Mitigación:** definir y probar una regla consistente de marcado HTML antes de implementar, manteniendo comentarios como texto plano.
- **[Riesgo]** Las pruebas de fecha dependen del día actual. **Mitigación:** comparar con la fecha actual de forma determinista en las pruebas y cubrir el límite de la fecha de hoy.
- **[Riesgo]** El esquema actual del repositorio puede evolucionar durante el primer incremento. **Mitigación:** centralizar la inicialización y las sentencias SQL en `app/database.py` y probar la persistencia con una base aislada.