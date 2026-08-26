## Purpose

Esta capacidad permite al propietario de la agenda registrar personas nuevas con sus datos de contacto y biográficos, para conservarlos y consultarlos posteriormente.

## ADDED Requirements

### Requirement: Registrar una persona válida

El sistema SHALL permitir al propietario de la agenda registrar una persona mediante `POST /api/personas`. El nombre y los apellidos SHALL ser obligatorios y no estar vacíos. La fecha de nacimiento, el correo electrónico, el teléfono, la dirección, la categoría y los comentarios SHALL ser opcionales. La categoría, cuando se proporcione, SHALL ser exactamente `Familia`, `Trabajo`, `Amigos` u `Otro`. Los comentarios SHALL ser texto plano de como máximo 500 caracteres.

#### Scenario: Registro con todos los datos válidos

- **GIVEN** que el propietario de la agenda proporciona nombre, apellidos, fecha de nacimiento válida, correo válido, teléfono, dirección, una categoría permitida y comentarios de texto plano
- **WHEN** envía una petición `POST /api/personas`
- **THEN** el sistema registra la persona, genera un identificador único y responde con código `201` y la persona registrada, incluido su identificador

#### Scenario: Registro solo con campos obligatorios

- **GIVEN** que el propietario de la agenda proporciona únicamente nombre y apellidos no vacíos
- **WHEN** envía una petición `POST /api/personas`
- **THEN** el sistema registra la persona con los demás campos opcionales vacíos o ausentes y responde con código `201` y un identificador único

#### Scenario: Registro de una persona duplicada

- **GIVEN** que ya existe una persona con los mismos datos
- **WHEN** el propietario de la agenda registra otra persona con esos datos
- **THEN** el sistema registra ambas personas con identificadores distintos y responde con código `201`

### Requirement: Validar los datos de una persona

El sistema SHALL rechazar una petición de registro que incumpla una validación y SHALL responder con código `422` sin persistir la persona ni exponer trazas internas. La fecha de nacimiento SHALL usar exactamente el formato `AAAA-MM-DD` y no ser posterior a la fecha actual. El correo electrónico, si se proporciona, SHALL tener un formato válido. El contenido de comentarios SHALL rechazar HTML.

#### Scenario: Falta un campo obligatorio

- **GIVEN** que falta el nombre o los apellidos, o uno de ellos está vacío
- **WHEN** se envía una petición `POST /api/personas`
- **THEN** el sistema responde con código `422` indicando el campo inválido y no registra la persona

#### Scenario: Nombre o apellidos con solo espacios en blanco

- **GIVEN** que el nombre o los apellidos están compuestos únicamente por espacios en blanco
- **WHEN** se envía una petición `POST /api/personas`
- **THEN** el sistema trata el campo como vacío y responde con código `422` indicando el campo obligatorio faltante, sin registrar la persona

#### Scenario: Fecha de nacimiento con formato incorrecto o futura

- **GIVEN** que la fecha de nacimiento no cumple `AAAA-MM-DD` o es posterior a la fecha actual
- **WHEN** se envía una petición `POST /api/personas`
- **THEN** el sistema responde con código `422` y no registra la persona

#### Scenario: Correo electrónico inválido

- **GIVEN** que se proporciona un correo electrónico con formato inválido
- **WHEN** se envía una petición `POST /api/personas`
- **THEN** el sistema responde con código `422` y no registra la persona

#### Scenario: Categoría no permitida

- **GIVEN** que se proporciona una categoría distinta de `Familia`, `Trabajo`, `Amigos` u `Otro`
- **WHEN** se envía una petición `POST /api/personas`
- **THEN** el sistema responde con código `422` y no registra la persona

#### Scenario: Comentarios demasiado largos o con HTML

- **GIVEN** que los comentarios superan 500 caracteres o contienen marcado HTML
- **WHEN** se envía una petición `POST /api/personas`
- **THEN** el sistema responde con código `422` y no registra la persona

### Requirement: Conservar una persona registrada

El sistema SHALL conservar de forma persistente los datos y el identificador de una persona registrada correctamente, de modo que permanezcan disponibles después de reiniciar la aplicación.

#### Scenario: Datos disponibles después de reiniciar

- **GIVEN** que una persona se ha registrado correctamente
- **WHEN** la aplicación se reinicia y se consulta el almacenamiento mediante las capacidades disponibles de la agenda
- **THEN** los datos registrados y su identificador permanecen conservados