import pandas as pd
from pandas import DataFrame
from sqlalchemy import Engine, text


class EtlControl:
    def __init__(self, eng: Engine):
        self.engine = eng

    def get_file_sources(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM ctl_file_sources"))
            return result.mappings().all()

    def read_sql_as_dataframe(self, sql: str) -> DataFrame:
        return pd.read_sql(sql, self.engine)

    def write_dataframe_to_sql_overwrite(self, df: DataFrame, table_name: str):
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)

    def write_dataframe_to_sql_append(self, df: DataFrame, table_name: str):
        df.to_sql(table_name, self.engine, if_exists="append", index=False)
