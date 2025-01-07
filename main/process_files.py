import pandas as pd
import os
from config import downloaded_csvs, files_to_upload_dir

def process_excel_files(downloaded_raw_dir, upload_dir):
    for filename in os.listdir(downloaded_raw_dir):
        filepath = os.path.join(downloaded_raw_dir, filename)
        if os.path.isfile(filepath) and filename.endswith('.csv'):
            try:
                # Load the CSV file
                df = pd.read_csv(filepath)

                # Clean the headers
                df = clean_headers(df)

                # Save cleaned DataFrame to a new CSV file
                csv_filename = os.path.splitext(filename)[0] + '_processed.csv'
                csv_filepath = os.path.join(upload_dir, csv_filename)
                df.to_csv(csv_filepath, index=False)
                print(f'Saved {csv_filename} to {upload_dir}')

            except Exception as e:
                print(f'Failed to process {filename}: {e}')

def clean_headers(df):
    df.columns = (
        df.columns
        .str.replace(r'[^\w\s]', '', regex=True)  # Remove special characters
        .str.replace(' ', '_')  # Replace spaces with underscores
        .str.lower()  # Convert to lowercase
    )
    return df