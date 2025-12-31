"""
Kaggle dataset download script.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from kaggle.api.kaggle_api_extended import KaggleApi
from src.config import KAGGLE_DATASET_NAME, DATA_DIR, KAGGLE_FILE_NAME


def download_dataset():
    """Downloads and unzips the Amazon Fine Food Reviews dataset from Kaggle."""
    
    DATA_DIR.mkdir(exist_ok=True)

    file_path = DATA_DIR / KAGGLE_FILE_NAME
    if file_path.exists():
        print(f"Dataset already exists at {file_path}")
        return

    print(f"Downloading {KAGGLE_DATASET_NAME}...")
    try:
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(KAGGLE_DATASET_NAME, path=str(DATA_DIR), unzip=True)
        print("Download and extraction complete.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Ensure you have a valid kaggle.json in your root directory or ~/.kaggle/")


if __name__ == "__main__":
    download_dataset()
