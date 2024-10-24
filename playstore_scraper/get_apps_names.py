import os
import json
import csv
from google_play_scraper import search

# Define the absolute paths for playstore_scraper folder, JSON and CSV files
scraper_folder = os.path.dirname(os.path.realpath(__file__))  # This gets the directory of the current script
json_file_path = os.path.join(scraper_folder, 'apps_names.json')
csv_file_path = os.path.join(scraper_folder, 'apps_names.csv')

# Ensure the folder exists
if not os.path.exists(scraper_folder):
    os.makedirs(scraper_folder)

# Base URL for Play Store apps
play_store_base_url = "https://play.google.com/store/apps/details?id="

# Function to search for apps in the 'Medical' category
def search_medical_apps(query='medical'):
    results = search(
        query=query,  # Searching for apps with a custom query
        lang='en',    # Language
        country='us'  # Country
    )
    
    # Extract app names and construct their Play Store URLs using the app ID (package name)
    apps = [{"App Name": app['title'], "App URL": f"{play_store_base_url}{app['appId']}"} for app in results]
    
    return apps

# Function to remove duplicate apps by name
def remove_duplicates(app_list):
    seen = set()
    distinct_apps = []
    for app in app_list:
        if app['App Name'] not in seen:
            distinct_apps.append(app)
            seen.add(app['App Name'])
    return distinct_apps

# Load existing apps from JSON if the file exists
existing_apps = []
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        existing_apps = json.load(json_file)

# Retrieve apps over multiple runs
all_apps = existing_apps.copy()  # Start with existing apps
queries = ['medical', 'medicine', 'doctor', 'hospital']  # Multiple related queries

for query in queries:
    print(f"Searching for apps with query: {query}")
    new_apps = search_medical_apps(query=query)
    all_apps.extend(new_apps)

# Remove duplicate apps by name (including old and new apps)
distinct_apps = remove_duplicates(all_apps)

# Save the combined data (old + new distinct apps) back to the JSON file
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(distinct_apps, json_file, indent=4)

print(f"Distinct medical app names and URLs saved to: {json_file_path}")

# Function to update the CSV file with the app names
def read_json_and_update_csv(json_file, csv_file):
    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        return

    # Read the apps from the JSON file
    with open(json_file, 'r', encoding='utf-8') as json_file:
        apps_data = json.load(json_file)

    # Extract only the app names
    app_names = [app['App Name'] for app in apps_data]

    # Write the app names to the CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['No', 'App Name'])  # Write the header

        # Write app names to the CSV with a numbered list
        for i, app_name in enumerate(app_names, start=1):
            writer.writerow([i, app_name])

    print(f"CSV file updated: {csv_file}")

# Run the function to update the CSV from JSON
read_json_and_update_csv(json_file_path, csv_file_path)
