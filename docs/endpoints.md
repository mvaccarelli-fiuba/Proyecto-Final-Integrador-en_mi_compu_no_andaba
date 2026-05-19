# API REST — Crusty Crab

**Grupo 20 — en_mi_compu_andaba**
Entregable hito 20/05 — Listado de endpoints

---

## Convenciones

- Todas las respuestas son JSON.
- Errores: `{ "error": "<mensaje>", "code": "<slug>" }` con códigos HTTP coherentes (400, 401, 403, 404, 409, 422, 500).
- Autenticación admin: `Authorization: Bearer <jwt>` o cookie de sesión (a decidir en implementación).
- Endpoints marcados con 🔒 requieren admin autenticado. Los demás son públicos.
- Endpoints marcados con 🎫 usan el `token` de la reserva como autorización (el que va en el QR / link del email).

---

## 1. Autenticación admin

| Método | Path              | Auth | Descripción                          |
|--------|-------------------|------|--------------------------------------|
| POST   | `/api/admin/login`  | —    | Login del administrador              |
| POST   | `/api/admin/logout` | 🔒   | Cierra la sesión                     |
| GET    | `/api/admin/me`     | 🔒   | Devuelve datos del admin logueado    |

**POST `/api/admin/login`**
```json
// request
{ "email": "admin@crustycrab.com", "password": "admin1234" }
// response 200
{ "token": "<jwt>", "admin": { "id": 1, "nombre": "Mr. Krabs", "email": "..." } }
```

---

## 2. Menú (platos)

| Método | Path                       | Auth | Descripción                                |
|--------|----------------------------|------|--------------------------------------------|
| GET    | `/api/platos`              | —    | Lista todos los platos disponibles         |
| GET    | `/api/platos/:id`          | —    | Detalle de un plato                        |
| GET    | `/api/categorias`          | —    | Lista de categorías del menú               |
| GET    | `/api/restricciones`       | —    | Catálogo de restricciones alimenticias     |
| POST   | `/api/admin/platos`        | 🔒   | Crear plato                                |
| PUT    | `/api/admin/platos/:id`    | 🔒   | Editar plato                               |
| DELETE | `/api/admin/platos/:id`    | 🔒   | Eliminar plato                             |
| POST   | `/api/admin/platos/:id/imagen` | 🔒 | Subir imagen del plato (multipart)        |

**GET `/api/platos`** — query params opcionales: `categoria_id`, `restriccion_id`
```json
// response 200
[
  {
    "id": 1,
    "nombre": "Krabby Patty",
    "descripcion": "La hamburguesa secreta de la casa.",
    "precio": 5500.00,
    "imagen_url": "/static/platos/1.jpg",
    "categoria": { "id": 1, "nombre": "Hamburguesas" },
    "restricciones": []
  }
]
```

**POST `/api/admin/platos`**
```json
// request
{
  "nombre": "Krabby Patty",
  "descripcion": "...",
  "precio": 5500.00,
  "categoria_id": 1,
  "restriccion_ids": [1, 3]
}
// response 201 → mismo formato que GET
```

---

## 3. Servicios extras

| Método | Path                          | Auth | Descripción                     |
|--------|-------------------------------|------|---------------------------------|
| GET    | `/api/servicios`              | —    | Lista de servicios activos      |
| POST   | `/api/admin/servicios`        | 🔒   | Crear servicio                  |
| PUT    | `/api/admin/servicios/:id`    | 🔒   | Editar servicio                 |
| DELETE | `/api/admin/servicios/:id`    | 🔒   | Eliminar servicio               |

---

## 4. Mesas (sólo admin)

| Método | Path                     | Auth | Descripción          |
|--------|--------------------------|------|----------------------|
| GET    | `/api/admin/mesas`       | 🔒   | Lista todas las mesas|
| POST   | `/api/admin/mesas`       | 🔒   | Crear mesa           |
| PUT    | `/api/admin/mesas/:id`   | 🔒   | Editar mesa          |
| DELETE | `/api/admin/mesas/:id`   | 🔒   | Dar de baja mesa     |

```json
// POST /api/admin/mesas
{ "numero": 7, "capacidad": 4 }
```

---

## 5. Reservas

### Flujo público

| Método | Path                                  | Auth | Descripción                                                |
|--------|---------------------------------------|------|------------------------------------------------------------|
| GET    | `/api/disponibilidad`                 | —    | Slots disponibles para una fecha + cantidad de personas    |
| POST   | `/api/reservas`                       | —    | Crear reserva (asigna mesa automáticamente)                |
| GET    | `/api/reservas/:token`                | 🎫   | Consultar reserva por su token (el del QR)                 |
| PUT    | `/api/reservas/:token/cancelar`       | 🎫   | Cancelar reserva (link del email)                          |

