# from google.cloud import bigquery
# import os

# def get_bigquery_client():
#     """Initialize and return a BigQuery client."""
#     return bigquery.Client()

# def get_schema():
#     """Return the schema for the BigQuery table."""
#     return [
#         bigquery.SchemaField('vendor', 'STRING'),
#         bigquery.SchemaField('carrier', 'STRING'),
#         bigquery.SchemaField('account_number','STRING'),
#         bigquery.SchemaField('company','STRING'),
#         bigquery.SchemaField('invoice_number','STRING'),
#         bigquery.SchemaField('invoice_amount','FLOAT64'),
#         bigquery.SchemaField('invoice_date','DATE'),
#         bigquery.SchemaField('transportation_mode','STRING'),
#         bigquery.SchemaField('shipment_tracking_number','STRING'),
#         bigquery.SchemaField('original_cost','FLOAT64'),
#         bigquery.SchemaField('discount','FLOAT64'),
#         bigquery.SchemaField('net_shipment_cost','FLOAT64'),
#         bigquery.SchemaField('currency','STRING'),
#         bigquery.SchemaField('carrier_service_code','STRING'),
#         bigquery.SchemaField('carrier_service_level','STRING'),
#         bigquery.SchemaField('normalized_service_level','STRING'),
#         bigquery.SchemaField('zone','FLOAT64'),
#         bigquery.SchemaField('class','STRING'),
#         bigquery.SchemaField('miles','FLOAT64'),
#         bigquery.SchemaField('ship_date','DATE'),
#         bigquery.SchemaField('delivery_date','DATE'),
#         bigquery.SchemaField('delivery_time','STRING'),
#         bigquery.SchemaField('delivery_signature','STRING'),
#         bigquery.SchemaField('actual_weight_lbs','FLOAT64'),
#         bigquery.SchemaField('bhilled_weight_lbs','FLOAT64'),
#         bigquery.SchemaField('shipper_name','STRING'),
#         bigquery.SchemaField('shipper_company','STRING'),
#         bigquery.SchemaField('shipper_address','STRING'),
#         bigquery.SchemaField('shipper_city','STRING'),
#         bigquery.SchemaField('shipper_state','STRING'),
#         bigquery.SchemaField('shipper_postal_code','STRING'),
#         bigquery.SchemaField('shipper_country','STRING'),
#         bigquery.SchemaField('receiver_name','STRING'),
#         bigquery.SchemaField('receiver_company','STRING'),
#         bigquery.SchemaField('receiver_address','STRING'),
#         bigquery.SchemaField('receiver_city','STRING'),
#         bigquery.SchemaField('receiver_state','STRING'),
#         bigquery.SchemaField('receiver_postal_code','STRING'),
#         bigquery.SchemaField('receiver_country','STRING'),
#         bigquery.SchemaField('bill_option','STRING'),
#         bigquery.SchemaField('decladed_value','FLOAT64'),
#         bigquery.SchemaField('piece_count','INT64'),
#         bigquery.SchemaField('reference_1','STRING'),
#         bigquery.SchemaField('reference_2','STRING'),  
#         bigquery.SchemaField('reference_3','STRING'),
#         bigquery.SchemaField('reference_4','STRING'),
#         bigquery.SchemaField('reference_5','STRING'),
#         bigquery.SchemaField('reference_6','STRING'),
#         bigquery.SchemaField('reference_7','STRING'),
#         bigquery.SchemaField('reference_8','STRING'),
#         bigquery.SchemaField('gl_code_1','STRING'),
#         bigquery.SchemaField('gl_code_2','STRING'),
#         bigquery.SchemaField('gl_code_3','STRING')   
# ]
# def load_csv_to_bigquery(client, schema, csvs_to_upload_dir, dataset_id, table_id):
#     """Load CSV files from a directory into a BigQuery table."""
#     for filename in os.listdir(csvs_to_upload_dir):
#         if filename.endswith('.csv'):
#             file_path = os.path.join(csvs_to_upload_dir, filename)
            
#             # Define the BigQuery table reference
#             table_ref = client.dataset(dataset_id).table(table_id)
            
#             # Configure the load job
#             job_config = bigquery.LoadJobConfig(
#                 schema=schema,
#                 skip_leading_rows=1,  # Skip header row
#                 source_format=bigquery.SourceFormat.CSV,
#                 autodetect=False,  # Do not auto-detect schema
#             )
            
#             # Load data from CSV file to BigQuery
#             with open(file_path, "rb") as source_file:
#                 load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
            
#             # Wait for the job to complete
#             load_job.result()
            
#             print(f"Loaded {filename} into {dataset_id}:{table_id}")
