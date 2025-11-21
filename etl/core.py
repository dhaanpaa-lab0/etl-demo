import os
from enum import Enum

from sqlalchemy import create_engine, Engine


class EtlDbConfig:
    """
    Configuration for ETL database connection.

    This class facilitates managing database connection configurations for ETL
    processes, such as extracting essential database credentials from environment
    variables based on a specific environment name. It is designed to construct
    connection URIs compatible with SQLAlchemy.

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
        to "postgres+psycopg3" if not explicitly specified.
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


class SysFolderType(Enum):
    INBOX = "in"
    OUTBOX = "out"
    LOGS = "logs"
    TEMP = "tmp"
    DATA = "dat"
    CONTROL = "ctl"


class EtlEnvironment:
    def __init__(self, sys_root="."):
        self.sys_root = sys_root

    """
    Manages the ETL environment setup and configuration.

    This class handles the creation and management of necessary system folders
    for ETL operations.
    """

    def check_folders(self):
        """
        Checks and ensures the existence of specific system folders defined by `SysFolderType`.
        Iterates through all folder types enumerated in `SysFolderType`, constructs their paths
        relative to a system root directory, and creates any missing folders.

        :param self: Instance reference to access the `sys_root` attribute.

        :raises OSError: If there is an issue creating a directory, such as insufficient
            permissions or invalid name.

        """
        for folder_type in SysFolderType:
            folder_path = os.path.join(self.sys_root, folder_type.value)
            print(f"Folder={folder_type.name} Path={folder_path}")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def get_folder_path(self, folder_type: SysFolderType) -> str:
        """
        Returns the absolute path for a specified system folder type.

        :param folder_type: The type of system folder to get the path for.
        :type folder_type: SysFolderType
        :return: The absolute path to the specified system folder.
        :rtype: str
        """
        return os.path.join(self.sys_root, folder_type.value)
