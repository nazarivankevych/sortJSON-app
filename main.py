import sys
import os
import argparse
import modules.sortJson as sortJson
import modules.buildStructure as modifiedJson
from assets.constants import BASE_DIRECTORY

# Add the root directory of the project to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    parser = argparse.ArgumentParser(
      description="Main script to handle JSON processing.")
    parser.add_argument(
      "base_directory",
      type=str,
      nargs="?",
      default=BASE_DIRECTORY,
      help="Base directory to start searching for directories",
    )
    parser.add_argument(
      "--mod",
      action="store_true",
      help="Flag to create modified JSON files",
    )
    parser.add_argument(
      "--quit",
      action="store_true",
      help="Flag to delete corrected JSON files",
    )
    parser.add_argument(
      "--no-mod",
      action="store_true",
      help="Flag to delete modified JSON files",
    )
    parser.add_argument(
      "--save",
      action="store_true",
      help="Flag to save the corrected JSON files after processing",
    )
    parser.add_argument(
      "--no-save",
      action="store_true",
      help="Flag to merge modified JSON files into the original JSON files",
    )

    args = parser.parse_args()

    if args.mod or args.quit or args.no_mod:
        modifiedJson.main(args.base_directory, args.mod, args.quit,
                          args.no_mod)

    if args.save:
        sortJson.main(args.base_directory, args.save)

    if args.no_save:
        # Use sortJson.main with save_corrected set to False
        sortJson.main(args.base_directory, False)


if __name__ == "__main__":
    main()
