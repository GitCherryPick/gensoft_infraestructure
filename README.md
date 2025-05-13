## Descripción del Proyecto

  El Backend del sistema GitCherryPick es el componente central de una plataforma educativa que fomenta la enseñanza de Python a través de recursos prácticos e interactivos. Este proyecto, alojado en el repositorio gensoft_infraestructure, gestiona la lógica de negocio, la comunicación con la base de datos, y la integración con servicios externos, incluyendo un entorno seguro para ejecutar código.

## Características Principales

* API RESTful: Implementada con FastAPI para ofrecer endpoints rápidos, eficientes y con documentación automática.
* Gestión de Datos: Uso de SQLAlchemy como ORM para conectar con una base de datos relacional MySQL.
* Entorno Seguro: Docker para sandboxing de código en un entorno aislado y para despliegues escalables.
* Arquitectura Modular: Diseñada para facilitar la escalabilidad y la integración con sistemas externos, como repositorios OER y modelos de inteligencia artificial.
* Autenticación y Gestión de Usuarios: En desarrollo, con soporte para flujos seguros de autenticación.

## Estado del Proyecto

En desarrollo activo. Actualmente en Sprint 01, enfocados en:
	Implementación de autenticación de usuarios.
	Gestión de perfiles y datos de usuarios.
	Integración del simulador de código en un entorno seguro.

## Demostración

Para ejecutar el backend localmente:
bash
# Clonar el repositorio
	git clone https://github.com/GitCherryPick/gensoft_infraestructure.git
	cd gensoft_infraestructure

# Crear un entorno virtual (opcional pero recomendado)
	python -m venv venv
	source venv/bin/activate  # Linux/Mac
	venv\Scripts\activate     # Windows

# Instalar dependencias
	pip install -r requirements.txt

Configurar variables de entorno
Crear un archivo .env con las siguientes variables (ajusta según tu configuración)
 
# GLOBAL 
# Archivo .env para las predenciales
DB_PORT=3306
MYSQL_ROOT_PASSWORD=password

USER_DB_HOST=mysql-db
USER_DB_NAME=user_db
USER_DB_NAME_TEST=user_db_test
USER_DB_USER=app_user
USER_DB_PASSWORD=user_pass

CONTENT_DB_HOST=mysql-content
CONTENT_DB_NAME=content_db
CONTENT_DB_NAME_TEST=content_db_test
CONTENT_DB_USER=content_user
CONTENT_DB_PASSWORD=content_pass

AI_DB_HOST=mysql-ai
AI_DB_NAME=ai_db
AI_DB_NAME_TEST=ai_db_test
AI_DB_USER=ai_user
AI_DB_PASSWORD=ai_pass
AI_API_KEY=AIzaSyDFL5k8ZvJmrrz2BHhcfqXrmk66VKRdnnM

CODE_DB_HOST=mysql-code-exec
CODE_DB_NAME=code_db
CODE_DB_NAME_TEST=code_db_test
CODE_DB_USER=code_user
CODE_DB_PASSWORD=code_pass

EMAIL_HOST=smtp.sendgrid.net
EMAIL_USERNAME=apikey  
EMAIL_PASSWORD=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
EMAIL_FROM=judith.margarita.paco@hotmail.com


# Ejecutar la aplicación
### Antes de la ejecición se debe abrir docker desktop
	uvicorn app.main:app --reload

## Para ejecutar con Docker:
### User-service
Accede a la documentación automática de la API en:
 http://localhost:8000/docs

 ### IA-assistance
Accede a la documentación automática de la API en:
 http://localhost:8005/docs

 ### sandbox
Accede a la documentación automática de la API en:
 http://localhost:8002/docs

 ### User-managerment
Accede a la documentación automática de la API en:
 http://localhost:8006/docs

 
## Acceso al Proyecto
Repositorio del Backend:
 https://github.com/GitCherryPick/gensoft_infraestructure
 
Repositorio Principal del Proyecto:
 https://github.com/GitCherryPick
 
## Requisitos previos:
* Python 3.11+
* MySQL configurado
* Docker (para entornos con contenedores)
* Archivo .env con las variables de entorno necesarias

## Tecnologías Utilizadas
* Python 3.11+: Lenguaje principal.
* FastAPI: Framework para APIs rápidas y escalables.
* SQLAlchemy: ORM para la gestión de bases de datos.
* MySQL: Base de datos relacional.
* Docker: Para sandboxing de código y despliegues.
* Pydantic: Validación y serialización de datos.
* Uvicorn: Servidor ASGI para desarrollo y producción.
