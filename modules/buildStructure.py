import json
import os
import glob
from assets.constants import DIRECTORY_PATTERN, MODIFIED_FILE_PATTERN, CORRECTED_FILE_PATTERN

import logging
from modules.customLogger import CustomFormatter


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def load_json(file_path):
    """
    Load a JSON file from the specified file path.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data, file_path):
    """
    Save a dictionary as a JSON file to the specified file path.

    Args:
        data (dict): The JSON data to be saved.
        file_path (str): The path where the JSON file will be saved.

    Returns:
        None
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent="\t".expandtabs(2))


def create_modified_json():
    """
    Create a blank modified JSON data.

    Returns:
        dict: The modified JSON data.
    """
    modified = {}

    # Add default content to the blank JSON data
    # For example, adding a new key-value pair
    modified["Put modified content here"] = "And let the magic begins"

    return modified


def process_directory(directory, create_mod, quit_flag, delete_modified):
    """
    Process all JSON files in the specified directory.

    Args:
        directory (str): The directory to process.
        create_mod (bool): Flag indicating whether to create modified JSON files.
        quit_flag (bool): Flag indicating whether to quit (delete corrected JSON files).
        delete_modified (bool): Flag indicating whether to delete modified JSON files.

    Returns:
        None
    """
    logger.warning(
      f"\nProcessing directory: {directory}"
    )

    if create_mod:
        # Create modified JSON
        modified_json = create_modified_json()

        # Save the modified JSON as modified.json
        modified_file_path = os.path.join(directory, "modified.json")
        save_json(modified_json, modified_file_path)
        logger.debug(f"Modified JSON saved to {modified_file_path}")

    if quit_flag:
        # Remove any existing corrected.json files
        corrected_files = glob.glob(
          os.path.join(directory, CORRECTED_FILE_PATTERN))
        for corrected_file_path in corrected_files:
            os.remove(corrected_file_path)
            logger.debug(f"Deleted corrected file: {corrected_file_path}")

    if delete_modified:
        # Remove any existing modified.json files
        modified_files = glob.glob(
          os.path.join(directory, MODIFIED_FILE_PATTERN))
        for modified_file_path in modified_files:
            os.remove(modified_file_path)
            logger.warning(f"Deleted modified file: {modified_file_path}")


def main(base_directory, create_mod, quit_flag, delete_modified):
    """
    Main function to process directories matching the DIRECTORY_PATTERN.

    Args:
        base_directory (str): The base directory to start searching for directories.
        create_mod (bool): Flag indicating whether to create modified JSON files.
        quit_flag (bool): Flag indicating whether to quit (delete corrected JSON files).
        delete_modified (bool): Flag indicating whether to delete modified JSON files.

    Returns:
        None
    """
    pattern = os.path.join(base_directory, DIRECTORY_PATTERN)
    directories = glob.glob(pattern)

    for directory in directories:
        if os.path.isdir(directory):
            process_directory(directory, create_mod, quit_flag,
                              delete_modified)
