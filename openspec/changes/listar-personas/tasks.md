## 1. Persistencia y repositorio

- [ ] 1.1 Implementar en `app/database.py` la consulta que obtiene ID, nombre y apellidos de todas las personas.
- [ ] 1.2 Aplicar en `app/database.py` la ordenación ascendente por apellidos y nombre, sin paginación ni límite de resultados.
- [ ] 1.3 Crear o ampliar `app/repositories/persona_repository.py` para devolver la colección completa y una colección vacía cuando no existan personas, sin incluir SQL.

## 2. Servicio y API

- [ ] 2.1 Crear o ampliar `app/services/persona_service.py` con el caso de uso de consulta del listado, sin dependencia de la interfaz.
- [ ] 2.2 Implementar `GET /api/personas` en `app/main.py`, devolviendo `200` con una lista JSON y solo ID, nombre y apellidos por persona.
- [ ] 2.3 Traducir los fallos conocidos de consulta a respuestas HTTP controladas, sin SQL ni trazas internas en `app/main.py`.

## 3. Interfaz web

- [ ] 3.1 Actualizar `app/static/index.html` para solicitar `GET /api/personas` y mostrar ID, nombre y apellidos en el listado.
- [ ] 3.2 Mostrar un mensaje específico cuando la API devuelva `200` con `[]`, sin presentar filas vacías.
- [ ] 3.3 Actualizar el listado después de un registro exitoso de HU-01 mediante la API y mostrar errores de carga con un mensaje comprensible.
- [ ] 3.4 Verificar que la interfaz no accede directamente a SQLite ni implementa reglas de negocio en JavaScript.

## 4. Pruebas automatizadas

- [ ] 4.1 Añadir pruebas pytest del listado con varias personas, verificando `200`, inclusión de todas y únicamente los campos básicos.
- [ ] 4.2 Añadir una prueba pytest de agenda vacía que verifique exactamente `200` y `[]`.
- [ ] 4.3 Añadir una prueba pytest de ordenación por apellidos y, en caso de empate, por nombre.
- [ ] 4.4 Añadir una prueba de integración del flujo HU-01/HU-02 que verifique que el listado se actualiza después de registrar una persona.
- [ ] 4.5 Añadir pruebas de interfaz o integración para el mensaje de agenda vacía y el mensaje de error controlado.
- [ ] 4.6 Añadir una prueba de fallo de persistencia que verifique el código de error controlado y la ausencia de trazas internas.

## 5. Verificación final

- [ ] 5.1 Ejecutar `pytest` y corregir únicamente los fallos relacionados con HU-02.
- [ ] 5.2 Revisar que todas las personas se devuelven sin paginación y que no se han añadido búsqueda, filtros u ordenación configurable.
- [ ] 5.3 Revisar que las sentencias SQL están únicamente en `app/database.py`, que las capas permanecen separadas y que no se añadieron dependencias.
- [ ] 5.4 Comprobar la conformidad final con `docs/architecture.md` y con todos los escenarios de `specs/listar-personas/spec.md`.