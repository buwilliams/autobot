# Backend
Modular python backend with FastAPI and unit tests.

## Run.py script

- script is in the root directory
- scripts always configures and uses Python virtual environment
- ensure graceful shutdown of application when Ctrl+C is pressed
- `run.py` will show help text
- `run.py help` will show help text
- `run.py web` will start the backend
- `run.py db:migrate` will run database migrations
- `run.py db:clean` will clean the database
- `run.py db:seed` will seed the database
- `run.py test` will run tests
- `run.py coverage` will show test coverage

## Run.sh script
- simple pass through script to execute `run.py` script
- ensure graceful shutdown of application when Ctrl+C is pressed

## Database
- database is in `backend` directory
- use SQLModel library
- uses SQLite as database
- SQLModel is stored as `db/database.db`
- migrations are in `db/migrations`
- seeds are in `db/seeds`

## Python Code Organization
- requirements.txt is in root directory
- python is in `backend` directory
- modular code organization
- app.py is the main application file and is in `backend`
- routes are in `backend/routes`
- models are in `backend/models`
- services are in `backend/services`
- tests are in `backend/tests`

## REST API
- all endpoints begin with `/api/`
- create a simple hello world endpoint in `backend/routes/hello.py`

## Static Web Server
- static files are in `frontend/` directory
- any endpoint that doesn't begin with `/api/` will be served from `frontend/` directory
- create simple hello world index.html files in `frontend/index.html`

## Best Practices
- unit tests with pytest
- high level of test coverage

## Unit tests
- write tests for `run.py`
- write tests for `backend/app.py`
- write tests for `backend/routes/hello.py`

## requirements.txt for python dependencies
- Python 3.10
- FastAPI 0.115.12
- uvicorn 0.34.1
- SQLModel 0.0.24
- pytest 8.3.5
- pytest-asyncio 0.26.0
- pytest-cov 6.1.1
- httpx 0.28.1