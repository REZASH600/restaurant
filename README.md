# Getting Started with Docker for django Project

This project uses Docker to containerize the Django application and PostgreSQL database.

## Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/)

## Environment Setup

Before running the project, you need to set up environment variables. The required `.env` files should be placed in the following locations:
```
envs/local/web.env
```
```
envs/local/postgres.env
```

### Example `web.env` File:
```ini
DJANGO_SUPERUSER_PHONE=09337817068
DJANGO_SUPERUSER_EMAIL=rezasharafdini973@gmail.com
DJANGO_SUPERUSER_PASSWORD=1234


SECRET_KEY=django-insecure-xm&wc39ajw8q9a(q_i*+!p$ic$-6e3zo0aq2aci7#rdx3(97()
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```



### Example `postgres.env` File:
```ini
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```


## Running the Project with Docker

To build and run the Docker containers, use the following command:
```
make l-build
```

This command will build and start all necessary containers, including the Django application and PostgreSQL database.


## Accessing the Application
Once the containers are up and running, you can access the application at:
```
http://localhost:8000
```

## Stopping the Containers
To stop the running containers, use:
```
make l-down
```


## Database Schema Diagram

The database schema diagram is available at the following link:

[Database Schema (draw.io)](https://drive.google.com/file/d/1tckU4alTGrlECxeaksk15KEk69UviUN8/view?usp=sharing)
