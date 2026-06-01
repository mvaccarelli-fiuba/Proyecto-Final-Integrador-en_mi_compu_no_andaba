-- =============================================================
-- Crusty Crab - Sitio web gastronómico con reservas
-- Grupo 20 - en_mi_compu_andaba
-- Script de creación de tablas (MySQL 8.0+)
-- =============================================================
DROP DATABASE IF EXISTS crusty_crab;
CREATE DATABASE crusty_crab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE crusty_crab;
-- -------------------------------------------------------------
-- Administradores
-- -------------------------------------------------------------
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR (80) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
-- -------------------------------------------------------------
-- Restricciones alimenticias (catálogo: vegetariano, sin TACC, etc.)
-- -------------------------------------------------------------
CREATE TABLE restriccion_alimenticia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL UNIQUE
);
-- -------------------------------------------------------------
-- Categorías de plato (catálogo: hamburguesas, bebidas, postres, etc.)
-- -------------------------------------------------------------
CREATE TABLE categoria_plato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE
);
-- -------------------------------------------------------------
-- Platos del menú
-- -------------------------------------------------------------
CREATE TABLE plato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    imagen_url VARCHAR(255),
    categoria_id INT NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    es_vegetariano BOOLEAN NOT NULL DEFAULT FALSE,
    es_vegano BOOLEAN NOT NULL DEFAULT FALSE,
    sin_gluten BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categoria_plato(id)
);
-- -------------------------------------------------------------
-- Servicios extras (estacionamiento, wifi, accesibilidad, ...)
-- -------------------------------------------------------------
CREATE TABLE servicio_extra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
-- -------------------------------------------------------------
-- Mesas del local
-- -------------------------------------------------------------
CREATE TABLE mesa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    activa BOOLEAN NOT NULL DEFAULT TRUE
);
-- -------------------------------------------------------------
-- Reservas
-- Una reserva ocupa una mesa en un slot (fecha + hora).
-- Se evita que dos reservas confirmadas pisen la misma mesa
-- en el mismo slot vía índice único.
-- -------------------------------------------------------------
CREATE TABLE reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token CHAR(36) NOT NULL UNIQUE,
    -- UUID, va en el QR
    cliente_nombre VARCHAR(120) NOT NULL,
    cliente_email VARCHAR(120) NOT NULL,
    cantidad_personas INT NOT NULL CHECK (cantidad_personas >= 1),
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    -- slot de 1 hora
    mesa_id INT NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'consumida') NOT NULL DEFAULT 'confirmada',
    -- expirada se calcula: estado='confirmada' AND fecha < CURDATE()
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cancelado_en DATETIME,
    consumido_en DATETIME,
    FOREIGN KEY (mesa_id) REFERENCES mesa(id),
    INDEX idx_reserva_email (cliente_email),
    INDEX idx_reserva_fecha (fecha, hora_inicio)
);
-- Evita doble reserva confirmada para misma mesa+fecha+slot.
CREATE UNIQUE INDEX uniq_mesa_slot_estado ON reserva (mesa_id, fecha, hora_inicio, estado);
-- -------------------------------------------------------------
-- Reseñas
-- Una reseña existe sólo si la reserva fue consumida.
-- El token de reserva oficia de "permiso" para publicar.
-- -------------------------------------------------------------
CREATE TABLE resena (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL UNIQUE,
    -- 1 reseña por reserva
    puntaje TINYINT NOT NULL CHECK (
        puntaje BETWEEN 1 AND 5
    ),
    comentario TEXT,
    autor VARCHAR(120) NOT NULL,
    publicada BOOLEAN NOT NULL DEFAULT TRUE,
    -- baja lógica por admin
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reserva(id)
);
-- -------------------------------------------------------------
-- Log de actividad (requisito del enunciado)
-- -------------------------------------------------------------
CREATE TABLE log_actividad (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT,
    -- NULL si fue acción anónima
    accion VARCHAR(80) NOT NULL,
    -- ej: 'login', 'plato.create', 'reserva.consumir'
    entidad VARCHAR(40),
    -- ej: 'plato', 'reserva'
    entidad_id INT,
    detalle JSON,
    ip VARCHAR(45),
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admin(id),
    INDEX idx_log_fecha (creado_en),
    INDEX idx_log_accion (accion)
);
-- =============================================================
-- Datos de prueba (seed mínimo)
-- =============================================================
-- Admin de prueba. Password: admin1234 (texto plano, TODO: hashear)
INSERT INTO admin (email, password_hash, nombre)
VALUES ('admin@crustycrab.com', 'admin1234', 'Mr. Krabs');
INSERT INTO categoria_plato (nombre)
VALUES ('Hamburguesas'),
    ('Acompañamientos'),
    ('Bebidas'),
    ('Postres');
