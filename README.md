# Getting Started with Docker for django Project

This project uses Docker to containerize the Django application and PostgreSQL database.

## Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/)


## Running the Project with Docker

To build and run the Docker containers, use the following command:
```
make l-build
```

This command will build and start all necessary containers, including the Django application and PostgreSQL database.

## Enabling pg_trgm Extension for PostgreSQL

The project uses PostgreSQL's `pg_trgm` extension for fuzzy search functionality. To enable this extension inside the PostgreSQL container, run the following command:

```bash
pg_trgm-enable

```


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
