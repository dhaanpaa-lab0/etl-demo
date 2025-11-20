from dotenv import load_dotenv

from etl.core import EtlEnvironment

load_dotenv()
etl_environment = EtlEnvironment()


def main():
    etl_environment.check_folders()
    print("Hello from etl-demo!")


if __name__ == "__main__":
    main()
