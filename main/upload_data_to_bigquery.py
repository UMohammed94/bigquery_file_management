import os
from log import logger
from google.cloud import bigquery


def get_bigquery_client():
    """Initialize and return a BigQuery client."""
    return bigquery.Client()

def get_schema():
    """Return the schema for the BigQuery table."""
    return [
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('id', 'STRING'),
        bigquery.SchemaField('diameter_min_m', 'FLOAT64'),
        bigquery.SchemaField('diameter_max_m', 'FLOAT64'),
        bigquery.SchemaField('potentially_hazardous', 'BOOL'),
        bigquery.SchemaField('unique_id', 'STRING'),
    ]


def get_existing_ids(client, project_id, dataset_id, table_id):
    """Fetch existing unique IDs from the BigQuery table."""
    query = f"""
        SELECT DISTINCT unique_id
        FROM `{project_id}.{dataset_id}.{table_id}`
    """
    query_job = client.query(query)
    existing_ids = {row["unique_id"] for row in query_job}
    return existing_ids


def filter_csv_file(file_path, existing_ids):
    """
    Filter out rows with duplicate IDs in a CSV file.
    """
    import pandas as pd

    # Read CSV into DataFrame
    df = pd.read_csv(file_path)
    
    if "unique_id" not in df.columns:
        raise ValueError("The CSV file does not contain a 'unique_id' column.")

    # Filter out rows with existing IDs
    filtered_df = df[~df["unique_id"].isin(existing_ids)]
    duplicate_count = len(df) - len(filtered_df)

    return filtered_df, duplicate_count


def load_csv_to_bigquery(client, schema, csvs_to_upload_dir, project_id, dataset_id, table_id):
    """Load CSV files from a directory into a BigQuery table, avoiding duplicates."""
    existing_ids = get_existing_ids(client, project_id, dataset_id, table_id)
    logger.info(f"Fetched {len(existing_ids)} existing unique IDs from BigQuery.")

    for filename in os.listdir(csvs_to_upload_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(csvs_to_upload_dir, filename)
            
            # Filter duplicates
            try:
                filtered_df, duplicate_count = filter_csv_file(file_path, existing_ids)
                logger.info(f"Found {duplicate_count} duplicate records in {filename}.")
                
                if not filtered_df.empty:
                    # Define the BigQuery table reference
                    table_ref = f"{project_id}.{dataset_id}.{table_id}"
                    
                    # Configure the load job
                    job_config = bigquery.LoadJobConfig(
                        schema=schema,
                        skip_leading_rows=1,  # Skip header row
                        source_format=bigquery.SourceFormat.CSV,
                        autodetect=False,  # Do not auto-detect schema
                    )
                    
                    # Convert filtered DataFrame to a CSV buffer
                    buffer = filtered_df.to_csv(index=False).encode("utf-8")
                    
                    # Load data from buffer to BigQuery
                    load_job = client.load_table_from_file(buffer, table_ref, job_config=job_config)
                    load_job.result()  # Wait for the job to complete
                    
                    logger.info(f"Loaded {len(filtered_df)} rows from {filename} into {dataset_id}:{table_id}.")
                else:
                    logger.info(f"No new data to upload from {filename}.")
            except Exception as e:
                logger.error(f"Failed to process {filename}: {e}")