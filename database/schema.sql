CREATE DATABASE IF NOT EXISTS chifa_fusion_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE chifa_fusion_db;

-- =========================================
-- TABLA: CATEGORIAS
-- =========================================

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    estado BOOLEAN NOT NULL DEFAULT TRUE
);

-- =========================================
-- TABLA: PLATOS
-- =========================================

CREATE TABLE IF NOT EXISTS platos (
    id_plato INT AUTO_INCREMENT PRIMARY KEY,
    id_categoria INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    imagen_url VARCHAR(500),
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_platos_categorias
        FOREIGN KEY (id_categoria)
        REFERENCES categorias(id_categoria)
);

-- =========================================
-- TABLA: RESERVAS
-- =========================================

CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(120) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    fecha_reserva DATE NOT NULL,
    hora_reserva TIME NOT NULL,
    numero_personas INT NOT NULL,
    observaciones TEXT,
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- TABLA: MENSAJES DE CONTACTO
-- =========================================

CREATE TABLE IF NOT EXISTS mensajes_contacto (
    id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    asunto VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Nuevo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- CATEGORIAS INICIALES
-- =========================================

INSERT IGNORE INTO categorias (nombre, descripcion) VALUES
('Arroces', 'Arroces orientales y especialidades'),
('Tallarines', 'Tallarines salteados y preparados al wok'),
('Entradas', 'Entradas para compartir'),
('Sopas', 'Sopas tradicionales'),
('Especialidades', 'Platos especiales de la casa');

-- =========================================
-- PLATOS DE EJEMPLO
-- =========================================

INSERT INTO platos
(id_categoria, nombre, descripcion, precio, imagen_url, disponible)
SELECT c.id_categoria, 'Arroz chaufa especial',
       'Arroz salteado al wok con una combinación de sabores.',
       25.00,
       'https://images.unsplash.com/photo-1512058564366-18510be2db19?w=700',
       TRUE
FROM categorias c
WHERE c.nombre = 'Arroces'
AND NOT EXISTS (
    SELECT 1 FROM platos p
    WHERE p.nombre = 'Arroz chaufa especial'
);

INSERT INTO platos
(id_categoria, nombre, descripcion, precio, imagen_url, disponible)
SELECT c.id_categoria, 'Tallarín saltado',
       'Tallarines salteados con verduras y salsa especial.',
       23.00,
       'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=700',
       TRUE
FROM categorias c
WHERE c.nombre = 'Tallarines'
AND NOT EXISTS (
    SELECT 1 FROM platos p
    WHERE p.nombre = 'Tallarín saltado'
);

INSERT INTO platos
(id_categoria, nombre, descripcion, precio, imagen_url, disponible)
SELECT c.id_categoria, 'Wantán frito',
       'Crujientes wantanes ideales para compartir.',
       12.00,
       'https://images.unsplash.com/photo-1563245372-f21724e3856d?w=700',
       TRUE
FROM categorias c
WHERE c.nombre = 'Entradas'
AND NOT EXISTS (
    SELECT 1 FROM platos p
    WHERE p.nombre = 'Wantán frito'
);

INSERT INTO platos
(id_categoria, nombre, descripcion, precio, imagen_url, disponible)
SELECT c.id_categoria, 'Sopa wantán',
       'Caldo preparado con wantanes y vegetales.',
       18.00,
       NULL,
       TRUE
FROM categorias c
WHERE c.nombre = 'Sopas'
AND NOT EXISTS (
    SELECT 1 FROM platos p
    WHERE p.nombre = 'Sopa wantán'
);

INSERT INTO platos
(id_categoria, nombre, descripcion, precio, imagen_url, disponible)
SELECT c.id_categoria, 'Pollo Chi Jau Kay',
       'Especialidad de pollo con salsa oriental.',
       29.00,
       NULL,
       TRUE
FROM categorias c
WHERE c.nombre = 'Especialidades'
AND NOT EXISTS (
    SELECT 1 FROM platos p
    WHERE p.nombre = 'Pollo Chi Jau Kay'
);