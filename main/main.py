# import os
# import pandas as pd
# from helpers import files_to_upload_dir, csvs_to_upload_dir, dataset_id, table_id
# from process_excel import process_excel_files
# from upload_data_to_bigquery import get_bigquery_client, get_schema, load_csv_to_bigquery

# # TODO: add logging
# # TODO: this will be the base for uploading to big query

# def main():
#     process_excel_files(files_to_upload_dir)
#     # Initialize BigQuery client
#     client = get_bigquery_client()
    
#     # Get the schema
#     schema = get_schema()
    
#     load_csv_to_bigquery(client, schema, csvs_to_upload_dir, dataset_id, table_id)
    
#     print("All files have been uploaded successfully.")

# main()