import numpy as np
import utils.tiff_utils as tiff_utils


def transpose_tif(tif_data, tiff_type):
    # Initialize an array to store the transposed slices. Original access pattern is (z, y, x), but we are using (z, x, y) instead.
    transposed_slices = np.zeros((tif_data.shape[0], tif_data.shape[2], tif_data.shape[1]), dtype=tiff_type)

    # Transpose each slice of the 3D array
    for i in range(tif_data.shape[0]):
        transposed_slices[i] = tif_data[i].transpose()

    # Convert to a supported bit depth (8-bit integers)
    transposed_slices = transposed_slices.astype(tiff_type)

    return transposed_slices


def convert_dorsal_tif_to_coronal_tif(tif_file_path, output_tif_path):
    tif_file_data = tiff_utils.load_tiff_image(tif_file_path, np.uint8)
    coronal_tif_data = np.rot90(tif_file_data, k=3, axes=(0, 1))
    tiff_utils.save_tif_file(output_tif_path, coronal_tif_data)


def convert_dorsal_tif_to_sagittal_tif(tif_file_path, output_tif_path):
    tif_file_data = tiff_utils.load_tiff_image(tif_file_path, np.uint8)
    # Rotate the entire 3D array to change from dorsal to sagittal view
    sagittal_tif_data = np.rot90(tif_file_data, k=3, axes=(0, 2))
    tiff_utils.save_tif_file(output_tif_path, transpose_tif(sagittal_tif_data, np.uint8))


def convert_sagittal_tif_to_coronal_tif(tif_file_path, output_tif_path):
    tif_file_data = tiff_utils.load_tiff_image(tif_file_path, np.uint8)
    coronal_tif_data = np.rot90(tif_file_data, k=3, axes=(0, 2))
    coronal_tif_data = np.flip(coronal_tif_data, axis=2)  # Flip coronal view along axis 2(z)
    tiff_utils.save_tif_file(output_tif_path, coronal_tif_data)


def convert_sagittal_tif_to_dorsal_tif(tif_file_path, output_tif_path):
    tif_file_data = tiff_utils.load_tiff_image(tif_file_path, np.uint8)
    # Rotate the entire 3D array to change from dorsal to sagittal view
    dorsal_tif_data = np.rot90(tif_file_data, k=1, axes=(0, 1))
    tiff_utils.save_tif_file(output_tif_path, transpose_tif(dorsal_tif_data, np.uint8))


def convert_coronal_tif_to_dorsal_tif(tif_file_path, output_tif_path):
    tif_file_data = tiff_utils.load_tiff_image(tif_file_path, np.uint8)
    # Rotate the 3D array from coronal to dorsal view
    dorsal_tif_data = np.rot90(tif_file_data, k=-3, axes=(0, 1))
    tiff_utils.save_tif_file(output_tif_path, dorsal_tif_data)


def convert_coronal_tif_to_sagittal_tif(tif_file_path, output_tif_path):
    tif_file_data = tiff_utils.load_tiff_image(tif_file_path, np.uint8)
    # Rotate the 3D array from coronal to sagittal view
    sagittal_tif_data = np.rot90(tif_file_data, k=3, axes=(0, 2))
    # Optionally, flip along the appropriate axis to correct the orientation
    sagittal_tif_data = np.flip(sagittal_tif_data, axis=2)
    tiff_utils.save_tif_file(output_tif_path, sagittal_tif_data)
