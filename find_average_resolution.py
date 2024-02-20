import os
import pydicom as dicom
from tqdm import tqdm
from get_series_attributes import *
from messages import *
from issues_cases import *

# Define a dictionary to store histograms for each image modality
resolutions = {}

# Provide a list of the cancer types to check
cancer_types = ["breast", "colorectal", "lung", "prostate"]

# Select the data provider
dps = {"breast" : ["auth", "disba", "goc", "hcs", "unitov", "uns"],
                  "colorectal" : ["auth", "disba", "goc", "unitov", "uns"],
                  "lung" : ["auth", "disba", "goc", "unitov", "uoa", "visaris"],
                  "prostate" : ["goc", "idibaps", "uoa"]
}

def find_modality_resolution(serie_path):

    dicom_filenames = [os.path.join(serie_path, filename) for filename in os.listdir(serie_path) if filename.endswith(".dcm")]
    if len(dicom_filenames):
        dicom_name = dicom_filenames[0]
        try:
            image = dicom.dcmread(dicom_name, specific_tags=[(0x0008, 0x0060), (0x0028, 0x0010), (0x0028, 0x0011)])
            modality = image.Modality
            resolution = (image.Rows, image.Columns)
        except Exception as e:
            return None, None
    else:
        return None, None

    return modality, resolution

# Function to update the resolutions
def update_resolutions(resolution, image_modality):
    if resolution and image_modality:
        if image_modality not in resolutions:
            resolutions[image_modality] = []
        resolutions[image_modality].append(resolution)

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
                modality, resolution = find_modality_resolution(serie_path)
                update_resolutions(resolution, modality)

# Calculate the average resolution for each image modality
average_resolutions = {}
for image_modality, resolutions_list in resolutions.items():
    total_rows = 0
    total_columns = 0
    for resolution in resolutions_list:
        total_rows += resolution[0]
        total_columns += resolution[1]
    average_rows = total_rows / len(resolutions_list)
    average_columns = total_columns / len(resolutions_list)
    average_resolutions[image_modality] = (average_rows, average_columns)

# Print the average resolutions
for image_modality, average_resolution in average_resolutions.items():
    print(f"Image Modality: {image_modality}, Average Resolution: {average_resolution}")
