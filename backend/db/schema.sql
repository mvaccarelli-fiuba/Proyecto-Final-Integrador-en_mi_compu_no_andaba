CREATE DATABASE IF NOT EXISTS krusty_krab;
USE krusty_krab;

CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasenia VARCHAR(150) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(100) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE platos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    vegano BOOLEAN NOT NULL DEFAULT FALSE
    vegetariano BOOLEAN NOT NULL DEFAULT FALSE
    gluten BOOLEAN NOT NULL DEFAULT FALSE,
    imagen_url VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE servicios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    icono_url VARCHAR(150),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE mesas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero INT  NOT NULL UNIQUE,
    capacidad INT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mesa_id INT NOT NULL,
    usuario_nombre VARCHAR(100) NOT NULL,
    usuario_email VARCHAR(150) NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    cantidad_personas INT NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT "pendiente",
    token_unico VARCHAR(64) NOT NULL UNIQUE,
    token_resenia VARCHAR(64) UNIQUE,
    comentarios TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(mesa_id) REFERENCES mesas(id)
);

CREATE TABLE resenia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    estrellas INT NOT NULL,
    comentarios TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(reserva_id) REFERENCES reservas(id)
);
