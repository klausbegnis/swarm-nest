# Tests

## Structure

```
tests/
├── conftest.py              # Shared fixtures (TestClient, DB, etc)
│
├── unit/                    # Unit tests (fast, isolated)
│   ├── core/                # Tests for app/core
│   │   └── test_exceptions.py
│   ├── schemas/             # Tests for app/schemas
│   │   └── (add schema validation tests)
│   └── services/            # Tests for app/services
│       └── (add service logic tests)
│
└── integration/             # Integration tests (API, DB, external)
    ├── api/                 # API endpoint tests
    │   ├── test_health.py
    │   └── test_root.py
    └── database/            # Database integration tests
        └── (add DB tests when needed)
```

## Running Tests

### By Folder
```bash
# All tests
uv run pytest

# Only unit tests (fast)
uv run pytest tests/unit

# Only integration tests
uv run pytest tests/integration

# Specific module
uv run pytest tests/unit/core
uv run pytest tests/integration/api
```

### By Marker
```bash
# Using markers
uv run pytest -m unit
uv run pytest -m integration
```

### With Coverage
```bash
# Coverage by test type
uv run pytest tests/unit --cov=app --cov-report=term-missing
uv run pytest tests/integration --cov=app --cov-report=term-missing
```

## Adding New Tests

### Unit Test
Place in corresponding module under `tests/unit/`:
- Core logic → `tests/unit/core/`
- Schemas → `tests/unit/schemas/`
- Services → `tests/unit/services/`

```python
# tests/unit/services/test_user_service.py
import pytest
from app.services.user_service import UserService

@pytest.mark.unit
def test_user_service_create():
    service = UserService()
    user = service.create(name="John")
    assert user.name == "John"
```

### Integration Test
Place in corresponding module under `tests/integration/`:
- API endpoints → `tests/integration/api/`
- Database → `tests/integration/database/`

```python
# tests/integration/api/test_users.py
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
def test_create_user(client: TestClient):
    response = client.post("/users", json={"name": "John"})
    assert response.status_code == 201
```

## Guidelines

### Unit Tests
- ✅ Fast (< 100ms each)
- ✅ No external dependencies (DB, API, files)
- ✅ Test single unit of code
- ✅ Use mocks for dependencies

### Integration Tests
- ✅ Test multiple components together
- ✅ Can use TestClient, database, etc
- ✅ Verify end-to-end functionality
- ✅ May be slower

## Best Practices

1. **One assertion per concept** - Keep tests focused
2. **Descriptive names** - `test_user_creation_with_duplicate_email`
3. **Arrange-Act-Assert** - Clear test structure
4. **Use fixtures** - Share setup code
5. **Isolate tests** - No dependencies between tests

