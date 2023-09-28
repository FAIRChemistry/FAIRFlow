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

    def enumerate_subdirectories(self, directory: Path):
        dir_dict = {
            index: dir
            for index, dir in enumerate(
                [x for x in directory.iterdir() if x.is_dir()]
            )
        }
        print(f"Parent directory: \n {directory} \nAvailable subdirectories:")
        for index, dir in dir_dict.items():
            print(f"{index}: .../{dir.name}")

        # directory = self.root_directory
        # if directory:
        #     directory = directory / subdirectory
        #     if not isinstance(directory, Path):
        #         raise ValueError('Not a valid Path object.')
        #     if not directory.exists():
        #         raise ValueError('Directory does not exist.')

        return dir_dict

    def enumerate_files(
        self,
        directory: Path | List[Path],
        indices: List[int] = None,
        filter: str = None,
    ):
        """
        Directory is set to the root directory.
        If subdirectories are passed: Build corresponding paths by appending
        the subdirectory extension to the root directory and append them to
        the directories list.
        Else: append root directory to the directories list.
        If no value is passed for filter, all file types will be considered.
        """
        # directory = self.root_directory
        # directories = []
        # if subdirectories != None:
        #     for subdirectory in subdirectories:
        #         directories.append(directory / subdirectory)
        # else:
        #     directories.append(directory)
        suffix = "*"
        if filter != None:
            suffix = suffix + "." + filter
        # file_list = []
        # for directory in directories:
        #     files_in_directory = [file for file in directory.glob(suffix) if file.is_file()]
        #     file_list.extend(files_in_directory)
        # file_dict = {index: file for index, file in enumerate(file_list)}

        file_dict = {
            index: file
            for index, file in enumerate(directory.glob(suffix))
            if file.is_file()
        }
        print(f"Directory: \n {directory} \nAvailable files:")
        for index, file in file_dict.items():
            print(f"{index}: {file.name}")
        return file_dict

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
