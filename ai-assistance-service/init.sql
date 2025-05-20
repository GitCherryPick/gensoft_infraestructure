-- Base de datos para AI Assistant
CREATE DATABASE IF NOT EXISTS ai_db;
CREATE DATABASE IF NOT EXISTS ai_db_test;

-- Permisos para los usuarios
CREATE USER IF NOT EXISTS 'ai_user'@'%' IDENTIFIED BY 'ai_pass';
GRANT ALL PRIVILEGES ON ai_db.* TO 'ai_user'@'%';
GRANT ALL PRIVILEGES ON ai_db_test.* TO 'ai_user'@'%';

FLUSH PRIVILEGES;
