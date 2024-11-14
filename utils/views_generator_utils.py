import os
import utils.views_converter_utils as views_converter


def convert_dorsals_tiffs_to_other_views(regions_dir, target_dir, view_type):
    """
    Convert dorsal TIFF images to specified views (coronal or sagittal) and save the output.

    Parameters:
    - regions_dir (str): Directory containing the original dorsal TIFF images.
    - target_dir (str): Directory to save the converted TIFF images.
    - view_type (str): The type of view to convert to, either 'coronal' or 'sagittal'.
    """
    # Mapping of view types to corresponding TifOrientationConverter methods
    conversion_methods = {
        "coronal": views_converter.convert_dorsal_tif_to_coronal_tif,
        "sagittal": views_converter.convert_dorsal_tif_to_sagittal_tif,
    }

    # Check if the provided view_type is valid
    if view_type not in conversion_methods:
        raise ValueError(
            f"convert_dorsals_tiffs_to_other_views() ==> Invalid view_type '{view_type}'. Expected 'coronal' or 'sagittal'.")

    # Iterate through the files in the regions_dir
    for region in os.listdir(regions_dir):
        if region.lower().endswith(".tif"):  # Check if the file is a TIFF
            region_name, _ = os.path.splitext(region)
            output_tif_path = os.path.join(target_dir, f"{region_name}_{view_type}.tif")

            # Only process if the output file doesn't already exist
            if not os.path.isfile(output_tif_path):
                tif_dorsal_path = os.path.join(regions_dir, region)
                # Call the appropriate conversion method
                conversion_methods[view_type](tif_dorsal_path, output_tif_path)