**GET `/api/disponibilidad?fecha=2026-05-30&personas=4`**
```json
// response 200
{
  "fecha": "2026-05-30",
  "personas": 4,
  "slots": [
    { "hora_inicio": "20:00", "disponible": true },
    { "hora_inicio": "21:00", "disponible": false },
    { "hora_inicio": "22:00", "disponible": true }
  ]
}
```

**POST `/api/reservas`**
```json
// request
{
  "cliente_nombre": "Bob Esponja",
  "cliente_email": "bob@fondodebikini.com",
  "fecha": "2026-05-30",
  "hora_inicio": "20:00",
  "cantidad_personas": 4
}
// response 201
{
  "token": "f7c1b8a2-...",
  "estado": "confirmada",
  "mesa": { "numero": 3, "capacidad": 4 },
  "fecha": "2026-05-30",
  "hora_inicio": "20:00",
  "qr_url": "/api/reservas/f7c1b8a2-.../qr"
}
// response 409 si no hay mesa para ese slot/cantidad
```

**GET `/api/reservas/:token/qr`** — devuelve la imagen PNG del QR (también se adjunta por mail).

### Admin

| Método | Path                                     | Auth | Descripción                                  |
|--------|------------------------------------------|------|----------------------------------------------|
| GET    | `/api/admin/reservas`                    | 🔒   | Listado con filtros (fecha, estado, email)   |
| POST   | `/api/admin/reservas/consumir`           | 🔒   | Validar QR y marcar reserva como consumida   |

**POST `/api/admin/reservas/consumir`**
```json
// request
{ "token": "f7c1b8a2-..." }
// response 200
{ "id": 17, "estado": "consumida", "consumido_en": "2026-05-30T20:05:00" }
// errores: 404 token inexistente, 409 ya consumida/cancelada/expirada
```

**GET `/api/admin/reservas`** — query params: `desde`, `hasta`, `estado`, `email`, `page`, `page_size`.

---

## 6. Reseñas

| Método | Path                              | Auth | Descripción                                       |
|--------|-----------------------------------|------|---------------------------------------------------|
| GET    | `/api/resenas`                    | —    | Lista de reseñas publicadas                       |
| POST   | `/api/resenas`                    | 🎫   | Publicar reseña (requiere token de reserva consumida) |
| DELETE | `/api/admin/resenas/:id`          | 🔒   | Baja lógica de reseña inapropiada                 |

**POST `/api/resenas`**
```json
// request
{
  "token_reserva": "f7c1b8a2-...",
  "puntaje": 5,
  "comentario": "Las mejores hamburguesas del fondo del mar.",
  "autor": "Bob Esponja"
}
// response 201
{ "id": 42, "puntaje": 5, "comentario": "...", "autor": "Bob Esponja", "creado_en": "..." }
// errores: 403 si la reserva no está consumida, 409 si ya hay reseña para esa reserva
```

---

## 7. Dashboard / Estadísticas (admin)

| Método | Path                                     | Auth | Descripción                                       |
|--------|------------------------------------------|------|---------------------------------------------------|
| GET    | `/api/admin/stats/reservas`              | 🔒   | Reservas agregadas por período                    |
| GET    | `/api/admin/stats/cancelaciones`         | 🔒   | Cancelaciones + top emails con más cancelaciones  |
| GET    | `/api/admin/stats/ocupacion`             | 🔒   | Ocupación promedio del local por período          |

Query params comunes: `desde`, `hasta`, `granularidad` (`dia`, `semana`, `mes`).

---

## 8. Informes en PDF (admin)

| Método | Path                                  | Auth | Descripción                                |
|--------|---------------------------------------|------|--------------------------------------------|
| GET    | `/api/admin/informes/reservas.pdf`    | 🔒   | PDF con listado de reservas (con filtros)  |
| GET    | `/api/admin/informes/estadisticas.pdf`| 🔒   | PDF con estadísticas del período           |
| GET    | `/api/admin/informes/menu.pdf`        | 🔒   | PDF del menú completo                      |

Responden `Content-Type: application/pdf`. Aceptan los mismos filtros que los listados correspondientes.

---

## 9. Log de actividad (admin)

| Método | Path                  | Auth | Descripción                                |
|--------|-----------------------|------|--------------------------------------------|
| GET    | `/api/admin/logs`     | 🔒   | Listado de eventos del sistema (paginado)  |

---

## Resumen de tablas usadas

| Tabla                      | Usada por                                            |
|----------------------------|------------------------------------------------------|
| `admin`                    | login, logs                                          |
| `categoria_plato`          | menú                                                 |
| `plato`                    | menú                                                 |
| `restriccion_alimenticia`  | menú                                                 |
| `plato_restriccion`        | menú                                                 |
| `servicio_extra`           | landing + admin                                      |
| `mesa`                     | reservas (asignación automática) + admin             |
| `reserva`                  | reservas, dashboard, informes                        |
| `resena`                   | reseñas, landing                                     |
| `log_actividad`            | auditoría                                            |
