## Descripción del Proyecto

  El Backend del sistema GitCherryPick es el componente central de una plataforma educativa que fomenta la enseñanza de Python a través de recursos prácticos e interactivos. Este proyecto, alojado en el repositorio gensoft_infraestructure, gestiona la lógica de negocio, la comunicación con la base de datos, y la integración con servicios externos, incluyendo un entorno seguro para ejecutar código.

Para instalar el proyecto y agregar nuevas caracteristicas visita [install.md](https://github.com/GitCherryPick/gensoft_infraestructure/blob/feat/add-install-file/install.md)

## Características Principales

* API RESTful: Implementada con FastAPI para ofrecer endpoints rápidos, eficientes y con documentación automática.
* Gestión de Datos: Uso de SQLAlchemy como ORM para conectar con una base de datos relacional MySQL.
* Entorno Seguro: Docker para sandboxing de código en un entorno aislado y para despliegues escalables.
* Arquitectura Modular: Diseñada para facilitar la escalabilidad y la integración con sistemas externos, como modelos de inteligencia artificial.
* Autenticación y Gestión de Usuarios: En desarrollo, con soporte para flujos seguros de autenticación.

## Estado del Proyecto

En desarrollo activo. Actualmente se ha completado el flujo de resolver ejercicios de programación en el lenguaje Python como estudiantes, feedback en tiempo real y revisar contenido subido por el docente. Además, como docente se puede crear dos tipos de ejercicios (replicador y ejercicio de laboratorio), revisar y tener feedback de las soluciones utilizando diferentes recursos, crear contenido teorico y exámenes. Este trabajo fue realizado en 8 sprints y puede ser mejorado con más características a implementar.

# Clonar el repositorio
	git clone https://github.com/GitCherryPick/gensoft_infraestructure.git
	cd gensoft_infraestructure

## Para verificar la documentación de cada microservicio:
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
* Gemini AI: Modelo flash 2.0 específicamente.
