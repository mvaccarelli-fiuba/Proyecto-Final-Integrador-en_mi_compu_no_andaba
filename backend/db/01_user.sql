CREATE USER IF NOT EXISTS 'tp_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON crusty_crab.* TO 'tp_user'@'localhost';
FLUSH PRIVILEGES;
