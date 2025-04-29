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

# Ejecutar la aplicación
	uvicorn app.main:app --reload

Para ejecutar con Docker:
Accede a la documentación automática de la API en:
 http://localhost:8000/docs
 
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
