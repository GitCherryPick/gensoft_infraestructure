-- Base de datos para Sandbox/Code Executor
CREATE DATABASE IF NOT EXISTS code_db;
CREATE DATABASE IF NOT EXISTS code_db_test;

-- Permisos para los usuarios
CREATE USER IF NOT EXISTS 'code_user'@'%' IDENTIFIED BY 'code_pass';
GRANT ALL PRIVILEGES ON code_db.* TO 'code_user'@'%';
GRANT ALL PRIVILEGES ON code_db_test.* TO 'code_user'@'%';

FLUSH PRIVILEGES;
