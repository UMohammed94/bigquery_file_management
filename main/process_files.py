import pandas as pd
import os
from helpers import csvs_to_upload_dir

def clean_headers(df):
# Your existing header mapping function
    header_mapping = {
        'Vendor': 'vendor',
        'Carrier': 'carrier',
        'Account #': 'account_number',
        'Company(s)': 'company',
        'Invoice #': 'invoice_number',
        'Invoice Amount': 'invoice_amount',
        'Invoice Date': 'invoice_date',
        'Transportation Mode': 'transportation_mode',
        'Shipment Tracking #': 'shipment_tracking_number',
        'Original Cost': 'original_cost',
        'Discount':'discount',
        'Net Shipment Cost':'net_shipment_cost',
        'Currency':'currency',
        'Carrier Service Code':'carrier_service_code',
        'Carrier Service Level':'carrier_service_level',
        'Normalized Service Level':'normalized_service_level',
        'Zone':'zone',
        'Class':'class',
        'Miles':'miles',
        'Ship Date':'ship_date',
        'Delivery Date':'delivery_date',
        'Delivery Time':'delivery_time',
        'Delivery Signature':'delivery_signature',
        'Actual Weight (lbs.)':'actual_weight_lbs',
        'Billed Weight (lbs.)':'bhilled_weight_lbs',
        'Shipper Name':'shipper_name',
        'Shipper Company':'shipper_company',
        'Shipper Address':'shipper_address',
        'Shipper City':'shipper_city',
        'Shipper State':'shipper_state',
        'Shipper Postal Code':'shipper_postal_code',
        'Shipper Country':'shipper_country',
        'Receiver Name':'receiver_name',
        'Receiver Company':'receiver_company',
        'Receiver Address':'receiver_address',
        'Receiver City':'receiver_city',
        'Receiver State':'receiver_state',
        'Receiver Postal Code':'receiver_postal_code',
        'Receiver Country':'receiver_country',
        'Bill Option':'bill_option',
        'Declared Value':'decladed_value',
        'Piece Count':'piece_count',
        'Reference 1':'reference_1',
        'Reference 2':'reference_2',
        'Reference 3':'reference_3',
        'Reference 4':'reference_4',
        'Reference 5':'reference_5',
        'Reference 6':'reference_6',
        'Reference 7':'reference_7',
        'Reference 8':'reference_8',
        'Gl Code 1':'gl_code_1',
        'Gl Code 2':'gl_code_2',
        'Gl Code 3':'gl_code_3'    
    }
    df.rename(columns=header_mapping, inplace=True)
    return df

def preprocess_column(df, column_name, dtype, fill_value=None):
    if column_name in df.columns:
        if dtype == 'string':
            df[column_name] = df[column_name].astype(str).fillna('')  # Ensure string type
        elif dtype == 'float':
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0.0)  # Ensure float type with 0.0 as default
        elif dtype == 'custom':
            df[column_name] = df[column_name].apply(lambda x: fill_value + str(x) if pd.notnull(x) else '')  # Custom string processing
    return df

def process_excel_files(upload_dir):
    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)
        if os.path.isfile(filepath) and filename.endswith('.xlsx'):
            try:
                # Load the Excel file
                xls = pd.ExcelFile(filepath, engine='openpyxl')

                # Parse sheets except 'Report Criteria'
                sheet_names = xls.sheet_names
                dfs = {sheet: xls.parse(sheet) for sheet in sheet_names if sheet != 'Report Criteria'}

                # Process and save each DataFrame to a CSV file
                for sheet_name, df in dfs.items():
                    # Clean the headers
                    df = clean_headers(df)

                    # Preprocess specific columns with correct data types
                    df = preprocess_column(df, 'Reference_5', 'string')
                    df = preprocess_column(df, 'Shipper_Postal_Code', 'string')  # Ensure Shipper_Postal_Code is string
                    df = preprocess_column(df, 'Carrier_Service_Code', 'custom', 'CS_')
                    df = preprocess_column(df, 'Declared_Value', 'float')

                    # Save cleaned DataFrame to a CSV file
                    csv_filename = os.path.splitext(filename)[0] + f'_{sheet_name}.csv'
                    csv_filepath = os.path.join(csvs_to_upload_dir, csv_filename)
                    df.to_csv(csv_filepath, index=False)
                    print(f'Saved {csv_filename} to {csvs_to_upload_dir}')

            except Exception as e:
                print(f'Failed to process {filename}: {e}')