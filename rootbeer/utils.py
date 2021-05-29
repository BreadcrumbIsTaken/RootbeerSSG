from shutil import rmtree
from distutils import dir_util
from subprocess import check_call, DEVNULL
from sys import executable
from typing import KeysView
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

    :return: None
    """
    if os.path.exists(path):
        rmtree(path)
    os.makedirs(path)


def rb_copy_static_files_to_public_directory(path1: str, path2: str, log_steps: bool) -> None:
    """
    Transfers the files from a static folder to another folder.

    :param path1: The static folder path.
    :param path2: The output folder path.
    :param log_steps: Weither to log the steps.

    :return: None
    """
    if log_steps:
        print(f'{Fore.CYAN}Transfering static files to "{Fore.YELLOW}{path2}/{Fore.CYAN}". . .')
    # Copy all static files (i.e. css/ img/) to the public folder so paths dont break.
    dir_util.copy_tree(f'{path1}/static', path2)
    if log_steps:
        print(f'{Fore.GREEN}Successfully transfered the static files to "{Fore.YELLOW}{path2}/{Fore.GREEN}"!'
              f'{Fore.RESET}')


def rb_install_markdown_extras_modules(modules_to_install: KeysView[str]) -> None:
    """
    Installs all mardown extnetions.

    :param modules_to_install: The modules to install.

    :return: None
    """
    install_command: list = [executable, '-m', 'pip', 'install']
    for module in modules_to_install:
        install_command.append(module)
    check_call(install_command, stdout=DEVNULL)