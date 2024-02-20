import os
from tqdm import tqdm

def find_excel_files(directory, excel_names):
    """
    Find full paths of specific Excel files in a directory.

    Parameters:
    - directory (str): The directory to search for Excel files.
    - excel_names (list): List of Excel file names to search for.

    Returns:
    - excel_paths (list): List of full paths to the found Excel files.
    """
    excel_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower() in [excel_name.lower() for excel_name in excel_names] and file.lower().endswith((".xls", ".xlsx")):
                excel_paths.append(os.path.join(root, file))
    return excel_paths

def anonymize_excel(excel_path):
    """
    Anonymize an excel file

    Parameters:
    - excel_path (str): The path to the excel file.
    """
    # Get DICOM filenames contained inside the series

    # Anonymize the excel file
    # Delete the old file
    # Save the anonymized file
    
    # Insert your code here

    pass

if __name__ == "__main__":

    # Provide a list of the cancer types to check
    cancer_types = ["breast", "colorectal", "lung", "prostate"]

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

            # List of specific Excel file names to check
            excel_names_to_check = [f"{cancer_type}_cancer.xls", f"{cancer_type}_cancer_training.xls", f"{cancer_type}_cancer_observational.xls", f"{cancer_type}_cancer_feasibility.xls"]
            
            # Find full paths of specific Excel files in the directory
            excel_paths = find_excel_files(working_path, excel_names_to_check)

            for excel_path in excel_paths:
                anonymize_excel(excel_path)
