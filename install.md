# Installing Guide

This repository contains the backend microservices for the **Pythonidae** project, developed by the **GitCherryPick** team. 
The architecture follows RESTful API principles and each microservice maintains a modular structure with:
-   `api/`: route definitions according to RESTful standards
-   `models/`: SQLAlchemy models representing the database schema
-   `schemas/`: Pydantic schemas for request/response validation (similar to DTOs)
-   `services/`: business logic for API endpoints
-   `main.py`: application entry point and route inclusion
-   `database.py`: database connection logic (MySQL)
-   `tests/`: unit and integration tests for each service

## Local development Setup
	
1. Clone the repository in your code editor:
   ```
   git clone https://github.com/GitCherryPick/gensoft_infraestructure.git
   cd gensoft_infraestructure
   ```
 
2. You need to create .env file at the level of the root of the project, you need copy file .env.example and fill in the required environment variables, such as:
   ```
   USER_DB_HOST=mysql-db
   USER_DB_NAME=user_db
   USER_DB_NAME_TEST=user_db_test
   USER_DB_USER=app_user
   USER_DB_PASSWORD=user_pass
   ```
   > Use a different database name for testing to avoid overwriting production data.
3. For variables like AI_API_KEY, EMAIL_PASSWORD, and EMAIL_FROM, please contact us directly to receive these credentials securely:
 [supportGitCherryPick](202102843@est.umss.edu)
4. In this case, this repository needs Docker, once Docker is installed run:
   ```
   docker compose build
   docker compose up
   ```
6. The project - backend should now be running locally! :)

## Deployment

Currently, we use a local machine as our deployment server. Make sure the backend is running locally if you're trying to connect from the frontend.

### Additional documentation
For more information about the project you need visit [dev.md](https://github.com/GitCherryPick/gensoft_infraestructure/blob/main/dev.md). 
Or running app: [deploy.md](https://github.com/GitCherryPick/gensoft_infraestructure/blob/main/deploy.md)
