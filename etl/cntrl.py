import pandas as pd
from pandas import DataFrame
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from etl.ctl.models import FileSource, HttpSource


class EtlControl:
    def __init__(self, eng: Engine):
        self.engine = eng

    def get_file_sources(self):
        # Use ORM model to fetch all file sources
        with Session(self.engine) as session:
            return session.scalars(select(FileSource)).all()

    def get_http_sources(self):
        with Session(self.engine) as session:
            return session.scalars(select(HttpSource)).all()
