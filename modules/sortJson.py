import json
import copy
import os
import glob
from assets.constants import ORIGINAL_FILE_PATTERN, DIRECTORY_PATTERN, MODIFIED_FILE_PATTERN, FORMATS
from typing import Dict, Any

import logging
from modules.customLogger import CustomFormatter


# Custom logger which help to identifie log level and an error message
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file from the specified file path.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data: Dict[str, Any], file_path: str) -> None:
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


def compare_and_correct(original: Dict[str, Any],
                        modified: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare and correct the structure of the modified JSON to match the original JSON.

    Args:
        original (dict): The original JSON data.
        modified (dict): The modified JSON data.

    Returns:
        dict: The corrected JSON data.
    """
    corrected = copy.deepcopy(modified)

    def correct_structure(orig: Dict[str, Any],
                          mod: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively correct the structure of the modified JSON to match the original JSON.

        Args:
            orig (dict or list): The original JSON data.
            mod (dict or list): The modified JSON data.

        Returns:
            dict or list: The corrected structure.
        """
        if isinstance(orig, dict):
            for key in orig:
                if key in mod:
                    mod[key] = correct_structure(orig[key], mod[key])
                else:
                    mod[key] = orig[key]
            # Ensure the "variables" key maintains the same order and handle descriptions
            if "variables" in orig and "variables" in mod:
                orig_vars = orig["variables"]
                mod_vars = {
                  var["properties"]["name"]: var
                  for var in mod["variables"]
                  if "properties" in var and "name" in var["properties"]
                }
                corrected_vars = []
                for var in orig_vars:
                    if "properties" in var and "name" in var["properties"]:
                        var_name = var["properties"]["name"]
                        if var_name in mod_vars:
                            corrected_var = mod_vars[var_name]
                            # Retain the description from the original if it exists
                            if "description" in var["properties"]:
                                corrected_var["properties"][
                                  "description"] = var["properties"][
                                    "description"]
                            elif "description" in corrected_var["properties"]:
                                del corrected_var["properties"]["description"]
                            corrected_vars.append(corrected_var)
                mod["variables"] = corrected_vars
        elif isinstance(orig, list):
            if len(orig) > 0 and isinstance(orig[0], dict):
                for i, item in enumerate(orig):
                    if i < len(mod):
                        mod[i] = correct_structure(item, mod[i])
                    else:
                        mod.append(item)
        return mod

    def check_variable_string_format(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check and update the variable_string_format in the JSON data.

        Args:
            data (dict): The JSON data to check and update.

        Returns:
            dict: The updated JSON data with variable_string_format checked.
        """
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value,
                              dict) and "variable_string_format" in value:
                    # TODO: Maybe need to add datatype.large_string
                    if value["type"] == "datatype.string":
                        if value["variable_string_format"] not in FORMATS:
                            value["variable_string_format"] = "text"
                else:
                    check_variable_string_format(value)
        elif isinstance(data, list):
            for item in data:
                check_variable_string_format(item)
        return data

    corrected = correct_structure(original, corrected)
    corrected = check_variable_string_format(corrected)

    # Ensure name, title, and display_name are copied from modified to corrected
    if "workflow" in modified:
        if "workflow" not in corrected or not isinstance(
          corrected["workflow"], dict):
            corrected["workflow"] = {}
        for key in ["name", "title", "display_name"]:
            if key in modified["workflow"]:
                corrected["workflow"][key] = modified["workflow"][key]

    return corrected


def process_directory(directory: str, save_corrected: bool) -> None:
    """
    Process all JSON files in the specified directory.

    Args:
        directory (str): The directory to process.
        save_corrected (bool): Flag indicating whether to save the corrected JSON files.

    Returns:
        None
    """
    logger.info(
      f"\nProcessing directory: {directory}"
    )
    original_files = glob.glob(os.path.join(directory, ORIGINAL_FILE_PATTERN))

    if not original_files:
        logger.error(f"No original JSON files found in {directory}")
        return

    for original_file_path in original_files:
        # logger.info(f"Original file found: {original_file_path}")

        original_json = load_json(original_file_path)
        modified_files = glob.glob(
          os.path.join(directory, MODIFIED_FILE_PATTERN))

        for modified_file_path in modified_files:
            # logger.warning(f"Processing modified file: {modified_file_path}")
            try:
                modified_json = load_json(modified_file_path)
            except json.JSONDecodeError:
                logger.error(
                  f"Error: {modified_file_path} is not a valid JSON file or is empty. Skipping."
                )
                continue
            except FileNotFoundError:
                logger.error(f"Modified file not found: {modified_file_path}")
                continue

            corrected_json = compare_and_correct(original_json, modified_json)

            if save_corrected:
                # Create a new filename for the corrected version
                corrected_file_path = modified_file_path.replace(
                  "modified", "corrected")
                save_json(corrected_json, corrected_file_path)
                logger.debug(f"Corrected JSON saved to {corrected_file_path}")
            else:
                # Save the corrected JSON back to the original file
                save_json(corrected_json, original_file_path)
                # logger.info(f"Original JSON updated with corrected data: {original_file_path}")

            # Log the date and time when the processing is finished
            logger.warning(f"Processing of {modified_file_path} completed")

            # Delete the modified file
            os.remove(modified_file_path)
            # logger.warning(f"Deleted modified file: {modified_file_path}")


def main(base_directory: str, save_corrected: bool) -> None:
    """
    Main function to process directories matching the DIRECTORY_PATTERN.

    Args:
        base_directory (str): The base directory to start searching for directories.
        save_corrected (bool): Flag indicating whether to save the corrected JSON files.

    Returns:
        None
    """
    pattern = os.path.join(base_directory, DIRECTORY_PATTERN)
    directories = glob.glob(pattern)

    for directory in directories:
        if os.path.isdir(directory):
            process_directory(directory, save_corrected)
