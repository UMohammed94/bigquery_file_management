import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from helpers import BASE_URL

# load env variables
load_dotenv()

def fetch_asteroid_data(start_date, end_date, api_key):
    # Define parameters for the API call
    params = {
        "start_date": start_date,  # Start date in YYYY-MM-DD format
        "end_date": end_date,    # End date in YYYY-MM-DD format
        "api_key": api_key
    }

    # Make the API request
    response = requests.get(BASE_URL, params=params)

    # Check the response status
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    return data

def process_asteroid_data(data):
    # Prepare table data
    table_data = []
    headers = ["Date", "Name", "ID", "Diameter (Min M)", "Diameter (Max M)", "Potentially Hazardous"]

    for date, neo_list in data["near_earth_objects"].items():
        for neo in neo_list:
            # Extract relevant details
            name = neo["name"]
            neo_id = neo["id"]
            diameter_min = neo["estimated_diameter"]["meters"]["estimated_diameter_min"]
            diameter_max = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
            hazardous = neo["is_potentially_hazardous_asteroid"]
            
            # Append row to table data
            table_data.append([date, name, neo_id, diameter_min, diameter_max, hazardous])
    
    return pd.DataFrame(table_data, columns=headers)

def save_data_to_csv(df, output_dir): 
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, f"asteroids_data_{timestamp}.csv")
    df.to_csv(output_file, index=False)
    print(f"Data successfully downloaded to: {output_file}")