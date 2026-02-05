# Using This Template

## Automated Setup (Recommended)

Run the setup script to customize the template:

```bash
uv run python scripts/setup.py \
  --project-name "my-awesome-api" \
  --author "Your Name" \
  --company "Your Company" \
  --python-version "3.12"
```

This will:
- Update `pyproject.toml` with your project info
- Update `.ideconfig/settings.json` 
- Update all docstrings with your info and current date
- Create `.env` file from template
- Sync dependencies with uv

## Manual Setup

### 1. Update IDE Config

Edit `.ideconfig/settings.json`:

```json
"psi-header.variables": [
    ["author", "Your Name"],
    ["company", "Your Company"],
    ["projectname", "Your Project Name"]
]
```

### 2. Update Project Info

Edit `pyproject.toml`:

```toml
[project]
name = "your-project-name"
description = "Your project description"
```

### 3. Environment Variables

Copy `.env.template` to `.env` and customize:

```bash
# Copy template and edit
cp .env.template .env
# Edit .env with your values
```

### 4. Update Existing Docstrings

Existing files have placeholder docstrings. If using `psi-header` extension, regenerate headers after updating settings.json, or manually replace:
- `"replace with your name"` → Your Name
- `"replace with your company"` → Your Company  
- `"replace with your project name"` → Your Project Name

### 5. Using UV to manage dependencies

```bash
# Install dependencies
uv sync

# Run development server
uv run python main.py

# Or use FastAPI CLI
uv run fastapi dev app/main.py
```

## Structure

- `app/config/` - Settings loaded from `.env`
- `app/core/` - Infrastructure (logger, security, exceptions)
- `app/schemas/api/` - API schemas (requests, responses, base models)
- `app/routers/` - API endpoints
- `app/services/` - Business logic
- `app/utils/` - Generic utilities
- `app/dependencies.py` - Shared dependencies

## Settings Usage

```python
# Import global (for startup/config)
from app.config import settings

# Dependency injection (for routes/services)
from app.config import SettingsDep

@router.get("/example")
def example(settings: SettingsDep):
    return {"key": settings.OPENAI_API_KEY}
```

## Logger Usage

```python
from app.core.logger import get_logger

logger = get_logger(__name__)

@router.get("/users")
def get_users():
    logger.info("Fetching users")
    return {"users": []}
```

## Ruff - Linter & Formatter

```bash
# Check code
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

Configuration in `pyproject.toml`. Enforces PEP8, type hints, and best practices.

## Exception Handling

Standardized error responses:

```python
from app.core import NotFoundException, ValidationException

@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found")
    return user
```

Available exceptions:
- `NotFoundException` (404)
- `ValidationException` (422)
- `UnauthorizedException` (401)
- `ForbiddenException` (403)

All return format:
```json
{
  "success": false,
  "error_code": "NOT_FOUND",
  "message": "User not found",
  "path": "/users/123"
}
```

## Response Models

Standardized success responses:

```python
from app.schemas.api import SuccessResponse, PaginatedResponse

@router.post("/users", response_model=SuccessResponse[User])
def create_user(user: UserCreate):
    new_user = db.create_user(user)
    return SuccessResponse(
        message="User created",
        data=new_user
    )
```

Response format:
```json
{
  "success": true,
  "message": "User created",
  "data": {"id": 1, "name": "John"}
}
```

For pagination use `PaginatedResponse[T]`.

## Testing

Organized structure for scalability:

```
tests/
├── unit/          # Fast, isolated tests
│   ├── core/
│   ├── schemas/
│   └── services/
└── integration/   # API, DB tests
    ├── api/
    └── database/
```

Run tests:
```bash
# All tests
uv run pytest

# Only unit tests (fast)
uv run pytest tests/unit
uv run pytest -m unit

# Only integration tests
uv run pytest tests/integration
uv run pytest -m integration

# Specific folder
uv run pytest tests/unit/core
```

