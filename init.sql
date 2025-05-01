-- Base de datos y usuario para User Management
CREATE DATABASE IF NOT EXISTS user_db;
CREATE DATABASE IF NOT EXISTS user_db_test;

-- Base de datos para Content Management
CREATE DATABASE IF NOT EXISTS content_db;
CREATE DATABASE IF NOT EXISTS content_db_test;

-- Base de datos para AI Assistant
CREATE DATABASE IF NOT EXISTS ai_db;
CREATE DATABASE IF NOT EXISTS ai_db_test;

-- Base de datos para Sandbox/Code Executor
CREATE DATABASE IF NOT EXISTS code_db;
CREATE DATABASE IF NOT EXISTS code_db_test;

-- Permisos para los usuarios
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'user_pass';
GRANT ALL PRIVILEGES ON user_db.* TO 'app_user'@'%';
GRANT ALL PRIVILEGES ON user_db_test.* TO 'app_user'@'%';

CREATE USER IF NOT EXISTS 'content_user'@'%' IDENTIFIED BY 'content_pass';
GRANT ALL PRIVILEGES ON content_db.* TO 'content_user'@'%';
GRANT ALL PRIVILEGES ON content_db_test.* TO 'content_user'@'%';

CREATE USER IF NOT EXISTS 'ai_user'@'%' IDENTIFIED BY 'ai_pass';
GRANT ALL PRIVILEGES ON ai_db.* TO 'ai_user'@'%';
GRANT ALL PRIVILEGES ON ai_db_test.* TO 'ai_user'@'%';

CREATE USER IF NOT EXISTS 'code_user'@'%' IDENTIFIED BY 'code_pass';
GRANT ALL PRIVILEGES ON code_db.* TO 'code_user'@'%';
GRANT ALL PRIVILEGES ON code_db_test.* TO 'code_user'@'%';

FLUSH PRIVILEGES;
