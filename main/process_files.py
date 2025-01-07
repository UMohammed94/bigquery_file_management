import pandas as pd
import os
from config import downloaded_csvs, files_to_upload_dir

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

                # # Check for existing IDs before upload
                # df = check_existing_ids(df, upload_dir, 'unique_id')

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

def validate_date_format(df, date_column):
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def add_unique_id(df, columns):
    if all(col in df.columns for col in columns):
        df['unique_id'] = df[columns].astype(str).agg('_'.join, axis=1)
    return df


# TODO: refactor to check if it exists in db
# def check_existing_ids(df, upload_dir, id_column):
#     existing_ids = set()
#     for filename in os.listdir(upload_dir):
#         if filename.endswith('.csv'):
#             existing_df = pd.read_csv(os.path.join(upload_dir, filename))
#             if id_column in existing_df.columns:
#                 existing_ids.update(existing_df[id_column].dropna().unique())
    
#     # Filter out rows with existing IDs
#     if id_column in df.columns:
#         df = df[~df[id_column].isin(existing_ids)]
#     return df


# # Main function to process the CSV files
# def main():
#     process_csv_files(downloaded_csvs, files_to_upload_dir)

# if __name__ == "__main__":
#     main()
