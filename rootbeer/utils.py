from shutil import rmtree
import os


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
