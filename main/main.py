import os
import pandas as pd
from config import files_to_upload_dir, files_to_upload_dir, project_id, dataset_id, table_id
from process_files import process_csv_files
from upload_data_to_bigquery import get_bigquery_client, get_schema, load_csv_to_bigquery

# TODO: add logging
# TODO: this will be the base for uploading to big query
# TODO: add logging


def main():
    # process_excel_files(files_to_upload_dir)
    # Initialize BigQuery client
    client = get_bigquery_client()
    
    # Get the schema
    schema = get_schema()
    
    load_csv_to_bigquery(client, schema, files_to_upload_dir, project_id, dataset_id, table_id)
    
    print("All files have been uploaded successfully.")

main()