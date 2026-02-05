# Testing

## Quick Start

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_health.py

# Run with verbose output
uv run pytest -v
```

## Test Markers

Tests are categorized using pytest markers:

```bash
# Run only unit tests (fast, isolated)
uv run pytest -m unit

# Run only integration tests (API, database)
uv run pytest -m integration

# Run all except slow tests
uv run pytest -m "not slow"

# Combine markers
uv run pytest -m "unit or integration"
```

Available markers:
- `@pytest.mark.unit` - Unit tests (fast, no external dependencies)
- `@pytest.mark.integration` - Integration tests (API endpoints, DB)
- `@pytest.mark.slow` - Slow running tests

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures (TestClient, etc)
├── unit/                    # Unit tests (fast, isolated)
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── test_exceptions.py
│   ├── schemas/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
└── integration/             # Integration tests (API, DB)
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   ├── test_health.py
    │   └── test_root.py
    └── database/
        └── __init__.py
```

Benefits:
- Clear separation of test types
- Organized by application layer
- Easy to run specific test categories
- Scales well as project grows

## Writing Tests

### Unit Test Example

```python
import pytest
from app.core import NotFoundException

@pytest.mark.unit
def test_exception_properties():
    """Test exception class (isolated, fast)"""
    exc = NotFoundException("Resource not found")
    assert exc.status_code == 404
    assert exc.error_code == "NOT_FOUND"
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
def test_endpoint(client: TestClient):
    """Test API endpoint (requires TestClient)"""
    response = client.get("/endpoint")
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

### Using Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Test", "value": 123}

# tests/test_example.py
def test_with_fixture(client: TestClient, sample_data):
    response = client.post("/endpoint", json=sample_data)
    assert response.status_code == 201
```

### Testing with Dependencies

```python
from app.config import get_settings

def override_settings():
    return Settings(DATABASE_URL="sqlite:///./test.db")

def test_with_override(client: TestClient):
    app.dependency_overrides[get_settings] = override_settings
    response = client.get("/endpoint")
    assert response.status_code == 200
    app.dependency_overrides.clear()
```

## Test Coverage

```bash
# Run with coverage report
uv run pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Best Practices

1. **One test, one assertion focus** - Test one thing at a time
2. **Use descriptive names** - `test_user_login_with_invalid_password`
3. **Arrange-Act-Assert** - Setup, execute, verify
4. **Use fixtures** - Reuse setup code
5. **Mock external services** - Don't hit real APIs in tests

## Example Tests

### Testing POST Requests

```python
def test_create_item(client: TestClient):
    item_data = {"name": "Test Item", "price": 10.99}
    response = client.post("/items", json=item_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.99
```

### Testing Error Handling

```python
def test_not_found(client: TestClient):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

### Testing Authentication

```python
def test_protected_endpoint(client: TestClient):
    # Without auth
    response = client.get("/protected")
    assert response.status_code == 401
    
    # With auth
    headers = {"Authorization": "Bearer token"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
```

## Continuous Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    uv sync
    uv run pytest --cov=app
```

