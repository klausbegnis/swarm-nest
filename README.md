# FastAPI Template

Modern FastAPI project template.

## Quick Setup

After cloning, customize the template:

```bash
uv run python scripts/setup.py \
  --project-name "my-awesome-api" \
  --author "Your Name" \
  --company "Your Company" \
  --python-version "3.12"
```

This automatically updates all files, docstrings, and dependencies.

## Folder Structure

```
app/
├── config/          # Settings with Pydantic
├── core/            # Infrastructure (logger, security, exceptions)
├── schemas/         # Pydantic schemas
│   └── api/         # API schemas (requests, responses, base)
├── routers/         # API endpoints
├── services/        # Business logic
├── utils/           # Utilities
└── main.py          # FastAPI app

tests/
├── conftest.py      # Shared fixtures
├── unit/            # Unit tests (fast, isolated)
│   ├── core/        # Core module tests
│   ├── schemas/     # Schema validation tests
│   └── services/    # Service logic tests
└── integration/     # Integration tests (API, DB)
    ├── api/         # API endpoint tests
    └── database/    # Database tests

scripts/
└── setup.py         # Template customization script
```

## Docs

1. [Using this template](/docs/template.md)
2. [Docker](/docs/docker.md)
3. [Testing](/docs/testing.md)

## Copyright

Copyright (c) 2025. All rights reserved.

