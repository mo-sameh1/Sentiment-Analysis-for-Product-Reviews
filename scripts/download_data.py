import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Configuration
DATASET_NAME = "snap/amazon-fine-food-reviews"
DATA_DIR = "data"
FILE_NAME = "Reviews.csv"

def download_dataset():
    """Downloads and unzips the Amazon Fine Food Reviews dataset from Kaggle."""
    
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Check if file already exists
    file_path = os.path.join(DATA_DIR, FILE_NAME)
    if os.path.exists(file_path):
        print(f"Dataset already exists at {file_path}")
        return

    print(f"Downloading {DATASET_NAME}...")
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(DATASET_NAME, path=DATA_DIR, unzip=True)
        print("Download and extraction complete.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Ensure you have a valid kaggle.json in your root directory or ~/.kaggle/")

if __name__ == "__main__":
    download_dataset()