INSERT INTO plato (
        nombre,
        descripcion,
        precio,
        categoria_id,
        es_vegetariano,
        es_vegano,
        sin_gluten
    )
VALUES (
        'Krabby Patty',
        'La hamburguesa secreta de la casa.',
        5500.00,
        1,
        FALSE,
        FALSE,
        FALSE
    ),
    (
        'Double Krabby',
        'Doble medallón, doble queso.',
        7800.00,
        1,
        FALSE,
        FALSE,
        FALSE
    ),
    (
        'Veggie Patty',
        'Versión vegetariana con medallón de lentejas.',
        5200.00,
        1,
        TRUE,
        FALSE,
        FALSE
    ),
    (
        'Papas Bikini',
        'Papas fritas extra crocantes.',
        2800.00,
        2,
        TRUE,
        TRUE,
        TRUE
    ),
    (
        'Kelp Shake',
        'Malteada de algas.',
        3200.00,
        3,
        TRUE,
        TRUE,
        TRUE
    ),
    (
        'Pie de Coral',
        'Postre de la casa.',
        3600.00,
        4,
        TRUE,
        FALSE,
        FALSE
    );
-- Papas -> Vegano
INSERT INTO servicio_extra (nombre, descripcion)
VALUES (
        'Estacionamiento',
        'Playa de estacionamiento gratuita.'
    ),
    (
        'Accesibilidad',
        'Acceso para personas con movilidad reducida.'
    ),
    (
        'Wifi',
        'Wifi gratis para clientes.'
    ),
    (
        'Pet friendly',
        'Aceptamos mascotas en el patio.'
    );
INSERT INTO mesa (numero, capacidad)
VALUES (1, 2),
    (2, 2),
    (3, 4),
    (4, 4),
    (5, 6),
    (6, 8);
--probamos la reseña con una reserva
INSERT INTO reserva (
        token,
        cliente_nombre,
        cliente_email,
        cantidad_personas,
        fecha,
        hora_inicio,
        mesa_id,
        estado
    )
VALUES (
        'test-token-1',
        'Marina González',
        'marina@test.com',
        2,
        '2026-05-15',
        '20:00',
        1,
        'consumida'
    ),
    (
        'test-token-2',
        'Tomás Parayra',
        'tomas@test.com',
        4,
        '2026-05-14',
        '21:00',
        3,
        'consumida'
    ),
    (
        'test-token-3',
        'Luna Ramos',
        'luna@test.com',
        2,
        '2026-05-13',
        '22:00',
        2,
        'consumida'
    );
-- Ahora las reseñas:
INSERT INTO resena (reserva_id, autor, puntaje, comentario)
VALUES (
        1,
        'Marina González',
        5,
        'Juro que pensé pasar, pero una burger me hará sentir como sirena. La Clásica es un crimen delicioso, ya voy cuatro veces este mes.'
    ),
    (
        2,
        'Tomás Parayra',
        5,
        'Me avisaron que la Extrema picaba pero fui a aguantar. Spoiler: no aguanté, pero volvería igual.'
    ),
    (
        3,
        'Luna Ramos',
        4,
        'Soy vegetariana y siempre termino mirando el menú ajena, hasta que probé la Veggie. Excelente.'
    );