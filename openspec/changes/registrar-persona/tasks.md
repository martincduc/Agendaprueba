## 1. Modelo y persistencia

- [x] 1.1 Definir el modelo y los esquemas de entrada y salida de Persona con los campos de HU-01, diferenciando obligatorios y opcionales.
- [x] 1.2 Implementar en `app/database.py` la inicialización del esquema SQLite y la tabla de personas con identificador generado por el sistema.
- [x] 1.3 Implementar en `app/database.py` la operación de inserción de una persona, conservando todos sus campos y permitiendo duplicados.

## 2. Repositorio y servicio

- [x] 2.1 Crear `app/repositories/persona_repository.py` para coordinar la inserción y recuperación de la persona creada sin incluir sentencias SQL.
- [x] 2.2 Crear `app/services/persona_service.py` para coordinar el caso de uso de registro y las reglas de negocio que no correspondan a la validación estructural.

## 3. API FastAPI

- [x] 3.1 Añadir `POST /api/personas` en `app/main.py`, delegando en el servicio y devolviendo `201` con la persona y su identificador.
- [x] 3.2 Validar nombre y apellidos obligatorios, fecha `AAAA-MM-DD` no futura, correo válido, categoría permitida y comentarios de texto plano de hasta 500 caracteres.
- [x] 3.3 Devolver errores `422` controlados para entradas inválidas, sin persistirlas ni exponer trazas internas.

## 4. Interfaz web

- [x] 4.1 Añadir en `app/static/index.html` el formulario de alta con los campos de Persona y las opciones fijas de categoría.
- [x] 4.2 Conectar el formulario exclusivamente con `POST /api/personas` y mostrar el resultado o los errores de validación como texto, sin acceso a SQLite ni reglas de negocio en JavaScript.

## 5. Pruebas automatizadas

- [x] 5.1 Añadir pruebas pytest de registro completo y registro mínimo, verificando `201`, los datos devueltos y el identificador generado.
- [x] 5.2 Añadir pruebas pytest de fecha inválida o futura, correo inválido, categoría no permitida y nombre o apellidos ausentes o vacíos, verificando `422` y ausencia de persistencia.
- [x] 5.3 Añadir pruebas pytest de comentarios con HTML y de más de 500 caracteres, verificando `422` y ausencia de persistencia.
- [x] 5.4 Añadir una prueba pytest de duplicados que verifique dos registros válidos con identificadores distintos.
- [x] 5.5 Añadir una prueba pytest de persistencia con una base SQLite aislada y reinicialización de la aplicación.
- [x] 5.6 Añadir una comprobación de integración de la interfaz que verifique que el formulario usa la API y no accede directamente a SQLite.

## 6. Verificación final

- [x] 6.1 Ejecutar `pytest` y corregir únicamente los fallos relacionados con HU-01.
- [x] 6.2 Revisar que las sentencias SQL están únicamente en `app/database.py`, que las capas permanecen separadas y que no se añadieron dependencias.
- [x] 6.3 Comprobar la conformidad final con `docs/architecture.md` y con todos los escenarios de `specs/registrar-persona/spec.md`.