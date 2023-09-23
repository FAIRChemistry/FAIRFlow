from pathlib import Path
from pydantic import BaseModel, PrivateAttr


class Librarian(BaseModel):

    root_directory: Path

    def enumerate_subdirectories(self, subdirectory=None):
        
        directory = self.root_directory
        if subdirectory != None:
            directory = directory / subdirectory
            if not isinstance(directory, Path):
                raise ValueError('Not a valid Path object.')
            if not directory.exists():
                raise ValueError('Directory does not exist.')
        dir_dict = {index: dir for index, dir in enumerate([x for x in directory.iterdir() if x.is_dir()])}
        print(f'Parent directory: \n {directory} \nAvailable subdirectories:')
        for index, dir in dir_dict.items():
            print(f'{index}: /{dir.name}')
        return dir_dict

    def enumerate_files(self, subdirectory=None, filter=None):

        directory = self.root_directory
        if subdirectory != None:
            directory = directory / subdirectory
            if not isinstance(directory, Path):
                raise ValueError('Not a valid Path object.')
            if not directory.exists():
                raise ValueError('Directory does not exist.')
        suffix = '*'
        if filter != None:
            suffix = suffix + '.' + filter
        file_dict = {index: file for index, file in enumerate(directory.glob(suffix)) if file.is_file()}
        print(f'Directory: \n {directory} \nAvailable files:')
        for index, file in file_dict.items():
            print(f'{index}: {file.name}')
        return file_dict
    
    @property
    def get_root_directory(self):
        return self.root_directory

        