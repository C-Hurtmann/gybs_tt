# Flask User Management API

### Test task: 
https://docs.google.com/document/d/1-nj3KBVA2ikirQAbF5N3v0HFhfTSSjUk/edit

A RESTful API for user management built with Flask, SQLAlchemy, and Marshmallow.


## API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users/ | Get a list of all users |
| GET | /users/{user_id} | Get a specific user by ID |
| POST | /users/ | Create a new user |
| PUT | /users/{user_id} | Update an existing user |
| DELETE | /users/{user_id} | Delete a user |
| GET | /swagger/ | Access API documentation |

## Tech Stack

- Flask: Web framework
- SQLAlchemy: ORM for database operations
- Flask-Migrate: Database migrations
- Marshmallow: Object serialization/deserialization
- Flasgger: API documentation
- Poetry: Dependency management
- Docker & Docker Compose: Containerization

## Installation

### Prerequisites

- Python 3.12+
- Poetry
- Docker and Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:C-Hurtmann/gybs_tt.git
   cd gybs_tt
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

4. Add .env file to project directory:

5. Run with Docker-Compose:
   ```bash
   docker-compose up --build
   ```

## API Documentation

The API documentation is available at `/swagger/` when the application is running. This interactive documentation allows you to:

- View all available endpoints
- See request and response formats
- Test the API directly from the browser

## Testing

Run the test suite using pytest:

```bash
# With Poetry
poetry run pytest

# With Docker
docker-compose exec app pytest
```