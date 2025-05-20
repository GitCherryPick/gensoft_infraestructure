## Sprint 1 – Documentación de Desarrollo 

### 1. Arquitectura

- Principios: S.O.L.I.D.

- Tecnologías: FastApi, SQLAlchemy, Alembic.

### 2. Estructura de carpetas
  

 - Microservicios (cada uno igual):
 - microservice-name/
   
		   app/
			  api/
		     core/
		     model/
		     repositories/
		     schema/
		     services/
		     utils/
		     main.py
		     database.py
			tests/ carpetas de tests específicas de este microservicio
		   Dockerfile
		   requirements.txt
		   alembic.ini
		   docker-compose.yml

  

### 3. Convenciones de Git

 - Ramas principales:
  > main Principal
  > sprint/"Numero" Desarrollo del sprint

 - Ramas de trabajo:

> feature/nombre-descriptivo
> bugfix/ticket-descripción
> hotfix/issue
> release/vX.Y.Z

  

### 4. Estándares de código
PEP8: https://peps.python.org/pep-0008/

### 5. Testing

- Frameworks: Pytest
- Ubicación: cada microservicio tiene su carpeta `tests/` con tests unitarios y de integración

6. CI/CD (GitHub Actions)

- En pull request, push hacia sprint/** y main