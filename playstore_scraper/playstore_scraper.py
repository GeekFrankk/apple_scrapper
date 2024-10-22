import os
import json
from google_play_scraper import app

# List of app IDs to scrape
app_ids = [
    '',
    '',
    '',
    '',
    '',
    '',
    '',
]

# Define the folder to save the data
folder_path = './playstore_scraper/scraped_data'

# Create folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Loop through the list of app IDs
for app_id in app_ids:
    try:
        # Scrape app details
        result = app(app_id, lang='en', country='us')
        
        # Generate a filename based on the app ID
        file_name = f"{app_id.replace('.', '_')}_data.json"
        file_path = os.path.join(folder_path, file_name)
        
        # Write the result to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)
        
        print(f"Data for {app_id} saved to {file_path}")

    except Exception as e:
        print(f"Failed to scrape {app_id}: {str(e)}")
