import os
import shutil
from pathlib import Path


def get_list_files(*, folder_name: str) -> list[str]:
    path: str = str(Path(Path.cwd(), 'files', folder_name))
    return os.listdir(path)


def get_paths_to_files(*, folder_name: str) -> list[str]:
    files: list[str] = get_list_files(folder_name=folder_name)
    return [str(Path(Path.cwd(), 'files', folder_name, file)) for file in files]


def copy_file_to_files(*, copy_from: str, copy_to: str):
    copy_to: str = f'{Path(Path.cwd(), "files", copy_to)}'
    shutil.copy2(copy_from, copy_to)
