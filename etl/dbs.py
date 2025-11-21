import pandas as pd
from pandas import DataFrame
from sqlalchemy import Engine
from typing import Any, Dict, Optional, Union


class EtlDbDataFrame:
    def __init__(self, eng: Engine, schema_name: str = None):
        self.engine = eng
        if schema_name:
            self.schema_name = schema_name
        else:
            self.schema_name = "public"

    def read_table_as_dataframe(self, table_name: str) -> DataFrame:
        return pd.read_sql_table(table_name, self.engine, schema=self.schema_name)

    def read_sql_as_dataframe(
        self, sql: str, sql_params: Optional[Union[Dict[str, Any], list]] = None
    ) -> DataFrame:
        return pd.read_sql_query(sql=sql, con=self.engine, params=sql_params)

    def write_dataframe_to_sql_overwrite(self, df: DataFrame, table_name: str):
        df.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False,
            schema=self.schema_name,
        )

    def write_dataframe_to_sql_append(self, df: DataFrame, table_name: str):
        df.to_sql(
            table_name,
            self.engine,
            if_exists="append",
            index=False,
            schema=self.schema_name,
        )
