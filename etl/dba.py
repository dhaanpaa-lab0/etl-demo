import os

from sqlalchemy import create_engine, Engine


class EtlDbConfig:
    """
    Configuration for ETL database connection.

    This class facilitates managing database connection configurations for ETL
    processes, such as extracting essential database credentials from environment
    variables based on a specific environment name. It is designed to construct
    connection URIs compatible with SQLAlchemy.

    Supports both server-based databases (PostgreSQL) and file-based databases (DuckDB).

    :ivar env_name: The name of the current environment. If not provided, defaults
        to None.
    :type env_name: str or None
    :ivar env_prefix: The prefix applied to environment variables for the database
        configurations. Computed dynamically based on the `env_name`, defaulting
        to "PG_" if not specified.
    :type env_prefix: str
    :ivar db_name: The database name extracted from the configuration.
    :type db_name: str
    :ivar db_user: The database username extracted from the configuration or
        defaults to the OS environment user if not specified.
    :type db_user: str
    :ivar db_password: The database password extracted from the configuration.
    :type db_password: str
    :ivar db_host: The database host extracted from the configuration. Defaults
        to "localhost" if not found.
    :type db_host: str
    :ivar db_port: The database port extracted from the configuration. Defaults
        to "5532" if not found.
    :type db_port: str
    :ivar db_type: The database type extracted from the configuration. Defaults
        to "postgresql+psycopg" if not explicitly specified.
    :type db_type: str
    """

    def __init__(self, env_name: str = None):
        if env_name:
            self.env_name = env_name.upper()
            self.env_prefix = f"PG_{env_name}_"
        else:
            self.env_name = None
            self.env_prefix = "PG_"

        self.db_name = self.get_config_var("DB")
        self.db_user = self.get_config_var("USER", os.environ.get("USER"))
        self.db_password = self.get_config_var("PASS")
        self.db_host = self.get_config_var("HOST", "localhost")
        self.db_port = self.get_config_var("PORT", "5532")
        self.db_type = self.get_config_var("TYPE", "postgresql+psycopg")

    def get_config_var(self, var_name: str, default_value=None) -> str:
        return os.environ.get(f"{self.env_prefix}{var_name.upper()}", default_value)

    def get_sqlalchemy_uri(self) -> str:
        """
        Constructs the SQLAlchemy connection URI based on database type.

        For DuckDB (duckdb://), uses file path format: duckdb:///path/to/file.db
        or duckdb:///:memory: for in-memory databases.

        For server-based databases (PostgreSQL, etc.), uses standard format:
        TYPE://USER:PASS@HOST:PORT/DB

        :return: SQLAlchemy connection URI
        :rtype: str
        """
        if self.db_type.startswith("duckdb"):
            # DuckDB uses file path or :memory:
            # db_name can be a file path or ":memory:"
            if self.db_name == ":memory:":
                return "duckdb:///:memory:"
            else:
                # For file paths, use three slashes for absolute paths
                return f"duckdb:///{self.db_name}"
        else:
            # Server-based database (PostgreSQL, MySQL, etc.)
            return f"{self.db_type}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class EtlDbSource:
    """
    EtlDbSource is responsible for interacting with a database source in the ETL process.

    This class is designed to initialize and manage a database connection engine using
    the provided database configuration. It aims to provide a seamless way to set up
    database connections as part of the ETL (Extract, Transform, Load) workflow.

    :ivar db_config: The database configuration required to establish a connection.
    :type db_config: EtlDbConfig
    """

    def __init__(self, db_config: EtlDbConfig):
        self.db_config = db_config

    def get_engine(self) -> Engine:
        return create_engine(self.db_config.get_sqlalchemy_uri())
