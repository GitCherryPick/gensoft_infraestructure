### DEPLOY BACKEND GITCHERRYPICK

## Descripcion
Se utilizará Docker para los microservicios que son contenedores en diferentes puertos.

## Running the app
1. Instala Docker Desktop, verifica que Docker funcione correctamente en tu PC. (Nota, en este proyecto es opcional tener un Virtual Environment para Python)
2. Nuestro proyecto está compuesto por microservicios, cada uno en un contenedor, incluyendo una base de datos Mysql (también en un contenedor)
3. Para facilitar su configuración, se usa Docker compose, ejecuta el siguiente comando:
```bash
# development
$ docker compose up
```
4. Verifica los contenedores corriendo en Docker Desktop.
![image](https://github.com/user-attachments/assets/2f23cc69-3808-41b3-8dab-732e9d6f486c)
