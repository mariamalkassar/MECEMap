# MECE Kunst Regions Processor

This project provides a Python-based pipeline for processing anatomical region data using the MECE method (Mutually Exclusive Collectively Exhaustive). 
The pipeline processes anatomical regions, smooths boundaries, fills gaps, and generates orthogonal views (dorsal, coronal, and sagittal) for anatomical visualization and analysis.

---

# Features
The script automates the processing of anatomical region datasets through the following steps:
1. Smooths boundaries of DORSAL regions using 3D Signed Distance Function (SDF):
The original TIFFs had jagged edges due to slight variations across frames. This step ensures smooth transitions and prepares the data for further processing.

2. Combines regions into a single 8-bit grayscale leaves TIFF file (69 regions):
Each anatomical region is assigned a specific grayscale value from 0 to 255, consolidating all regions into one file for easier management.

3. Gap filling using Signed Distance Function (SDF):
This step fills gaps in the anatomical region images, ensuring continuity across the data sequence.

3. Extraction of MECE leaves regions:
After processing, MECE Leaves regions are extracted and saved into separate TIFF files stacks.

4. Generation of orthogonal views:
The processed dorsal regions are converted into coronal and sagittal views for comprehensive visualization.

---

# Installation
Make sure you have the following installed:
1. Python 3.10 
2. Required Python packages (listed in requirements.txt if available)

# Setup
1. Clone the repository:

`git clone https://github.com/mariamalkassar/MECEMap.git
cd mece-kunst-regions-processor`

2. Install dependencies:

`pip install -r requirements.txt`

3. Update the base_directory path in the script to point to your dataset's base directory:

`base_directory = Path("/path/to/your/base/regions/directory")`

---

# Usage
To run the processing pipeline, simply execute the script:


`
cd /To/Your/MECEMap/Directory
python3 -m anatomical_regions_mece
`
The pipeline will perform the following steps:
1. Smooth boundaries: Processes raw TIFF files in the 1_leaves_regions directory and outputs smoothed TIFF files in 2_smoothed_leaves_regions.
2. Combine TIFFs: Creates a combined 8-bit grayscale TIFF file for all regions and saves it as 2_smoothed_leaves_regions.tif.
3. Save TIFF stack as image sequences: Converts the combined TIFF file into individual 2d TIFF image sequences in the 3_images_sequences directory.
4. Fill gaps: Fills gaps in the image sequences using a signed distance function and saves the results in 4_images_sequences__MECE.
5. Save MECE results as a TIFF stack: Merges the gap-filled sequences into a TIFF stack, saved as 4_mece_regions_stack.tif.
6. Extract MECE regions: Splits the TIFF stack into individual regions, saved in 5_dorsal_regions.
7. Generate coronal and sagittal views: Converts dorsal regions into coronal views (saved in 6_coronal_regions) and sagittal views (saved in 7_sagittal_regions).

---

# Directory Structure
Expected directory structure for the input dataset:

```
/path/to/your/base/regions/directory
├── 0_anatomical_structures_list/
│   └── anatomical_structures_list.txt
├── 1_leaves_regions/
│   ├── region_stack_1.tif
│   ├── region_stack_2.tif
│   └── ...
```
Output directories:

```
/path/to/your/base/regions/directory
├── 2_smoothed_leaves_regions/
│   ├── region_stack_1.tif
│   ├── region_stack_2.tif
│   └── ...
├── 3_images_sequences/
│   ├── 2D_tif_sequence_1.tif
│   ├── 2D_tif_sequence_2.tif
│   └── ...
├── 4_images_sequences__MECE/
│   ├── 2D_tif_sequence_1.tif
│   ├── 2D_tif_sequence_2.tif
│   └── ...
├── 5_dorsal_regions/
│   ├── dorsal_region_stack_1.tif
│   ├── dorsal_region_stack_2.tif
│   └── ...
├── 6_coronal_regions/
│   ├── coronal_region_stack_1.tif
│   ├── coronal_region_stack_2.tif
│   └── ...
├── 7_sagittal_regions/
│   ├── sagittal_region_stack_1.tif
│   ├── sagittal_region_stack_2.tif
│   └── ...
```
