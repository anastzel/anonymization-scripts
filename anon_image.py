import os
from tqdm import tqdm

def get_dicom_files(directory):
    """
    Get a list of DICOM files in the specified directory.

    Parameters:
    - directory (str): The directory to search for DICOM files.

    Returns:
    - dicom_files (list): List of paths to DICOM files.
    """
    dicom_files = [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files if file.lower().endswith(".dcm")]
    return dicom_files

def anonymize_series(series_path):
    """
    Anonymize a DICOM series by getting attributes and writing existing issues.

    Parameters:
    - series_path (str): The path to the DICOM series.
    """
    # Get DICOM filenames contained inside the series
    dicom_files = get_dicom_files(series_path)

    # Anonymize each DICOM file in the series
    for dicom_path in dicom_files:
        # Anonymize the DICOM file
        # Delete the old file
        # Save the anonymized file
        
        # Insert your code here

        pass

if __name__ == "__main__":

    # Provide a list of the cancer types to check
    cancer_types = ["breast", "colorectal", "lung", "prostate"]
    # cancer_types = ["lung"]

    # Select the data provider
    dps = {
        "breast": ["auth", "disba", "goc", "hcs", "unitov", "uns"],
        "colorectal": ["auth", "disba", "goc", "unitov", "uns"],
        "lung": ["auth", "disba", "goc", "unitov", "uoa", "visaris"],
        "prostate": ["goc", "idibaps", "uoa"]
    }

    database_path = "/mnt/nfs/incisive2"

    for cancer_type in cancer_types:
        for data_provider in dps[cancer_type]:
            # Define the target directory to examine based on cancer type and data provider name
            working_path = os.path.join(database_path, cancer_type, data_provider, "data")

            # Get all patients paths
            patients_paths = [os.path.join(working_path, filename) for filename in os.listdir(working_path) if os.path.isdir(os.path.join(working_path, filename))]

            # Get all studies and check for NIFTI files outside of series
            studies_paths = [os.path.join(patient_path, study) for patient_path in patients_paths for study in os.listdir(patient_path) if os.path.isdir(os.path.join(patient_path, study))]

            # Get all series paths
            series_paths = [os.path.join(study_path, serie) for study_path in studies_paths for serie in os.listdir(study_path) if os.path.isdir(os.path.join(study_path, serie))]
                    
            # Anonymize each series
            for series_path in tqdm(series_paths, total=len(series_paths)):
                anonymize_series(series_path)