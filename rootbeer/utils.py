from shutil import rmtree
from distutils import dir_util
import os

from colorama import Fore


def rb_create_path_if_does_not_exist(path: str) -> None:
    """
    Creates a path and it's sub directories if it does not exits. If it does, then it just does nothing.

    :param path: The path to check/create.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def rb_create_and_or_clean_path(path: str) -> None:
    """
    Cleans a path it it exists, and then remakes it. If it does not exist already, then just create it.

    :param path: The path to clean/create.
    """
    if os.path.exists(path):
        rmtree(path)
    os.makedirs(path)


def rb_copy_static_files_to_public_directory(path1: str, path2: str) -> None:
    print(f'{Fore.CYAN}Transfering static files to "{Fore.YELLOW}{path2}/{Fore.CYAN}". . .')
    # Copy all static files (i.e. css/ img/) to the public folder so paths dont break.
    dir_util.copy_tree(f'{path1}/static', path2)
    print(f'{Fore.GREEN}Successfully transfered the static files to "{Fore.YELLOW}{path2}/{Fore.GREEN}"!'
          f'{Fore.RESET}')
