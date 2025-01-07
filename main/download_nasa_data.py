import requests
import os
import pandas as pd
# library to import env variables
from dotenv import load_dotenv
from config import downloaded_csvs
from datetime import datetime

# load env variables
load_dotenv()

# define your env variable
API_KEY = os.getenv("api_key")

# define your url
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

# Define parameters for the API call
params = {
    "start_date": "2023-12-01",  # Start date in YYYY-MM-DD format
    "end_date": "2023-12-07",    # End date in YYYY-MM-DD format
    "api_key": API_KEY
}

# Make the API request
response = requests.get(BASE_URL, params=params)

# Check the response status
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()
    print('this is the data:',data)

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
    
     # Convert to DataFrame
    df = pd.DataFrame(table_data, columns=headers)
    
    timestamp = datetime.now().strftime("%Y-%m-%d")

    # Save to CSV
    output_file = os.path.join(downloaded_csvs, f"asteroids_data_{timestamp}.csv")
    df.to_csv(output_file, index=False)
    
    print(f"Data successfully downloaded to: {output_file}")
else:
    print(f"Failed to retrieve data: {response.status_code}")