# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a lightweight ETL/ELT demo using Python 3.12+, SQLAlchemy 2.0+, and PostgreSQL. The project demonstrates:
- Environment-based database configuration (with support for named environments like "dev", "prod")
- ETL folder structure management (in, out, logs, tmp, dat, ctl)
- Database control table patterns
- Alembic migrations

## Common Commands

### Setup and Dependencies
```bash
# Create virtual environment using uv
uv venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
uv pip install -e .
```

### Database Migrations
```bash
# Apply all migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Create new migration with autogenerate
alembic revision -m "description" --autogenerate
```

### Running the Application
```bash
# Run main demo
python main.py
```

### Code Formatting
```bash
# Format code with black (configured in pyproject.toml)
black .
```

## Architecture

### Core Module: `etl/core.py`
Contains the fundamental ETL infrastructure:
- **EtlDbConfig**: Builds SQLAlchemy connection URIs from environment variables with prefix pattern `PG_[ENV_]VAR`
  - Without env name: reads `PG_DB`, `PG_USER`, `PG_PASS`, `PG_HOST`, `PG_PORT`, `PG_TYPE`
  - With env name (e.g., "dev"): reads `PG_DEV_DB`, `PG_DEV_USER`, etc.
  - Defaults: HOST=localhost, PORT=5532, TYPE=postgresql+psycopg, USER=$USER
- **EtlDbSource**: Factory for creating SQLAlchemy Engine instances from EtlDbConfig
- **EtlEnvironment**: Manages standard ETL folder structure (creates if missing)
- **SysFolderType**: Enum defining standard folders (INBOX="in", OUTBOX="out", LOGS="logs", TEMP="tmp", DATA="dat", CONTROL="ctl")

### Control Module: `etl/cntrl.py`
- **EtlControl**: Database access layer for control tables
  - Example: `get_file_sources()` queries `ctl_file_sources` table
  - Pattern for querying metadata/configuration tables

### Entry Point: `main.py`
Demonstrates the wiring pattern:
1. Load environment variables with `python-dotenv`
2. Initialize `EtlEnvironment` and check/create folders
3. Create `EtlDbConfig` and `EtlDbSource`
4. Pass engine to data access layers like `EtlControl`

### Migrations: `migrations/`
- Alembic environment configured in `migrations/env.py`
- Loads `.env` automatically and injects connection URI from `EtlDbConfig` into Alembic
- Database schema changes tracked in `migrations/versions/`

## Environment Configuration

### PostgreSQL Configuration
Create a `.env` file (copy from `.env.example`) with:
```
PG_DB=mydb
PG_USER=myuser
PG_PASS=secret
PG_HOST=localhost
PG_PORT=5532
PG_TYPE=postgresql+psycopg
```

For named environments, add the environment name to the prefix:
```
PG_DEV_DB=dev_db
PG_DEV_USER=dev_user
PG_DEV_PASS=dev_secret
```

Then use `EtlDbConfig("dev")` to load those variables.

### DuckDB Configuration
For DuckDB (file-based or in-memory), set:
```
PG_TYPE=duckdb
PG_DB=/path/to/database.duckdb
```

For in-memory DuckDB:
```
PG_TYPE=duckdb
PG_DB=:memory:
```

DuckDB does not require USER, PASS, HOST, or PORT settings.

## Key Patterns

1. **Environment-based configuration**: All database credentials come from environment variables, never hardcoded
2. **Named environments**: Support multiple database configs (dev/staging/prod) via env name prefixes
3. **Folder management**: ETL jobs expect standard folder structure; `EtlEnvironment` ensures they exist
4. **Alembic integration**: Migrations automatically use the same config pattern as the application
5. **Engine factories**: Create engines via `EtlDbSource.get_engine()` rather than inline

## Dependencies

- `sqlalchemy>=2.0`: ORM and database toolkit
- `psycopg>=3`: PostgreSQL driver (note: uses `postgresql+psycopg` dialect)
- `duckdb>=1.1.3`: DuckDB database engine
- `duckdb-engine>=0.13.2`: SQLAlchemy dialect for DuckDB
- `python-dotenv`: Load `.env` files
- `alembic`: Database migrations
- `pandas`: Data manipulation (included but not required for core demo)
- `black`: Code formatting
