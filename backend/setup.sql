-- Admin de prueba. Email: admin@crustycrab.com / Password: admin1234
-- TODO: migrar a password hasheada con werkzeug antes de la entrega del 17/6.
INSERT INTO admin (email, password_hash, nombre)
VALUES ('admin@crustycrab.com', 'admin1234', 'Mr. Krabs');