CREATE DATABASE krusty krab;
USE krusty krab;

CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasenia VARCHAR(150) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(100) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE restricciones_alimenticias (
    id INT PRYMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE platos (
    id INT PRYMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    imagen_url VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE platos_restricciones (
    plato_id INT NOT NULL,
    restriccion_id INT NOT NULL,
    PRYMARY KEY(plato_id, restriccion_id),
    FOREIGN KEY(plato_id) REFERENCES platos(id) ON DELETE CASCADE,
    FOREIGN KEY(restriccion_id) REFERENCES restricciones_alimenticias(id) ON DELETE CASCADE
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
    comentarios TEXT
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(mesa_id) REFERENCES mesas(id)
);

CREATE TABLE resenia (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reserva_id INT NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    estrellas INT NOT NULL, --Del 0 al 5
    comentarios TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
