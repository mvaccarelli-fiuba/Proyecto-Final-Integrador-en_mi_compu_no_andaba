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
-- Platos del menú
-- -------------------------------------------------------------
CREATE TABLE plato (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0),
    imagen_url VARCHAR(255),
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    es_vegetariano BOOLEAN NOT NULL DEFAULT FALSE,
    es_vegano BOOLEAN NOT NULL DEFAULT FALSE,
    sin_gluten BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
