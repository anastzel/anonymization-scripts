import os
import pydicom as dicom
from tqdm import tqdm
from get_series_attributes import *
from messages import *
from issues_cases import *

def count_dicom_files(folder_path):
    dicom_count = 0

    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith(".dcm"):
                dicom_count += 1

    return dicom_count

# Provide a list of the cancer types to check
cancer_types = ["breast", "colorectal", "lung", "prostate"]

# Select the data provider
dps = {"breast" : ["auth", "disba", "goc", "hcs", "unitov", "uns"],
                  "colorectal" : ["auth", "disba", "goc", "unitov", "uns"],
                  "lung" : ["auth", "disba", "goc", "unitov", "uoa", "visaris"],
                  "prostate" : ["goc", "idibaps", "uoa"]
}

for cancer_type in cancer_types:
    dicom_per_cancer_type = 0
    data_providers = dps[cancer_type]
    for data_provider in data_providers:

        # Define the target directory to examine based on cancer type and data provider name
        database_path = "/mnt/nfs/incisive2"
        working_path = f"{database_path}/{cancer_type}/{data_provider}/data"

        print(f"\nCalculating statistcs for {data_provider}-{cancer_type}.\n")

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

        total_dicom = 0
        for serie_path in tqdm(series_paths, total=len(series_paths)):
            serie_dicom_count = count_dicom_files(serie_path)
            total_dicom += serie_dicom_count

        # print(f"Number of series: {len(series_paths)}")
        # print(series_paths)

        dicom_per_cancer_type += total_dicom
        print(f"Total DICOM count: {total_dicom} for {data_provider}-{cancer_type}")
    
    print(f"\nTotal DICOM count: {dicom_per_cancer_type} for {cancer_type} cancer.")