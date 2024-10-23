import os
import json
from google_play_scraper import app

# List of Google Play Store app IDs to scrape
app_ids = [
    'com.example.app1',
    'com.example.app2',
    'com.example.app3',
    # Add more app IDs
]

# Define the folder to save the scraped data
folder_path = './playstore_scraper/scraped_data'

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Function to scrape app data and save it to a JSON file
def scrape_app(app_id):
    try:
        # Scrape the app details using google_play_scraper
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

# Loop through the list of app IDs and scrape data
def scrape_all_apps(app_ids):
    for app_id in app_ids:
        scrape_app(app_id)

# Start scraping all apps
scrape_all_apps(app_ids)
