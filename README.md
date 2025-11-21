# Lightweight ETL or ELT demo

## Overview
This repository is a minimal ETL (Extract–Transform–Load) demo that shows how to:
- Configure database connections from environment variables (with optional environment names)
- Initialize a SQLAlchemy engine
- Manage expected system folders for an ETL runtime (in, out, logs, tmp, dat, ctl)
- Interact with a simple control table via SQL
- Support multiple database backends (PostgreSQL, DuckDB)

The code is small and intentionally straightforward so you can adapt it to your own projects.

## Key components
- etl/core.py
  - EtlDbConfig: builds a SQLAlchemy connection URI from env vars (PG_*). Supports named environments (e.g., PG_DEV_*) and multiple database backends (PostgreSQL, DuckDB).
  - EtlDbSource: creates a SQLAlchemy Engine from the config.
  - EtlEnvironment: checks/creates standard ETL folders under a system root (default: current directory).
- etl/cntrl.py
  - EtlControl: example DB access layer that queries ctl_file_sources.
- main.py
  - Wires everything together: loads .env, ensures folders exist, creates an engine, and queries ctl_file_sources.

## Requirements
- Python 3.12+
- A PostgreSQL instance you can connect to (or use DuckDB for local/embedded database)

## Project dependencies (via pyproject.toml)
- sqlalchemy>=2.0
- psycopg>=3 (driver used by SQLAlchemy URI: postgresql+psycopg)
- duckdb>=1.1.3 (embedded database engine)
- duckdb-engine>=0.13.2 (SQLAlchemy dialect for DuckDB)
- python-dotenv (loads .env)
- alembic (database migrations)
- pandas (not required for the minimal demo run, but included for convenience)
- black (code formatting)

## Quick start
1) Clone and enter the repo
   git clone <your-fork-or-origin>
   cd etl-demo

2) Create and activate a virtual environment (example using uv)
   uv venv
   source .venv/bin/activate

3) Install dependencies
   uv pip install -e .

4) Configure environment variables
   - Copy .env.example to .env and fill in values for your database.
   cp .env.example .env
   - Required keys (default prefix PG_):
     - PG_DB: database name
     - PG_USER: database user (defaults to OS $USER if not set)
     - PG_PASS: password
     - PG_HOST: host (default: localhost)
     - PG_PORT: port (default: 5532)
     - PG_TYPE: SQLAlchemy type/driver (default: postgresql+psycopg)
   - Named environments are supported by adding the env name to the prefix. For example, for "dev":
     - PG_DEV_DB, PG_DEV_USER, PG_DEV_PASS, PG_DEV_HOST, PG_DEV_PORT, PG_DEV_TYPE
     Then construct EtlDbConfig("dev") in your code to use those variables.

5) Initialize the database schema (optional but recommended)
   - The demo includes Alembic migrations under migrations/.
   - Ensure your PG_* connection points to the target database, then run:
   alembic upgrade head
   - This will create the ctl_file_sources table used by the demo query.

6) Run the demo
   python main.py

You should see folder creation logs and the result of selecting from ctl_file_sources.

## Environment variables and connection URI

### PostgreSQL Configuration
EtlDbConfig builds a SQLAlchemy URI like:
  TYPE://USER:PASS@HOST:PORT/DB
Defaults used if not specified in env vars:
- HOST=localhost
- PORT=5532
- TYPE=postgresql+psycopg
- USER defaults to the current OS user if PG_USER is not set

Example .env for PostgreSQL:
```
  PG_DB=mydb
  PG_USER=myuser
  PG_PASS=secret
  PG_HOST=localhost
  PG_PORT=5532
  PG_TYPE=postgresql+psycopg
```

### DuckDB Configuration
For DuckDB (file-based or in-memory database), the configuration is simpler:

Example .env for DuckDB (file-based):
```
  PG_TYPE=duckdb
  PG_DB=/path/to/database.duckdb
```

Example .env for DuckDB (in-memory):
```
  PG_TYPE=duckdb
  PG_DB=:memory:
```

DuckDB does not require USER, PASS, HOST, or PORT settings.
The connection URI will be `duckdb:///path/to/database.duckdb` or `duckdb:///:memory:`

See .env.example for a complete template.

## Project structure (selected)
- main.py                      Entry point wiring env, folders, and DB call
- etl/core.py                  Config, engine factory, and folder management
- etl/cntrl.py                 Simple control-table data access
- migrations/                  Alembic environment and example migrations
- alembic.ini                  Alembic config
- dw-demo/docker-compose.yml   Optional helper Compose file (not required)

## Alembic notes
- alembic.ini is configured for this project; ensure your environment variables are set before running migrations.
- Common commands:
  - alembic upgrade head
  - alembic downgrade -1
  - alembic revision -m "message" --autogenerate

## Troubleshooting
- Connection errors (PostgreSQL): Verify PG_* variables and that your database is reachable. Confirm your driver is postgresql+psycopg and psycopg>=3 is installed.
- Connection errors (DuckDB): Verify that PG_TYPE=duckdb and PG_DB is set to a valid file path or :memory:. Ensure duckdb>=1.1.3 and duckdb-engine>=0.13.2 are installed.
- Missing table ctl_file_sources: Run alembic upgrade head to apply migrations. Note: Alembic migrations are primarily designed for PostgreSQL; DuckDB users may need to adapt or create tables manually.
- Permission issues creating folders: The app creates in, out, logs, tmp, dat, ctl under the working directory. Run from a writable location or adjust EtlEnvironment(sys_root).
- DuckDB file permissions: If using a file-based DuckDB, ensure the directory where the database file will be created is writable.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Code is written mostly by humans with some help with a little bit of AI (Claude Code, and Jetbrains Junie Pro)

## License
MIT License. See the LICENSE file for full terms.

Copyright (c) 2025 Daniel Haanpaa [Lab0]
