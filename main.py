import json
from json import dumps

from dotenv import load_dotenv

from etl.cntrl import EtlControl
from etl.core import EtlEnvironment
from etl.dba import EtlDbConfig, EtlDbSource
from etl.steps import load_etl_steps

load_dotenv()
etl_environment = EtlEnvironment()
etl_db_config = EtlDbConfig()
etl_db_core_src = EtlDbSource(etl_db_config)


def main():
    etl_environment.check_folders()
    ec = EtlControl(etl_db_core_src.get_engine())
    # Serialize ORM object using SerializerMixin to avoid JSON serialization errors
    fs = ec.get_file_sources()
    fls = [o.to_dict() for o in fs]
    print(json.dumps(fls, indent=4))
    stps = load_etl_steps()
    print(stps)
    print("Hello from etl-demo!")


if __name__ == "__main__":
    main()
