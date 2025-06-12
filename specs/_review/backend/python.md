# Python Backend Specification

## Purpose
Create a modular Python backend application using FastAPI with SQLModel database integration, comprehensive testing, and proper project structure for API-driven applications.

## Goals
- Build a scalable FastAPI backend with clear separation of concerns
- Implement robust database layer with migrations and seeding
- Achieve high test coverage with comprehensive unit tests
- Provide easy development workflow with unified run script
- Support both API endpoints and static file serving

## Use Cases
1. **API Development**: Developers create REST endpoints for frontend applications
2. **Database Management**: Developers manage database schema, migrations, and test data
3. **Development Workflow**: Developers run, test, and debug the backend locally
4. **Static Serving**: Serve frontend assets alongside API endpoints

## Usage Rules
- All API endpoints must begin with `/api/` prefix
- Database operations must use SQLModel for type safety
- All code changes must include corresponding unit tests
- Use virtual environment for dependency isolation
- Graceful shutdown handling required for all processes

## Database Schema
```sql
-- SQLite database using SQLModel
-- Location: backend/db/database.db
-- Migrations: db/migrations/
-- Seeds: db/seeds/

-- Example user table structure
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Services
- **FastAPI Application**: Core web framework handling HTTP requests
- **Database Service**: SQLModel-based data access layer with SQLite
- **Migration Service**: Database schema version management
- **Static File Service**: Frontend asset serving for non-API routes
- **Test Service**: Comprehensive testing with pytest and coverage

## Endpoints
### REST API Endpoints
- `GET /api/health` - Health check endpoint
- `GET /api/hello` - Hello world demonstration endpoint
- All API routes prefixed with `/api/` for clear separation

### Static Routes
- `GET /*` - Serve static files from `frontend/` for non-API routes
- `GET /` - Serve `frontend/index.html` as default

## UI Layout
### Development Structure
- **Root Level**: Configuration and run scripts
- **Backend Directory**: Python application code
- **Frontend Directory**: Static assets and HTML files
- **Database Directory**: SQLite file and migration scripts

## Pages
1. **API Documentation** (`/docs`): FastAPI auto-generated documentation
2. **Frontend Assets** (`/`): Static file serving from frontend directory

## Technical Requirements

### Project Structure
```
/
├── run.py              # Main development script
├── run.sh              # Shell wrapper for run.py
├── requirements.txt    # Python dependencies
├── backend/
│   ├── app.py         # FastAPI application
│   ├── routes/        # API route handlers
│   ├── models/        # SQLModel database models
│   ├── services/      # Business logic layer
│   └── tests/         # Unit tests
├── frontend/
│   └── index.html     # Static frontend files
└── db/
    ├── database.db    # SQLite database
    ├── migrations/    # Database migrations
    └── seeds/         # Test data
```

### Run Script Commands
- `python run.py` or `python run.py help` - Show help text
- `python run.py web` - Start the FastAPI server
- `python run.py db:migrate` - Run database migrations
- `python run.py db:clean` - Clean database
- `python run.py db:seed` - Seed test data
- `python run.py test` - Run unit tests
- `python run.py coverage` - Show test coverage

### Dependencies (requirements.txt)
- Python 3.10+
- FastAPI 0.115.12
- uvicorn 0.34.1 (ASGI server)
- SQLModel 0.0.24 (database ORM)
- pytest 8.3.5 (testing framework)
- pytest-asyncio 0.26.0 (async test support)
- pytest-cov 6.1.1 (coverage reporting)
- httpx 0.28.1 (HTTP client for testing)

### Development Requirements
- Virtual environment configuration handled by run.py
- Graceful shutdown on Ctrl+C for all processes
- High test coverage with comprehensive unit tests
- Modular code organization with clear separation
- Type safety using SQLModel and FastAPI type hints