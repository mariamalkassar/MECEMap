import os
from pathlib import Path


def remove_file(file_path):
    """
    Remove a file if it exists.

    Parameters:
    - file_path (str or Path): The path of the file to be removed.
    """
    file_path = Path(file_path)  # Convert to Path object

    if file_path.is_file():
        try:
            file_path.unlink()  # Remove the file
            print(f'Successfully removed file: {file_path}')
        except Exception as e:
            print(f'Error removing file {file_path}: {e}')
    else:
        print(f'File not found: {file_path}')


def remove_all_files(directory_path):
    """
    Remove all files in the specified directory.

    Parameters:
    - directory_path (str): The path of the directory containing files to be removed.
    """
    if os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


def parse_anatomical_structures_txt_file(txt_file_path, regions_path):
    """
    Parse a txt file containing anatomical structures and colors.

    Parameters:
    - txt_file_path (str): Path to the text file.
    - regions_path (str): Path where input files are stored.
    - type (str): Type of anatomical structure.
    - flat_hierarchy (bool): Whether to use a flat hierarchy structure.

    Returns:
    - list, list, dict: Tif paths, color values, and MECE regions dictionary.
    """
    tif_paths = []
    color_values = []
    color_to_region_map = {}

    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            region_name, color = line.strip().split('|')
            tif_paths.append(os.path.join(regions_path, region_name))
            color_values.append(int(color))
            color_to_region_map[int(color)] = region_name

    return tif_paths, color_values, color_to_region_map
