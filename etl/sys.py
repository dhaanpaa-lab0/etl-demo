from enum import Enum


class SysFolderType(Enum):
    INBOX = "in"
    OUTBOX = "out"
    LOGS = "logs"
    TEMP = "tmp"
    DATA = "dat"
    CONTROL = "ctl"


class SysFileType(Enum):
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    PARQUET = "parquet"
    XML = "xml"
