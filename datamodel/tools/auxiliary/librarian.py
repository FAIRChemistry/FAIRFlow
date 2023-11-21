import logging
from pathlib import Path
from pydantic import BaseModel, PrivateAttr
from typing import List

logger = logging.getLogger(__name__)
logger.propagate = True


class DirectoryNotFoundError(Exception):
    def __init__(self, directory):
        super().__init__(f"Directory not found: {directory}")


class Librarian(BaseModel):
    root_directory: Path

    def enumerate_subdirectories(self, directory: Path, verbose: bool = None):
        dir_dict = {
            index: dir
            for index, dir in enumerate(
                [x for x in directory.iterdir() if x.is_dir()]
            )
        }
        if verbose:
            print(f"Parent directory: \n {directory} \nAvailable subdirectories:")
            for index, dir in dir_dict.items():
                print(f"{index}: .../{dir.name}")

        return dir_dict

    def enumerate_files(
        self,
        directory: Path | List[Path],
        indices: List[int] = None,
        filter: str = None,
        verbose: bool = None
    ):
        """
        Directory is set to the root directory.
        If no value is passed for filter, all file types will be considered.
        """

        suffix = "*." + filter if filter != None else "*"

        file_dict = {
            index: file
            for index, file in enumerate(directory.glob(suffix))
            if file.is_file()
        }
        if verbose: 
            print(f"Directory: \n {directory} \nAvailable files:")
            for index, file in file_dict.items():
                print(f"{index}: {file.name}")

        return file_dict

    def search_files_in_subdirectory(self,root_directory: Path, directory_keys: list[str], file_filter: str, verbose: bool = None) -> Path:
        """
        Function that loobs through Path objects containing a main directory. In this directory it is recoursevly searched for sub directories. 
        In the last sub directory files with the suffix 'file_filter' are searched and returned

        Args:
            root_directory (Path): Root directory
            directory_keys (list[str]): List of subdirectories that should be recoursevly searched
            file_filter (str): Suffix of files that should be found in last given sub directory
            verbose (bool, optional): Possiblity to printout all subdirectories in each directory listed. Defaults to None.

        Raises:
            KeyError: If either the specified sub directory or file could not be found

        Returns:
            subdirectory_files (Path): Path object containing all files found in the subdirectory
        """

        # First search for every nested sub directory in provided root directory #
        
        root = self.enumerate_subdirectories(root_directory)
        for j,directory_key in enumerate(directory_keys):
            try:
                idx_sub_directory = [i for i in range(len(root)) if root[i].parts[-1] == directory_key ][0]
                if j < len(directory_keys)-1: 
                    root          = self.enumerate_subdirectories(directory=root[idx_sub_directory])
            except:
                raise KeyError("Defined key: '%s' cannot be found in the given root directory: %s"%(directory_key,root[0].parent))

        # Search for all files that match the given filter in the specified sub directory #
        subdirectory_files = self.enumerate_files(directory=root[idx_sub_directory], filter=file_filter, verbose=verbose)   
        if not bool(subdirectory_files): 
            raise KeyError("No files with filter: '%s' found in the given sub directory: %s"%(file_filter,root_directory[idx_sub_directory]))
        
        return subdirectory_files


    def visualize_directory_tree(
        self, directory: Path, indent=0, skip_directories=None
    ):
        if skip_directories is None:
            skip_directories = []

        if directory.is_dir():
            if directory.name in skip_directories:
                return

            print("  " * indent + f"[{directory.name}]")

            for item in directory.iterdir():
                if item.is_dir():
                    self.visualize_directory_tree(
                        item, indent + 1, skip_directories
                    )
                else:
                    print("  " * (indent + 1) + item.name)
        else:
            print("Directory not found.")

    @property
    def get_root_directory(self):
        return self.root_directory
