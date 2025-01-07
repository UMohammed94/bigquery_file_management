import os
from pathlib import Path

current_dir = Path.cwd()
parent_dir = current_dir.parent
files_to_upload_dir = current_dir / 'files_to_bigquery'
downloaded_csvs = current_dir / 'downloaded_files_'
project_id = 'data-projects-mu'
dataset_id = 'nasa_general_raw'
table_id = 'asteriod_information_raw'
