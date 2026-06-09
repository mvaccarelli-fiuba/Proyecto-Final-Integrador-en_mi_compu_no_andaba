-- Admin de prueba. Email: admin@crustycrab.com / Password: admin1234
-- TODO: migrar a password hasheada con werkzeug antes de la entrega del 17/6.
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
-- probamos la reseña con una reserva
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