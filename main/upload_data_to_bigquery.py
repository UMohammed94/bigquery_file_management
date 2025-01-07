from google.cloud import bigquery
import os

def get_bigquery_client():
    """Initialize and return a BigQuery client."""
    return bigquery.Client()

# TODO: can we do this dynamically?
def get_schema():
    """Return the schema for the BigQuery table."""
    return [
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('id','STRING'),
        bigquery.SchemaField('diameter_min_m','FLOAT64'),
        bigquery.SchemaField('diameter_max_m','FLOAT64'),
        bigquery.SchemaField('potentially_hazardous','BOOL')
]

def load_csv_to_bigquery(client, schema, csvs_to_upload_dir, dataset_id, table_id):
    """Load CSV files from a directory into a BigQuery table."""
    for filename in os.listdir(csvs_to_upload_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(csvs_to_upload_dir, filename)
            
            # Define the BigQuery table reference
            table_ref = client.dataset(dataset_id).table(table_id)
            
            # Configure the load job
            job_config = bigquery.LoadJobConfig(
                schema=schema,
                skip_leading_rows=1,  # Skip header row
                source_format=bigquery.SourceFormat.CSV,
                autodetect=False,  # Do not auto-detect schema
            )
            
            # Load data from CSV file to BigQuery
            with open(file_path, "rb") as source_file:
                load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
            
            # Wait for the job to complete
            load_job.result()
            
            print(f"Loaded {filename} into {dataset_id}:{table_id}")
