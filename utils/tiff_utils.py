import os
import re
import numpy as np
from skimage import io
import tifffile as tiff
from PIL import Image


def load_tiff_image(datapath, dtype):
    """
    Load a TIFF or image file and return its data as a NumPy array.

    Parameters:
    - datapath (str): Path to the image file.
    - dtype: Desired data type for the returned array.

    Returns:
    - np.ndarray: Loaded image data as a NumPy array, or None if the file is not found.
    """
    if os.path.isfile(datapath):  # Check if the file exists
        img = io.imread(datapath)  # Read the image
        return np.asarray(img, dtype=dtype)  # Convert to NumPy array with specified dtype
    else:
        print(
            f"load_tiff_image() ==> Tif/Image file not found ==> {datapath}")  # Error message if the file is not found
    return None  # Return None if the file does not exist


def load_image(datapath):
    """
        Load an image file using io.imread and return it.

        Parameters:
        - datapath (str): Path to the image file.

        Returns:
        - Loaded image data as returned by io.imread, or None if the file is not found.
        """
    if os.path.isfile(datapath):  # Check if the file exists
        img = io.imread(datapath)  # Read the image
        return img  # Return the loaded image
    else:
        print(f"load_image() ==> Image file not found ==> {datapath}")  # Error message if the file is not found
    return None  # Return None if the file does not exist


def save_tif_file(output_path, tif_data):
    """
    Save the provided data as a TIFF file.

    Parameters:
    - output_path (str): Path where the TIFF file will be saved.
    - tif_data (np.ndarray): Data to be saved in the TIFF file.
    """
    with tiff.TiffWriter(output_path) as tif:  # Open a TIFF writer for the output path
        tif.write(tif_data)  # Write the data to the TIFF file


def save_tiff_stack_as_tif_image_sequences(tif_path, output_path):
    """
    Save each page of a multi-page TIFF file as separate TIFF images.

    Parameters:
    - tif_path (str): Path to the multi-page TIFF file.
    - output_path (str): Directory to save individual TIFF images.
    """
    with tiff.TiffFile(tif_path) as tif:
        for i, page in enumerate(tif.pages):  # Iterate through each page in the TIFF file
            image = page.asarray()  # Convert the page to a NumPy array
            output_img_path = f'{output_path}/{i}.tif'  # Create output path for the individual TIFF
            tiff.imwrite(output_img_path, image)  # Save the individual page as a TIFF file


def save_tif_sequences_to_tiff_stack(input_path, output_tiff):
    """
    Save a sequence of 2D TIFF images as a TIFF stack.
    input_directory: Should contain a sequence of images named numerically, such as "1.tif, 2.tif, 3.tif, ...".
    """

    # Function to extract numbers from filenames for proper numerical sorting
    def numerical_sort(filename):
        # Extract numbers from the filename
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else float('inf')

    # List and sort TIFF files numerically
    tiff_images = sorted([f for f in os.listdir(input_path) if f.lower().endswith('.tif')],
                         key=numerical_sort)

    # Load images into a list
    images = []
    for file in tiff_images:
        img_path = os.path.join(input_path, file)
        with Image.open(img_path) as img:
            images.append(np.array(img))  # Convert to NumPy array

    # Convert list of images to a 3D NumPy array
    image_stack = np.stack(images)

    tiff.imwrite(output_tiff, image_stack, photometric='minisblack')

    print(f'convert_tif_sequences_to_tiff_stack() ==> Successfully saved TIFF stack to {output_tiff}')


def normalize_stack(tif_data):
    normalized_result = (tif_data > 0).astype(np.uint8)  # Normalize the binary mask to [0, 1]
    normalized_result *= 255
    return normalized_result


def merge_8bit_grayscale_tif_files(output_path, tiffs_path, color_values=None):
    """
    Merge multiple 8-bit grayscale TIFF files into a single TIFF file.

    Parameters:
    - output_path (str): Path to save the merged TIFF file.
    - tiffs_path (list): List of paths to the TIFF files to merge.
    - color_values (list): List of color values to apply to the corresponding masks; if None, defaults to 255.
    """
    image = load_image(tiffs_path[0])  # Read the first TIFF file to get the shape
    tiff_stack_data = np.zeros(image.shape, dtype=image.dtype)  # Initialize an array for the merged data
    if color_values is None:  # If no color values provided
        color_values = [None] * len(tiffs_path)  # Create a list of None values
    # Iterate through each TIFF file and corresponding color
    for region_path, color_value in zip(tiffs_path, color_values):
        if os.path.isfile(region_path):  # Check if the file exists
            print(
                f"merge_8bit_grayscale_tif_files() ==> Start merging ==> {os.path.basename(region_path)}")  # Log the merging process
            mask_data = tiff.imread(region_path)  # Read the mask data from the TIFF file
            #  stack and merge binary masks from the TIFF images into a single output image, and set the corresponding color pixels
            tiff_stack_data[mask_data != 0] = color_value if color_value is not None else 255

    tiff.imwrite(output_path, tiff_stack_data)  # Save the merged data as a new TIFF file


def extract_8bit_grayscale_tif_files(combined_tiff, colors, color_to_region_dic, output_path):
    """
    Extracts regions from a grayscale TIFF image based on specified color values[100 to 255] and saves them as separate binary masks.

    Parameters:
        combined_tiff (str): Path to the combined grayscale TIFF image.
        colors (list of int): List of color values [100 to 255] representing distinct regions to extract.
        color_to_region_dic (dict): Dictionary mapping color values to regions names.
        output_path (str): Directory path where the binary masks will be saved.

    Returns:
        None
    """

    # Read the combined grayscale TIFF image
    try:
        combined_image = tiff.imread(combined_tiff)
    except Exception as e:
        print(f"Error reading the TIFF file: {e}")
        return

    # Iterate through the provided color values
    for color_value in colors:
        #  Initialize a binary mask with the same dimensions as the combined image
        binary_mask = np.zeros_like(combined_image, dtype=np.uint8)
        # Set pixels in the mask to 255 where the color value matches
        binary_mask[combined_image == color_value] = 255
        # Construct the file path for saving the binary mask
        region_name = color_to_region_dic[color_value]
        tif_file_path = f"{output_path}/{region_name}"
        # Save the binary mask as a separate TIFF file
        # tiff.imwrite(tif_file_path, binary_mask)
        save_tif_file(tif_file_path, binary_mask)
        print(f"Extract a region from the combined TIFF stack: ===> {tif_file_path}")
