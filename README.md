### BACKEND GITCHERRYPICK

## Description
Se utilizará Docker para los microservicios que son contenedores en diferentes puertos.

## Running the app
1. Instala Docker Desktop, verifica que Docker es compatible con tu PC. (Nota, en este proyecto es opcional tener un Virtual Environment para Python.)
2. Nuestro proyecto está compuesto por microservicios, cada uno en un contenedor, incluyendo una base de datos Mysql (también en un contenedor)
3. Para facilitar su configuración, se usa Docker compose, ejecuta el siguiente comando:
```bash
# development
$ docker compose up
```
4. Verifica los contenedores corriendo en Docker Desktop.
![image](https://github.com/user-attachments/assets/a1f96884-7b09-45f8-9f3e-502302c68e4e)
5. Puede ser util:
```bash
# install fastapi 
$ pip install fastapi

# SQLAlchemy relaciona SQL a Python 
$ pip install sqlalchemy

# install pymsql 
$ pip install pymsql

# alembic para migraciones 
$ pip install alembic

```
## Stay in touch

- Author - 
