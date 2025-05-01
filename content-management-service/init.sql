-- Base de datos para Content Management
CREATE DATABASE IF NOT EXISTS content_db;
CREATE DATABASE IF NOT EXISTS content_db_test;

-- Permisos para los usuarios
CREATE USER IF NOT EXISTS 'content_user'@'%' IDENTIFIED BY 'content_pass';
GRANT ALL PRIVILEGES ON content_db.* TO 'content_user'@'%';
GRANT ALL PRIVILEGES ON content_db_test.* TO 'content_user'@'%';

FLUSH PRIVILEGES;
