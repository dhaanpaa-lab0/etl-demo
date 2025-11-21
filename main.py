from json import dumps

from dotenv import load_dotenv

from etl.cntrl import EtlControl
from etl.core import EtlEnvironment, EtlDbConfig, EtlDbSource

load_dotenv()
etl_environment = EtlEnvironment()
etl_db_config = EtlDbConfig()
etl_db_core_src = EtlDbSource(etl_db_config)


def main():
    etl_environment.check_folders()
    ec = EtlControl(etl_db_core_src.get_engine())
    print(ec.get_file_sources())
    print("Hello from etl-demo!")


if __name__ == "__main__":
    main()
