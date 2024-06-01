# PolicyClaimProcess

## Introduction :
           This FastAPI-based API serves as a backend for managing medical procedure data. It provides endpoints for submitting, retrieving, updating, and deleting procedure data, as well as retrieving statistics on the top providers by net fees.

## Endpoints:
Submit Data: POST /submit-data

Saves procedure data to the database.
Get Data: GET /get-data

Retrieves all procedure data from the database.
Update Data: PUT /update-data/{procedure_id}

Updates existing procedure data in the database.
Delete Data: DELETE /delete-data/{procedure_id}

Deletes procedure data from the database.
Top Providers: GET /top-providers

Retrieves the top 10 provider NPIs by net fees.

## Dependencies:
FastAPI: Web framework for building APIs quickly.
SQLModel: SQL database toolkit and ORM.
SQLAlchemy: SQL toolkit and ORM.
Pydantic: Data validation and serialization library.
Rate Limiter: Middleware for rate limiting requests.

## Features:
Data validation using Pydantic models.
Rate limiting middleware to prevent abuse.
Database integration for storing and retrieving procedure data.
CRUD operations (Create, Read, Update, Delete) on procedure data.
Statistics retrieval for top providers by net fees.
For detailed documentation and usage examples, refer to the code and comments in the provided files (main.py, models.py, schemas.py, database.py, rate_limiter.py). You can also run the API locally or within a Docker container by following the instructions provided.

## Application Guide:

To run the App : “uvicorn app.main:app --reload”

Docker Build CMD:
docker-compose build
docker-compose up

