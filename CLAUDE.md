# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a lightweight ETL/ELT demo using Python 3.12+, SQLAlchemy 2.0+, and multiple database backends (PostgreSQL,
MySQL, DuckDB). The project demonstrates:

- Environment-based database configuration (with support for named environments like "dev", "prod")
- ETL folder structure management (in, out, logs, tmp, dat, ctl)
- Database control table patterns
- Alembic migrations

## Package Manager: uv

This project uses **uv** as its Python package manager. uv is an extremely fast Python package installer and resolver written in Rust, serving as a drop-in replacement for pip. Key benefits:

- **Speed**: 10-100x faster than pip for package installation and resolution
- **Deterministic**: Produces consistent, reproducible installs
- **Compatibility**: Drop-in replacement for pip commands (`uv pip install`, `uv pip list`, etc.)
- **Virtual environments**: Built-in venv support with `uv venv`

For more information, see: https://github.com/astral-sh/uv

## Common Commands

### Setup and Dependencies

```bash
# Create virtual environment using uv
uv venv
source .venv/bin/activate  # On macOS/Linux
# On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Add a new dependency
uv pip install package-name

# Update dependencies
uv pip install --upgrade package-name
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

### System Module: `etl/sys.py`

Defines system-level enumerations:

- **SysFolderType**: Enum defining standard ETL folders (INBOX="in", OUTBOX="out", LOGS="logs", TEMP="tmp", DATA="dat",
  CONTROL="ctl")
- **SysFileType**: Enum defining supported file formats (CSV, EXCEL, JSON, PARQUET, XML)

### Core Module: `etl/core.py`

Contains the fundamental ETL infrastructure:

- **EtlDbConfig**: Builds SQLAlchemy connection URIs from environment variables with prefix pattern `PG_[ENV_]VAR`
    - Without env name: reads `PG_DB`, `PG_USER`, `PG_PASS`, `PG_HOST`, `PG_PORT`, `PG_TYPE`
    - With env name (e.g., "dev"): reads `PG_DEV_DB`, `PG_DEV_USER`, etc.
    - Defaults: HOST=localhost, PORT=5532, TYPE=postgresql+psycopg, USER=$USER
- **EtlDbSource**: Factory for creating SQLAlchemy Engine instances from EtlDbConfig
- **EtlEnvironment**: Manages standard ETL folder structure (creates if missing)
    - `check_folders()`: Ensures all SysFolderType folders exist
    - `get_folder_path(folder_type)`: Returns absolute path for a specified folder type

### File Module: `etl/fil.py`

Provides file I/O operations using pandas:

- **FileSource**: Reads and writes files in various formats
    - Constructor: `FileSource(file_path, file_type=SysFileType.CSV)`
    - `read()`: Returns a pandas DataFrame from the file
    - `write(df)`: Writes a pandas DataFrame to the file
    - Supported formats: CSV, Excel, JSON, Parquet, XML (via SysFileType)

### Control Module: `etl/cntrl.py`

Database access layer for control tables and data operations:

- **EtlControl**: Provides database interaction methods
    - `get_file_sources()`: Queries `ctl_file_sources` table
    - `read_sql_as_dataframe(sql)`: Executes SQL query and returns results as pandas DataFrame
    - `write_dataframe_to_sql_overwrite(df, table_name)`: Writes DataFrame to table (replaces existing data)
    - `write_dataframe_to_sql_append(df, table_name)`: Writes DataFrame to table (appends to existing data)
    - Pattern for querying metadata/configuration tables

### Models Module: `etl/ctl/models.py`

SQLAlchemy ORM models using modern 2.0 type-annotated style:

- **Base**: DeclarativeBase class that serves as the base for all ORM models
- **HttpSource**: Model for `ctl_http_sources` table
    - `source_key: Mapped[str]` - Primary key for HTTP source
    - `source_url: Mapped[Optional[str]]` - URL endpoint
    - `source_method: Mapped[Optional[str]]` - HTTP method (GET, POST, etc.)
    - `source_params: Mapped[Optional[dict]]` - JSON parameters for the request
- **FileSource**: Model for `ctl_file_sources` table
    - `file_key: Mapped[str]` - Primary key for file source
    - `file_description: Mapped[Optional[str]]` - Human-readable description
    - `enabled: Mapped[Optional[bool]]` - Whether the file import is enabled
    - `file_type: Mapped[Optional[SysFileType]]` - File format (CSV, Excel, etc.)

**SQLAlchemy 2.0 Type-Annotated Style Guidelines:**

This project uses the modern SQLAlchemy 2.0 declarative mapping style. When creating or modifying models:

1. **Base class**: Inherit from `DeclarativeBase`, not the old `declarative_base()` function
   ```python
   from sqlalchemy.orm import DeclarativeBase

   class Base(DeclarativeBase):
       pass
   ```

2. **Type annotations**: Use `Mapped[T]` for all column attributes
   ```python
   from sqlalchemy.orm import Mapped, mapped_column

   class MyModel(Base):
       id: Mapped[int] = mapped_column(primary_key=True)
       name: Mapped[str] = mapped_column(String(50))
       optional_field: Mapped[Optional[str]] = mapped_column(String(100))
   ```

3. **mapped_column()**: Use `mapped_column()` instead of `Column()`
   - The type is inferred from the `Mapped[T]` annotation
   - Explicit type can still be provided for database-specific types (e.g., `String(50)`)

4. **Optional types**: Use `Optional[T]` for nullable columns to reflect the database schema in type hints

5. **Benefits**: Better IDE autocomplete, type checking with mypy, and alignment with SQLAlchemy 2.0 best practices

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

### MySQL Configuration

For MySQL, set:

```
PG_DB=mydb
PG_USER=myuser
PG_PASS=secret
PG_HOST=localhost
PG_PORT=3306
PG_TYPE=mysql+pymysql
```

MySQL uses the standard server-based connection format (USER, PASS, HOST, PORT, DB). The default port for MySQL is 3306.

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
6. **File format abstraction**: Use `FileSource` with `SysFileType` enum to handle different file formats consistently
7. **DataFrame integration**: `EtlControl` provides methods to read/write DataFrames directly to/from database tables
8. **SQLAlchemy 2.0 type-annotated style**: All ORM models use `Mapped[T]` annotations and `mapped_column()` for better type safety and modern best practices
9. **uv package manager**: Use `uv` commands for all package management operations for faster, more reliable dependency resolution

## Dependencies

- `sqlalchemy>=2.0`: ORM and database toolkit
- `psycopg>=3`: PostgreSQL driver (note: uses `postgresql+psycopg` dialect)
- `pymysql>=1.1.0`: MySQL driver (note: uses `mysql+pymysql` dialect)
- `duckdb>=1.1.3`: DuckDB database engine
- `duckdb-engine>=0.13.2`: SQLAlchemy dialect for DuckDB
- `python-dotenv`: Load `.env` files
- `alembic`: Database migrations
- `pandas>=2.3.3`: Data manipulation (required for FileSource and DataFrame operations in EtlControl)
- `pandas-stubs>=2.3.2`: Type hints for pandas
- `black`: Code formatting
