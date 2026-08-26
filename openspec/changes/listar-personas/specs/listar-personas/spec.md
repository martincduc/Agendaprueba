## Purpose

Esta capacidad permite al propietario de la agenda consultar todas las personas registradas y acceder a su información básica de forma ordenada, incluida una respuesta clara cuando la agenda está vacía.

## ADDED Requirements

### Requirement: Listar la información básica de las personas

El sistema SHALL permitir al propietario de la agenda consultar las personas mediante `GET /api/personas`. La respuesta SHALL tener código HTTP `200` y SHALL contener una lista con una entrada por cada persona registrada. Cada entrada SHALL incluir únicamente el identificador, el nombre y los apellidos de la persona.

#### Scenario: Listado con personas registradas

- **GIVEN** que existen personas registradas en la agenda
- **WHEN** el propietario de la agenda solicita `GET /api/personas`
- **THEN** el sistema responde con código `200` y una lista que contiene el ID, nombre y apellidos de cada persona

#### Scenario: Agenda vacía

- **GIVEN** que no existen personas registradas en la agenda
- **WHEN** el propietario de la agenda solicita `GET /api/personas`
- **THEN** el sistema responde con código `200` y el cuerpo `[]`

### Requirement: Ordenar el listado

El sistema SHALL devolver todas las personas sin paginación, ordenadas primero por apellidos en orden ascendente y después por nombre en orden ascendente. La ordenación SHALL aplicarse al resultado completo, sin omitir personas.

#### Scenario: Personas devueltas en orden por apellidos y nombre

- **GIVEN** que existen personas con apellidos o nombres en un orden diferente al de sus datos registrados
- **WHEN** el propietario de la agenda solicita `GET /api/personas`
- **THEN** el sistema devuelve todas las personas ordenadas ascendentemente por apellidos y, en caso de empate, por nombre

### Requirement: Mostrar y actualizar el listado en la interfaz

La interfaz SHALL mostrar el ID, nombre y apellidos de las personas obtenidas desde `GET /api/personas`. Cuando la respuesta esté vacía, SHALL mostrar un mensaje indicando que la agenda no contiene personas. Después de registrar correctamente una persona, SHALL actualizar el listado para incluirla.

#### Scenario: Mostrar mensaje para una agenda vacía

- **GIVEN** que `GET /api/personas` responde correctamente con `[]`
- **WHEN** el propietario de la agenda visualiza la sección de personas
- **THEN** la interfaz muestra un mensaje de agenda vacía y no presenta filas de personas

#### Scenario: Actualizar el listado después de registrar

- **GIVEN** que el propietario de la agenda registra correctamente una persona desde la interfaz
- **WHEN** el registro finaliza con éxito
- **THEN** la interfaz vuelve a consultar o actualiza el listado mediante la API y muestra la persona registrada con su ID, nombre y apellidos

### Requirement: Tratar los errores del listado de forma controlada

Si ocurre un error al consultar las personas, el sistema SHALL responder con un código HTTP coherente con el error, SHALL evitar exponer trazas internas y la interfaz SHALL mostrar un mensaje comprensible sin presentar datos como si la consulta hubiera sido correcta.

#### Scenario: Error controlado al consultar personas

- **GIVEN** que la consulta de personas no puede completarse
- **WHEN** el propietario de la agenda solicita `GET /api/personas`
- **THEN** el sistema devuelve una respuesta de error controlada sin trazas internas y la interfaz informa de que no se ha podido cargar el listado