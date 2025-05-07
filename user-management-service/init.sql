-- Base de datos y usuario para User Management
CREATE DATABASE IF NOT EXISTS user_db;
CREATE DATABASE IF NOT EXISTS user_db_test;

-- Permisos para los usuarios
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'user_pass';
GRANT ALL PRIVILEGES ON user_db.* TO 'app_user'@'%';
GRANT ALL PRIVILEGES ON user_db_test.* TO 'app_user'@'%';

FLUSH PRIVILEGES;
