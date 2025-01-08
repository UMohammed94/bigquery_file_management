import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

current_dir = Path.cwd()
parent_dir = current_dir.parent
files_to_upload_dir = current_dir / 'files_to_bigquery'
downloaded_csvs = current_dir / 'downloaded_files_'
PROJECT_ID = os.getenv('project_id')
DATASET_ID = os.getenv('dataset_id')
TABLE_ID = os.getenv('table_id')
