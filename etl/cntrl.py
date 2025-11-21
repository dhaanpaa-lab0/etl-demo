from sqlalchemy import Engine, text


class EtlControl:
    def __init__(self, eng: Engine):
        self.engine = eng

    def get_file_sources(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM ctl_file_sources"))
            return result.mappings().all()
