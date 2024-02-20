import os
import pydicom as dicom
from tqdm import tqdm

# Define a dictionary to store histograms for each image modality
images_per_modality = {}

# Provide a list of the cancer types to check
cancer_types = ["breast", "colorectal", "lung", "prostate"]
# cancer_types = ["lung"]

# Select the data provider
dps = {"breast" : ["auth", "disba", "goc", "hcs", "unitov", "uns"],
    "colorectal" : ["auth", "disba", "goc", "unitov", "uns"],
    "lung" : ["auth", "disba", "goc", "unitov", "uoa", "visaris"],
    "prostate" : ["goc", "idibaps", "uoa"]
}

def find_modality(serie_path):

    dicom_filenames = [os.path.join(serie_path, filename) for filename in os.listdir(serie_path) if filename.endswith(".dcm")]
    if len(dicom_filenames):
        dicom_name = dicom_filenames[0]
        try:
            image = dicom.dcmread(dicom_name, specific_tags=[(0x0008, 0x0060)])
            modality = image.Modality
        except Exception as e:
            return None
    else:
        return None

    return modality

# Function to update the resolutions
def update_images_per_modality(modality):
    if modality:
        if modality not in images_per_modality:
            images_per_modality[modality] = 1
        else:
            images_per_modality[modality] += 1

for cancer_type in cancer_types:
    data_providers = dps[cancer_type]
    for data_provider in data_providers:

        # Define the target directory to examine based on cancer type and data provider name
        database_path = "/mnt/nfs/incisive2"
        working_path = f"{database_path}/{cancer_type}/{data_provider}/data"

        print(f"\nCalculating average resolution for {data_provider}-{cancer_type}.\n")

        # Get all patients paths
        patients_paths = [os.path.join(working_path, filename) for filename in os.listdir(working_path) if os.path.isdir(os.path.join(working_path, filename))]

        # Get all studies and check for NIFTI files outside of Series
        studies_paths = []
        for patient_path in patients_paths:
            studies = os.listdir(patient_path)
            for study in studies:
                study_path = os.path.join(patient_path, study)
                if os.path.isdir(study_path):
                    studies_paths.append(study_path)

        # Get all series paths
        series_paths = []
        for study_path in studies_paths:
            series = os.listdir(study_path)
            for serie in series:
                serie_path = os.path.join(study_path, serie)
                if os.path.isdir(serie_path):
                    series_paths.append(serie_path)

        for serie_path in tqdm(series_paths, total=len(series_paths)):
            if len(os.listdir(serie_path)) > 0:
                for _ in range(len(os.listdir(serie_path))):
                    modality = find_modality(serie_path)
                    update_images_per_modality(modality)

sorted_images_per_modality = dict(sorted(images_per_modality.items(), key=lambda item: item[1], reverse=True))

# Remove the existing report file if it exists
file_path = "/mnt/nfs/incisive2/CERTH-curation/anonymization_scripts/images_per_modality.txt"
if os.path.exists(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path} has been deleted successfully.")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")

# Print the average resolutions
with open(file_path, "a") as f:
    for modality, occ in sorted_images_per_modality.items():
        f.write(f"For Modality: {modality} - Number of Images: {occ}\n")

