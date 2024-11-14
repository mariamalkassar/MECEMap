import utils.file_utils as file_utils
import utils.sdf_utils as sdf_utils
import utils.views_generator_utils as views_generator
import utils.tiff_utils as tiff_utils
from pathlib import Path

PATH__REGIONS__ROOT = "/Users/mimi/MaxPlanck/mapzebrain/server/media/NewRegions"

def start_MECEing_kunst_regions():
    """Apply MECE processing to anatomical regions and generate various views."""

    # Base directories
    base_directory = Path(PATH__REGIONS__ROOT) / "Paper_SDF_results"
    leaves_regions_dir = base_directory / "1_leaves_regions"
    smoothed_leaves_regions_dir = base_directory / "2_smoothed_leaves_regions"
    anatomical_structures_txt_path = base_directory / "0_anatomical_structures_list/anatomical_structures_list.txt"

    # Step A: Process and save smoothed boundaries (if needed)
    # sdf_utils.process_and_save_smoothed_boundary(leaves_regions_dir, smoothed_leaves_regions_dir, np.uint8)

    # Step B: Create a combined 8-bit grayscale TIFF file
    smoothed_leaves_tif_path = base_directory / "2_smoothed_leaves_regions.tif"
    file_utils.remove_file(smoothed_leaves_tif_path)

    tif_paths, colors, _ = file_utils.parse_anatomical_structures_txt_file(
        anatomical_structures_txt_path, smoothed_leaves_regions_dir
    )
    tiff_utils.merge_8bit_grayscale_tif_files(smoothed_leaves_tif_path, tif_paths, colors)

    # Step C: Save TIFF stack as individual image sequences
    images_sequences_dir = base_directory / "3_images_sequences"
    file_utils.remove_all_files(images_sequences_dir)
    tiff_utils.save_tiff_stack_as_tif_image_sequences(smoothed_leaves_tif_path, images_sequences_dir)

    # Step D: Fill gaps in the image sequence using MECE method
    max_distance = 8  # Distance parameter for gap filling
    mece_sequences_dir = base_directory / "4_images_sequences__MECE"
    file_utils.remove_all_files(mece_sequences_dir)
    sdf_utils.fill_gaps_in_tif_sequence(images_sequences_dir, max_distance, mece_sequences_dir)

    # Step E: Save MECE-processed sequences as a TIFF stack
    mece_regions_stack_path = base_directory / "4_mece_regions_stack.tif"
    file_utils.remove_file(mece_regions_stack_path)
    tiff_utils.save_tif_sequences_to_tiff_stack(mece_sequences_dir, mece_regions_stack_path)

    # Step F: Extract individual regions from the MECE regions stack
    extracted_regions_dir = base_directory / "5_dorsal_regions"
    file_utils.remove_all_files(extracted_regions_dir)

    _, colors, regions_dict = file_utils.parse_anatomical_structures_txt_file(
        anatomical_structures_txt_path, ""
    )
    tiff_utils.extract_8bit_grayscale_tif_files(mece_regions_stack_path, colors, regions_dict, extracted_regions_dir)

    # Step F: Extract individual regions from the MECE regions stack
    extracted_regions_dir = base_directory / "5_dorsal_regions"
    file_utils.remove_all_files(extracted_regions_dir)

    _, colors, regions_dict = file_utils.parse_anatomical_structures_txt_file(
        anatomical_structures_txt_path, ""
    )
    tiff_utils.extract_8bit_grayscale_tif_files(mece_regions_stack_path, colors, regions_dict, extracted_regions_dir)

    # Step G: Convert dorsal regions to coronal views
    coronal_regions_dir = base_directory / "6_coronal_regions"
    file_utils.remove_all_files(coronal_regions_dir)
    views_generator.convert_dorsals_tiffs_to_other_views(extracted_regions_dir, coronal_regions_dir, "coronal")

    # Step H: Convert dorsal regions to sagittal views
    sagittal_regions_dir = base_directory / "7_sagittal_regions"
    file_utils.remove_all_files(sagittal_regions_dir)
    views_generator.convert_dorsals_tiffs_to_other_views(extracted_regions_dir, sagittal_regions_dir, "sagittal")


if __name__ == '__main__':
    start_MECEing_kunst_regions()
