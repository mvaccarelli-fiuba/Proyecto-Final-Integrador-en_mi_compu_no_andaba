# API REST — Crusty Crab

**Grupo 20 — en_mi_compu_andaba**
Listado consolidado de endpoints del backend.

---

## Convenciones

- Todas las respuestas son JSON, salvo cuando son 204 No Content (body vacío) o cuando devuelven un PDF.
- Errores con el formato:
  ```json
  {
    "errors": [
      { "code": "404", "message": "Not Found", "level": "error", "description": "..." }
    ]
  }
  ```
- Autenticación admin: `Authorization: Bearer <jwt>`.
- Endpoints marcados con 🔒 requieren admin autenticado.
- Endpoints marcados con 🎫 usan el `token` de la reserva como autorización (el que va en el QR / link del email).

---

## 1. Autenticación admin

| Método | Path              | Auth | Descripción                          |
|--------|-------------------|------|--------------------------------------|
| POST   | `/auth/login`     | —    | Login del administrador              |
| POST   | `/auth/logout`    | 🔒   | Cierra la sesión                     |
| GET    | `/auth/me`        | 🔒   | Devuelve datos del admin logueado    |

**POST `/auth/login`**
```json
// request
{ "email": "admin@crustycrab.com", "password": "admin1234" }
// response 200
{ "token": "<jwt>", "admin": { "id": 1, "nombre": "Mr. Krabs", "email": "..." } }
```

---

## 2. Menú (platos)

| Método | Path                          | Auth | Descripción                                |
|--------|-------------------------------|------|--------------------------------------------|
| GET    | `/platos`                     | —    | Lista todos los platos disponibles         |
| GET    | `/platos/<id>`                | —    | Detalle de un plato                        |
| GET    | `/categorias`                 | —    | Lista de categorías del menú               |
| POST   | `/admin/platos`               | 🔒   | Crear plato                                |
| PUT    | `/admin/platos/<id>`          | 🔒   | Editar plato                               |
| DELETE | `/admin/platos/<id>`          | 🔒   | Eliminar plato                             |
| POST   | `/admin/platos/<id>/imagen`   | 🔒   | Subir imagen del plato (multipart)         |

**GET `/platos`** — query params opcionales:
- `restriccion` (`vegano` | `vegetariano` | `gluten`): filtra platos por restricción alimentaria
- `categoria_id` (int): filtra por categoría
- `es_vegetariano` (true/false): filtra platos vegetarianos
- `es_vegano` (true/false): filtra platos veganos
- `sin_gluten` (true/false): filtra platos sin gluten

```json
// response 200
[
  {
    "id": 3,
    "nombre": "Veggie Patty",
    "descripcion": "Versión vegetariana con medallón de lentejas.",
    "precio": 5200.0,
    "imagen_url": "/static/platos/3.jpg",
    "disponible": true,
    "created_at": "2026-05-19T03:25:30",
    "categoria": {
      "id": 1,
      "nombre": "Hamburguesas"
    },
    "restricciones": {
      "es_vegetariano": true,
      "es_vegano": false,
      "sin_gluten": false
    }
  }
]
// response 204 si no hay platos
```

**POST `/admin/platos`**
```json
// request
{
  "nombre": "Krabby Patty",
  "descripcion": "...",
  "precio": 5500.0,
  "categoria_id": 1,
  "es_vegetariano": false,
  "es_vegano": false,
  "sin_gluten": false
}
// response 201 → mismo formato que GET
```

---

## 3. Servicios extras

| Método | Path                          | Auth | Descripción                     |
|--------|-------------------------------|------|---------------------------------|
| GET    | `/servicios`                  | —    | Lista de servicios activos      |
| POST   | `/admin/servicios`            | 🔒   | Crear servicio                  |
| PUT    | `/admin/servicios/<id>`       | 🔒   | Editar servicio                 |
| DELETE | `/admin/servicios/<id>`       | 🔒   | Eliminar servicio               |

---

## 4. Mesas (sólo admin)

| Método | Path                  | Auth | Descripción          |
|--------|-----------------------|------|----------------------|
| GET    | `/admin/mesas`        | 🔒   | Lista todas las mesas|
| POST   | `/admin/mesas`        | 🔒   | Crear mesa           |
| PUT    | `/admin/mesas/<id>`   | 🔒   | Editar mesa          |
| DELETE | `/admin/mesas/<id>`   | 🔒   | Dar de baja mesa     |

```json
// POST /admin/mesas
{ "numero": 7, "capacidad": 4 }
```

---

## 5. Reservas

### Flujo público

