from config.loader import load_config
from datetime import datetime
from pathlib import Path
import os
import logging

log = logging.getLogger("root")
project_root = Path(__file__).resolve().parents[2]

# Load config
config = load_config()

def clean_folder(folder_path: str):
    """
    Deletes all .csv files in the specified folder.

    Parameters:
        folder_path (str): The path to the folder where .csv files need to be deleted.
    """
    folder = Path(folder_path)
    
    # Check if the folder exists
    if not folder.is_dir():
        raise ValueError(f"The specified path is not a directory: {folder_path}")
    
    # Iterate through all .csv files in the folder and delete them
    csv_files = folder.glob("*.csv")  # Matches all .csv files in the folder
    deleted_files = []
    for csv_file in csv_files:
        csv_file.unlink()  # Deletes the file
        deleted_files.append(csv_file.name)
    
    if deleted_files:
        log.info(f"Deleted the following CSV files: {', '.join(deleted_files)}")
    else:
        log.info("No CSV files found to delete.")

def rename_file(file: str) -> None:
  os.rename(project_root / "data" / file, project_root / "data" / "data.csv")

def extract_datetime_from_filename(filename: str) -> datetime:
    """
    Extracts a datetime object from the filename, assuming the format is %Y_%m_%d_%H_%M_%S.csv.
    
    Parameters:
        file_path (str): The full path to the file.

    Returns:
        datetime: The parsed datetime object from the filename.
    """
    stem = filename.split('.')[0]
    
    # Parse the datetime string assuming format %Y_%m_%d_%H_%M_%S
    try:
        file_datetime = datetime.strptime(stem, "%Y_%m_%d_%H_%M_%S")
        return file_datetime
    except ValueError as e:
        raise ValueError(f"Filename does not match the expected datetime format: {stem}") from e
  

  