from google.cloud import bigquery

def copy_table(source_table_id, destination_table_id):
    """
    Copy a table in BigQuery from source_table_id to destination_table_id.
    
    Args:
        source_table_id (str): The full ID of the source table in the format `project.dataset.table`.
        destination_table_id (str): The full ID of the destination table in the format `project.dataset.table`.
    """
    client = bigquery.Client()

    # Construct the table copy job
    job = client.copy_table(
        source_table_id,  # Source table
        destination_table_id,  # Destination table
        # Optionally, set a write disposition (e.g., WRITE_TRUNCATE to overwrite)
        job_config=bigquery.CopyJobConfig(write_disposition="WRITE_TRUNCATE")
    )

    # Wait for the job to complete
    job.result()

    print(f"Copied {source_table_id} to {destination_table_id}")

# Example usage
source_table = "my-project-id.source_dataset.source_table"
destination_table = "my-project-id.target_dataset.target_table"
copy_table(source_table, destination_table)
