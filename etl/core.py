import os
from .sys import SysFolderType


class EtlEnvironment:
    def __init__(self, sys_root="."):
        self.sys_root = sys_root

    """
    Manages the ETL environment setup and configuration.

    This class handles the creation and management of necessary system folders
    for ETL operations.
    """

    def check_folders(self):
        """
        Checks and ensures the existence of specific system folders defined by `SysFolderType`.
        Iterates through all folder types enumerated in `SysFolderType`, constructs their paths
        relative to a system root directory, and creates any missing folders.

        :param self: Instance reference to access the `sys_root` attribute.

        :raises OSError: If there is an issue creating a directory, such as insufficient
            permissions or invalid name.

        """
        for folder_type in SysFolderType:
            folder_path = os.path.join(self.sys_root, folder_type.value)
            print(f"Folder={folder_type.name} Path={folder_path}")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def get_folder_path(self, folder_type: SysFolderType) -> str:
        """
        Returns the absolute path for a specified system folder type.

        :param folder_type: The type of system folder to get the path for.
        :type folder_type: SysFolderType
        :return: The absolute path to the specified system folder.
        :rtype: str
        """
        return os.path.join(self.sys_root, folder_type.value)
