# Authors
# Developers: Mohammed Uddin, Muin Syed, Sabrin Tahmid, Soud Talukder
# Product Manager: Mohammed Monodol 

# TODO this will be the base for uploading to big query
# 1. download_data_from_biguquery()
# 2. delete_Data_from_bigquery()
# 3. Update_date_from_bigquery()
# 4. copy_data_From_bigquery() 
# 5. logging matrix
# 6. create a free google drive as backup for data aka s3 bucket
# 7. create a readme doc on how to authenticate with GCP
# 8. create a small chart maybe using anaconda? or sql? or looker?
# 9. schedule it using a free service like github actions?

import os
import pandas as pd
from config import files_to_upload_dir, files_to_upload_dir, downloaded_csvs, PROJECT_ID, DATASET_ID, TABLE_ID, NASA_REPORT_START_DATE, NASA_REPORT_END_DATE, API_KEY
from process_files import process_csv_files
from upload_data_to_bigquery import get_bigquery_client, get_schema, load_csv_to_bigquery
from download_nasa_data import fetch_asteroid_data, process_asteroid_data, save_data_to_csv


def main():
    # step 1: Download data
    print('fetching raw nasa data...')
    data = fetch_asteroid_data(NASA_REPORT_START_DATE, NASA_REPORT_END_DATE, API_KEY)
    if data:
        # Process the data into a DataFrame
        df = process_asteroid_data(data)
        
        # Save the data to a CSV file
        save_data_to_csv(df, downloaded_csvs)

    # step 2: process csv files for bigquery
    print('formatting csvs for bigquery...')
    process_csv_files(files_to_upload_dir)
    
    # step 3 : Initialize BigQuery client
    print('initalizing the bigquery client...')
    client = get_bigquery_client()
    
    # step 4: Get the schema
    print('initializing the schema for bigquery...')
    schema = get_schema()
    
    # step 5: Upload to bigquery
    print('uploading your files...')
    load_csv_to_bigquery(client, schema, files_to_upload_dir, PROJECT_ID, DATASET_ID, TABLE_ID)
    
    print("All files have been uploaded successfully!")

main()