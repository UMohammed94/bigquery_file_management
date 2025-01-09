import os
from pathlib import Path
from dotenv import load_dotenv
from log import logger

load_dotenv()

current_dir = Path.cwd()
parent_dir = current_dir.parent
files_to_upload_dir = current_dir / 'files_to_bigquery'
downloaded_csvs = current_dir / 'downloaded_files_'
log_output_dir = current_dir / 'log_output'
PROJECT_ID = os.getenv('project_id')
DATASET_ID = os.getenv('dataset_id')
TABLE_ID = os.getenv('table_id')
API_KEY = os.getenv("api_key")

NASA_REPORT_START_DATE = "2023-12-01"
NASA_REPORT_END_DATE = "2023-12-07"

required_dirs=[files_to_upload_dir, downloaded_csvs,log_output_dir]

def create_directories(dirs: list) -> None:
    logger.info(f"checking if required dirs exist")
    for dir_path in dirs:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")
    logger.info(f"all required dirs exist.")

create_directories(required_dirs)