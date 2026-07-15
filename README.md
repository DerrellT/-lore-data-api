# Lore Data API

- A beginner-friendly REST API built with FastAPI, SQLite, and JWT authentication to practice real-world backend development concepts, database design, and API testing.

⸻

## Project Overview

- Lore Data API manages fictional world data, including characters and regions. The project was built to learn backend development fundamentals through hands-on implementation rather than tutorials.

Throughout development, this was implemented:

* RESTful CRUD endpoints
* Relational database design
* JWT-based user authentication
* Password hashing with bcrypt
* Unit testing with pytest
* SQL queries using SQLite
⸻

## Tech Stack

- Python 3
- FastAPI
- SQLite (built-in database)
- Passlib (bycrypt)
- Python-JOSE (JWT)
- Pytest
- Uvicorn

⸻

## Database Design

- The system uses a relational database structure:

- 2 Tables

- regions:
id (Primary Key)
name

- characters:
id (Primary Key)
name
region_id (Foreign Key -> regions.id)

- users
- id (Primary Key)
- username
- password (bcrypt hashed)
- This demonstrates one-to-many relationships and basic relational database design.

⸻

## Features

- Character CRUD operations
- Region CRUD operations
- User login
- Password hashing
- JWT access token generation
- Foreign key relationships
- Error handling
- Unit tests for API endpoints

⸻

## API Endpoints:

* Characters 
- GET /characters/
- GET /characters/{name}
- POST /characters/
- PUT /characters/
- DELETE /characters/

* Regions
- GET /regions/
- GET /regions/{name}
- POST /regions/
- PUT /regions/
- DELETE /regions/

* Authentication
- POST /login/

⸻

## Testing

Implemented automated API tests using pytest.
- Character retrieval
- Region retrieval
- Login endpoint
- Character creation
- Region creation
- Character update
- Character deletion

⸻

## Key Concepts Learned:

- Relational database design
- Primary vs. foreign keys
- SQL CRUD operations
- Parameterized SQL queries
- REST API development
- JWT authentication
- Password hashing
- HTTP status codes
- API testing with pytest

⸻

# Project Status

This project is considered feature complete as a learning project. But future improvements may include:

- Dedicated test database
- SQLAlchemy ORM
- Request/response models using Pydantic
- Docker support
- User registration
- Role-based authorization
⸻

## How to Run

1. Install dependencies:
     FastAPI
     Uvicorn

2. Create the database:
    Run create_db.py

3. Start the server:
uvicorn app:app --reload

4. Visit:
http://127.0.0.1:8000/characters/


⸻

## Notes

- Built as part of a learning journey in backend development and database systems.
- Prioritizing learning fundamentals over production level architecture.
- It serves as a foundation for more advanced backend and API systems in the future.

