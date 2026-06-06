# Lore Data API

- A beginner backend API built with FastAPI and SQLite, designed to practice real-world database-driven API development.

⸻

## Project Overview

- Lore Data API is a simple REST API that manages fictional world data, including characters and regions. The project focuses on learning backend fundamentals such as database design, SQL queries, and API development using FastAPI.

- This project is actively in development as I expand my understanding of backend systems.

⸻

## Tech Stack

- Python 3
- FastAPI
- SQLite (built-in database)
- SQL (raw queries)

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

- This structure demonstrates basic relational database design and foreign key relationships.

⸻

## API Endpoints so far:

- GET /characters/
- Returns all characters in the database.
- GET /characters/{name}
- Returns a single character by exact name match.
- If the character does not exist, returns a 404 error.

⸻

## Key Concepts Learned:

- How relational databases work (SQLite)
- Primary keys vs foreign keys
- SQL SELECT queries
- Parameterized queries for safety
- fetchone vs fetchall usage
- Building REST APIs with FastAPI
- Connecting Python applications to databases

⸻

# Project Status

- This project is currently in active development. Future improvements include:

- Adding region based queries
- Implementing search functionality
- Expanding dataset relationships
- Improving API structure and performance

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

