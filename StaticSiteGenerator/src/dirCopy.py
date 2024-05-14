import logging
import os
import shutil

logging.basicConfig(level=logging.DEBUG)


def copy_dirs(from_directory: str, to_directory: str) -> None:
    """Simpler version of shutil.copytree

    Args:
        from_directory (str): path to directory from which to copy files
        to_directory (str): path to directory to where to copy files
    """

    from_directory_path = os.path.join(os.getcwd(), from_directory)
    to_directory_path = os.path.join(os.getcwd(), to_directory)

    manage_dirs(from_directory, to_directory)
    copy_files_recursive(from_directory_path, to_directory_path)


def manage_dirs(from_directory_path: str, to_directory_path: str) -> None:
    """Creates destination directory, or clears it before usage

    Raises:
        ValueError: From Directory doesn't exist
    """
    if not os.path.exists(from_directory_path):
        raise ValueError(f"{from_directory_path} directory doesn't exist")

    if os.path.exists(to_directory_path):
        logging.info(f"{to_directory_path} exists, cleaning it")

        remove_contents(to_directory_path)
    else:
        logging.info(f"{to_directory_path} doesn't exist, creating it...")

        os.mkdir(to_directory_path)


def remove_contents(directory_path: str) -> None:
    """Deletes file from the directory"""
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                logging.debug(f"Removing file {filename}")
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                logging.debug(f"Removing directory {filename}")
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def copy_files_recursive(from_directory_path: str, to_directory_path: str) -> None:
    if not os.path.exists(to_directory_path):
        os.mkdir(to_directory_path)

    for filename in os.listdir(from_directory_path):
        file_path = os.path.join(from_directory_path, filename)
        destination_path = os.path.join(to_directory_path, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                logging.debug(f"Copying {filename} to {to_directory_path}")
                shutil.copy(file_path, destination_path)
            elif os.path.isdir(file_path):
                logging.debug(f"Copying {filename} dir to {to_directory_path} recursively...")
                copy_files_recursive(file_path, destination_path)
        except Exception as e:
            print("Failed to copy %s. Reason: %s" % (file_path, e))
