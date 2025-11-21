#!/usr/bin/env python3
"""
Script to add a new file source to the ctl_file_sources table.

Usage:
    # Interactive mode
    python add_file_source.py

    # Command-line mode
    python add_file_source.py --key "my_file" --description "My data file" --type csv --enabled

    # With environment name
    python add_file_source.py --env dev --key "my_file" --description "My data file" --type csv
"""

import argparse
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from etl.dba import EtlDbConfig, EtlDbSource
from etl.ctl.models import FileSource
from etl.sys import SysFileType


def add_file_source(
    engine,
    file_key: str,
    file_description: str = None,
    file_type: SysFileType = None,
    enabled: bool = True,
) -> FileSource:
    """
    Adds a new file source to the ctl_file_sources table.

    :param engine: SQLAlchemy Engine instance
    :param file_key: Unique key for the file source (primary key)
    :param file_description: Optional description of the file source
    :param file_type: Optional file type from SysFileType enum
    :param enabled: Whether the file import is enabled (default: True)
    :return: The created FileSource object
    :raises ValueError: If file_key already exists
    """
    with Session(engine) as session:
        # Check if file_key already exists
        existing = session.get(FileSource, file_key)
        if existing:
            raise ValueError(f"File source with key '{file_key}' already exists")

        # Create new file source
        new_source = FileSource(
            file_key=file_key,
            file_description=file_description,
            file_type=file_type,
            enabled=enabled,
        )

        session.add(new_source)
        session.commit()
        session.refresh(new_source)

        print(f"Successfully added file source: {file_key}")
        return new_source


def interactive_mode(engine):
    """
    Interactive mode for adding a file source with user prompts.
    """
    print("\n=== Add New File Source ===\n")

    # Get file key
    file_key = input("Enter file key (required): ").strip()
    if not file_key:
        print("Error: File key is required")
        sys.exit(1)

    # Get description
    file_description = input("Enter file description (optional): ").strip() or ""

    # Get file type
    print("\nAvailable file types:")
    for ft in SysFileType:
        print(f"  - {ft.value}")
    file_type_input = input("Enter file type (optional): ").strip()
    file_type = None
    if file_type_input:
        try:
            file_type = SysFileType(file_type_input.lower())
        except ValueError:
            print(f"Warning: Invalid file type '{file_type_input}', skipping")

    # Get enabled status
    enabled_input = input("Enable file source? (Y/n): ").strip().lower()
    enabled = enabled_input != "n"

    # Confirm
    print("\n=== Summary ===")
    print(f"File Key: {file_key}")
    print(f"Description: {file_description or 'None'}")
    print(f"File Type: {file_type.value if file_type else 'None'}")
    print(f"Enabled: {enabled}")

    confirm = input("\nAdd this file source? (Y/n): ").strip().lower()
    if confirm == "n":
        print("Cancelled")
        sys.exit(0)

    # Add the file source
    try:
        add_file_source(engine, file_key, file_description, file_type, enabled)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Add a new file source to the ctl_file_sources table"
    )
    parser.add_argument(
        "--env",
        type=str,
        help="Environment name (e.g., dev, prod) for database connection",
    )
    parser.add_argument("--key", type=str, help="File key (primary key)")
    parser.add_argument("--description", type=str, help="File description")
    parser.add_argument(
        "--type",
        type=str,
        choices=[ft.value for ft in SysFileType],
        help="File type",
    )
    parser.add_argument(
        "--enabled",
        action="store_true",
        default=None,
        help="Enable the file source (default: True)",
    )
    parser.add_argument(
        "--disabled", action="store_true", help="Disable the file source"
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Setup database connection
    db_config = EtlDbConfig(args.env)
    db_source = EtlDbSource(db_config)
    engine = db_source.get_engine()

    # Determine mode
    if args.key:
        # Command-line mode
        file_type = SysFileType(args.type) if args.type else None
        enabled = False if args.disabled else True

        try:
            add_file_source(engine, args.key, args.description, file_type, enabled)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_mode(engine)


if __name__ == "__main__":
    main()
