import pandas as pd
from pandas import DataFrame
from .sys import SysFileType


class FileSource:

    def __init__(self, file_path, file_type: SysFileType = SysFileType.CSV):
        self.file_path = file_path
        self.file_type = file_type

    def read(self) -> DataFrame:
        match self.file_type:
            case SysFileType.CSV:
                return pd.read_csv(self.file_path)
            case SysFileType.EXCEL:
                return pd.read_excel(self.file_path)
            case SysFileType.JSON:
                return pd.read_json(self.file_path)
            case SysFileType.PARQUET:
                return pd.read_parquet(self.file_path)
            case SysFileType.XML:
                return pd.read_xml(self.file_path)

    def write(self, df: DataFrame):
        match self.file_type:
            case SysFileType.CSV:
                df.to_csv(self.file_path)
            case SysFileType.EXCEL:
                df.to_excel(self.file_path)
            case SysFileType.JSON:
                df.to_json(self.file_path)
            case SysFileType.PARQUET:
                df.to_parquet(self.file_path)
            case SysFileType.XML:
                df.to_xml(self.file_path)
