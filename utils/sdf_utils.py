import os
import gc
import numpy as np
from scipy import ndimage
from skimage import io
from scipy.ndimage import distance_transform_edt
import utils.tiff_utils as tiff_utils
import utils.file_utils as file_utils


def create_smoothed_boundary(mask_data: np.ndarray, threshold: int = 0) -> np.ndarray:
    """
    Create a smoothed boundary from a binary mask using Signed Distance Function (SDF).

    Parameters:
    - mask_data (np.ndarray): Binary mask data.
    - threshold (int): Threshold to create a binary mask from the smoothed SDF.

    Returns:
    - np.ndarray: Smoothed binary mask.
    """
    binary_mask = (mask_data > 0).astype(np.uint8)  # Convert mask to binary (0s and 1s)
    sdf_inside = ndimage.distance_transform_edt(binary_mask)  # Compute distance transform for the inside
    sdf_outside = ndimage.distance_transform_edt(1 - binary_mask)  # Compute distance transform for the outside
    sdf = sdf_inside - sdf_outside  # Calculate Signed Distance Function (SDF)
    smoothed_sdf = ndimage.gaussian_filter(sdf, sigma=2.0)  # Smooth the SDF with a Gaussian filter
    smoothed_mask = (smoothed_sdf > threshold).astype(np.uint8) * 255  # Create a binary mask from the smoothed SDF
    return smoothed_mask  # Return the smoothed binary mask


def process_and_save_smoothed_boundary(input_directory, output_directory, dtype):
    """
    Process all TIFF files in the input directory, create smoothed boundaries, and save them.

    Parameters:
    - input_directory (str): Directory containing input TIFF files.
    - output_directory (str): Directory to save the processed output files.
    - dtype (np.dtype): Data type for the loaded TIFF images.
    """
    file_utils.remove_all_files(output_directory)
    for tif_region in os.listdir(input_directory):  # Iterate through files in the input directory
        output_tif_path = os.path.join(output_directory, tif_region)  # Construct output file path
        if not os.path.isfile(output_tif_path):  # Check if the output file already exists
            print(
                f"process_and_save_smoothed_boundary() ==> Start smoothing ==> {tif_region}")  # Log the processing start
            tif_path = os.path.join(input_directory, tif_region)  # Construct input file path
            if tif_path.endswith(".tif"):  # Check if the file is a TIFF
                tif_data = tiff_utils.load_tiff_image(tif_path, dtype)  # Load the TIFF data
                smoothed_tif = create_smoothed_boundary(tif_data, threshold=0)  # Create smoothed boundary
                tiff_utils.save_tif_file(output_tif_path, smoothed_tif)  # Save the smoothed boundary
                del tif_data, smoothed_tif  # Delete variables to free memory
                gc.collect()  # Force garbage collection


def fill_2d_image_gaps(image_path, max_distance, output_path):
    """
    Fill gaps between 2D image regions in different gray colors using a signed distance function.
    The algorithm works by computing the Euclidean distance transform for each region in the image.
    It uses these distances to determine the nearest region for each pixel up to a specified maximum distance.
    The gaps within this distance are then filled with the grayscale value of the closest region,
    effectively filling the gaps between regions.
    This process ensures smooth transitions and fills in missing areas in the image based on proximity to existing regions.

    Parameters:
    - image_path: string path to the input 2D TIFF image.
    - max_distance: float, maximum distance to fill gaps.
    - output_path: string path to save the output image.

    Returns:
    - filled_image: np.ndarray, the image with gaps filled up to the specified distance.
    """

    # Load the grayscale TIFF image
    image = tiff_utils.load_image(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Initialize the filled image as a copy of the original
    filled_image = image.copy()

    # Identify unique grayscale values (regions), it will return an array of the colors I have in the image. e.g:[0 103 105 107 109 126 136 138 139 144 145 146 159 161 162 168 169]
    unique_colors = np.unique(image)

    # Creates a new array with the same shape of image and fills it with the value np.inf (infinity), to store the minimum distance to a region for each pixel in the image.
    # All distances are set to infinity because I haven't computed any distances yet. As the algorithm processes each region, it will update this array with the actual minimum distances.
    min_distances = np.full(image.shape, np.inf)

    # Create an array to hold the closest region's value
    closest_values = np.zeros(image.shape, dtype=image.dtype)

    # Loop over the unique_values grayscale colors we have.e.g.[0 103 105 107 109 126 136 138 139 144 145 146 159 161 162 168 169]
    for color_value in unique_colors:
        if color_value == 0:
            continue  # Skip background

        # Create a binary mask for the current region. e.g: if the color is (1) and the image=[1,1,0,0,3,4,5], the mask will be[1,1,0,0,0,0]
        mask = (image == color_value).astype(np.uint8)

        # Compute the distance transform for the current region. The distance transform (Euclidean distance transform) replaces each pixel of a binary image with the distance to the closest background pixel. If the pixel itself is already part of the background then this is 0.
        # e.g:mask = np.array([[0, 0, 0, 0, 0, 0],[0, 1, 1, 0, 0, 0]], dtype=np.uint8)
        # inverted_mask = np.array([[1, 1, 1, 1, 1, 1],[1, 0, 0, 1, 1, 1]], dtype=np.uint8), this is the result of:inverted_mask = 1 - mask
        # The distance_transform_edt function calculates the Euclidean distance transform of the binary image. This means it computes the distance of each pixel to the nearest zero (Current region after inverting).e.g:[1.0, 1.0, 1.0, 1.41421356, 2.0, 2.23606798],[0, 0, 0, 1.0, 2.0, 2.23606798]
        dt = distance_transform_edt(1 - mask)

        # Update minimum distances and closest values
        mask_update = (dt < min_distances) & (dt <= max_distance)
        min_distances[mask_update] = dt[mask_update]
        closest_values[mask_update] = color_value

    # Fill gaps where the original image is background (0) and within max distance
    fill_condition = (image == 0) & (min_distances <= max_distance)
    filled_image[fill_condition] = closest_values[fill_condition]

    # Save the filled image
    io.imsave(output_path, filled_image)


def fill_gaps_in_tif_sequence(sequences_path, max_distance, output_path):
    for img in os.listdir(sequences_path):
        if img.endswith(".tif"):
            print(f"fill_gaps_in_tif_sequence() ==> Start processing 2d tif image named ==> {img}")
            fill_2d_image_gaps(f"{sequences_path}/{img}", max_distance, f"{output_path}/{img}")
