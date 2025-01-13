import pandas as pd
import os
from log import logger

# TODO: AT THE END of the code, add a delete functionlity to upload the old files to archive and delete all files in the folder.
def process_csv_files(downloaded_raw_dir, upload_dir):
    for filename in os.listdir(downloaded_raw_dir):
        filepath = os.path.join(downloaded_raw_dir, filename)
        if os.path.isfile(filepath) and filename.endswith('.csv'):
            try:
                # Load the CSV file
                df = pd.read_csv(filepath)

                # Clean the headers
                df = clean_headers(df)

                # Ensure date column is in valid format
                df = validate_date_format(df, 'date')

                # Add a unique ID column
                df = add_unique_id(df, ['id', 'name', 'date'])

                # Save cleaned DataFrame to a new CSV file
                csv_filename = os.path.splitext(filename)[0] + '_processed.csv'
                csv_filepath = os.path.join(upload_dir, csv_filename)
                df.to_csv(csv_filepath, index=False)
                logger.info(f'Saved {csv_filename} to {upload_dir}')

            except Exception as e:
                logger.info(f'Failed to process {filename}: {e}')

def clean_headers(df):
    df.columns = (
        df.columns
        .str.replace(r'[^\w\s]', '', regex=True)  # Remove special characters
        .str.replace(' ', '_')  # Replace spaces with underscores
        .str.lower()  # Convert to lowercase
    )
    return df

def validate_date_format(df, date_column):
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def add_unique_id(df, columns):
    if all(col in df.columns for col in columns):
        df['unique_id'] = df[columns].astype(str).agg('_'.join, axis=1)
    return df