| Método | Path                              | Auth | Descripción                                                |
|--------|-----------------------------------|------|------------------------------------------------------------|
| GET    | `/disponibilidad`                 | —    | Slots disponibles para una fecha + cantidad de personas    |
| POST   | `/reservas`                       | —    | Crear reserva (asigna mesa automáticamente)                |
| GET    | `/reservas/<token>`               | 🎫   | Consultar reserva por su token (el del QR)                 |
| PUT    | `/reservas/<token>/cancelar`      | 🎫   | Cancelar reserva (link del email)                          |

**GET `/disponibilidad?fecha=2026-05-30&personas=4`**
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

**POST `/reservas`**
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
  "qr_url": "/reservas/f7c1b8a2-.../qr"
}
// response 409 si no hay mesa para ese slot/cantidad
```

**GET `/reservas/<token>/qr`** — devuelve la imagen PNG del QR (también se adjunta por mail).

### Admin

| Método | Path                                | Auth | Descripción                                  |
|--------|-------------------------------------|------|----------------------------------------------|
| GET    | `/admin/reservas`                   | 🔒   | Listado con filtros (fecha, estado, email)   |
| POST   | `/admin/reservas/consumir`          | 🔒   | Validar QR y marcar reserva como consumida   |

**POST `/admin/reservas/consumir`**
```json
// request
{ "token": "f7c1b8a2-..." }
// response 200
{ "id": 17, "estado": "consumida", "consumido_en": "2026-05-30T20:05:00" }
// errores: 404 token inexistente, 409 ya consumida/cancelada/expirada
```

**GET `/admin/reservas`** — query params: `desde`, `hasta`, `estado`, `email`.

---

## 6. Reseñas

| Método | Path                          | Auth | Descripción                                       |
|--------|-------------------------------|------|---------------------------------------------------|
| GET    | `/resenas`                    | —    | Lista de reseñas publicadas                       |
| POST   | `/resenas`                    | 🎫   | Publicar reseña (requiere token de reserva consumida) |
| DELETE | `/admin/resenas/<id>`         | 🔒   | Baja lógica de reseña inapropiada                 |

**POST `/resenas`**
```json
// request
{
  "token_reserva": "f7c1b8a2-...",
  "puntaje": 5,
  "comentario": "Las mejores hamburguesas del fondo del mar.",
  "autor": "Bob Esponja"
}
// response 201
{ "id": 42, "puntaje": 5, "comentario": "...", "autor": "Bob Esponja", "created_at": "..." }
// errores: 403 si la reserva no está consumida, 409 si ya hay reseña para esa reserva
```

---

## 7. Dashboard / Estadísticas (admin)

| Método | Path                                | Auth | Descripción                                       |
|--------|-------------------------------------|------|---------------------------------------------------|
| GET    | `/admin/stats/reservas`             | 🔒   | Reservas agregadas por período                    |
| GET    | `/admin/stats/cancelaciones`        | 🔒   | Cancelaciones + top emails con más cancelaciones  |
| GET    | `/admin/stats/ocupacion`            | 🔒   | Ocupación promedio del local por período          |

Query params comunes: `desde`, `hasta`, `granularidad` (`dia`, `semana`, `mes`).

---

## 8. Informes en PDF (admin)

| Método | Path                                | Auth | Descripción                                |
|--------|-------------------------------------|------|--------------------------------------------|
| GET    | `/admin/informes/reservas.pdf`      | 🔒   | PDF con listado de reservas (con filtros)  |
| GET    | `/admin/informes/estadisticas.pdf`  | 🔒   | PDF con estadísticas del período           |
| GET    | `/admin/informes/menu.pdf`          | 🔒   | PDF del menú completo                      |

Responden `Content-Type: application/pdf`. Aceptan los mismos filtros que los listados correspondientes.

---

## 9. Log de actividad (admin)

| Método | Path                  | Auth | Descripción                                |
|--------|-----------------------|------|--------------------------------------------|
| GET    | `/admin/logs`         | 🔒   | Listado de eventos del sistema             |

---

## Resumen de tablas usadas

| Tabla              | Usada por                                            |
|--------------------|------------------------------------------------------|
| `admin`            | login, logs                                          |
| `categoria_plato`  | menú                                                 |
| `plato`            | menú (incluye flags de restricciones)                |
| `servicio_extra`   | landing + admin                                      |
| `mesa`             | reservas (asignación automática) + admin             |
| `reserva`          | reservas, dashboard, informes                        |
| `resena`           | reseñas, landing                                     |
| `log_actividad`    | auditoría                                            |
