import os

from etl.core import EtlEnvironment
from etl.steps import BaseEtlStep
from etl.sys import SysFolderType


class CheckForInboxFiles(BaseEtlStep):
    name = "001_check_for_inbox_files"

    def run(self, env: EtlEnvironment):
        # Determine the inbox directory path from the environment
        inbox_dir = env.get_folder_path(SysFolderType.INBOX)

        # Gather list of regular files in the inbox directory
        try:
            entries = os.listdir(inbox_dir)
        except FileNotFoundError:
            files = []
        else:
            files = [e for e in entries if os.path.isfile(os.path.join(inbox_dir, e))]

        # Print file names, or a message if none are found
        if files:
            for fname in files:
                print(fname)
        else:
            print("No files found")
