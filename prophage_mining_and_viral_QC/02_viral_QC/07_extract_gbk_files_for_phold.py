#!/usr/bin/env python3

"""
Script to collect pharokka.gbk files from pharokka_* directories,
rename by removing the 'pharokka_' prefix, and copy to the 'gbk_files' folder.
"""

import shutil
from pathlib import Path


def main():
    # Set the base directory to where this script is located
    base = Path(__file__).parent.resolve()
    # Define the target directory
    target = base / 'gbk_files'
    # Create target directory if it doesn't exist
    target.mkdir(exist_ok=True)

    # Iterate over all items in the base directory
    for folder in base.iterdir():
        # Process only directories starting with 'pharokka_'
        if folder.is_dir() and folder.name.startswith('pharokka_'):
            source_gbk = folder / 'pharokka.gbk'
            if source_gbk.is_file():
                # Construct new filename by stripping the prefix
                new_name = folder.name[len('pharokka_'):] + '.gbk'
                dest = target / new_name
                # Copy the file
                shutil.copy2(source_gbk, dest)
                print(f"Copied {source_gbk} to {dest}")
            else:
                print(f"Warning: {source_gbk} not found, skipped.")


if __name__ == '__main__':
    main()
