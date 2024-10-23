import os
import json
from google_play_scraper import app

# Define the path to the apps_names.json file (which contains app URLs)
scraper_folder = os.path.dirname(os.path.realpath(__file__))  # This gets the directory of the current script
json_file_path = os.path.join(scraper_folder, 'apps_names.json')

# Define the folder to save the scraped data
scraped_data_path = os.path.join(scraper_folder, 'scraped_data')

# Create the folder if it doesn't exist
if not os.path.exists(scraped_data_path):
    os.makedirs(scraped_data_path)

# Function to extract app IDs from the apps_names.json file
def get_app_ids_from_json(json_file_path):
    app_ids = []
    
    # Load the JSON data from apps_names.json
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        apps_data = json.load(json_file)
        
        # Extract the appId from the URL (the part after 'id=')
        for app in apps_data:
            app_url = app['App URL']
            app_id = app_url.split('id=')[-1]  # Get the appId from the URL
            app_ids.append(app_id)
    
    return app_ids

# Function to load already scraped app IDs from the scraped_data folder
def get_already_scraped_app_ids(scraped_data_path):
    scraped_files = os.listdir(scraped_data_path)
    scraped_app_ids = [file.replace('_data.json', '').replace('_', '.') for file in scraped_files if file.endswith('_data.json')]
    return set(scraped_app_ids)

# Function to scrape app data and save it to a JSON file
def scrape_app(app_id):
    try:
        # Scrape the app details using google_play_scraper
        result = app(app_id, lang='en', country='us')

        # Generate a filename based on the app ID
        file_name = f"{app_id.replace('.', '_')}_data.json"
        file_path = os.path.join(scraped_data_path, file_name)

        # Write the result to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        print(f"Data for {app_id} saved to {file_path}")

    except Exception as e:
        print(f"Failed to scrape {app_id}: {str(e)}")

# Function to scrape all apps using app IDs
def scrape_all_apps(app_ids):
    scraped_app_ids = get_already_scraped_app_ids(scraped_data_path)
    print(f"Already scraped app IDs: {len(scraped_app_ids)}")

    for app_id in app_ids:
        if app_id not in scraped_app_ids:
            scrape_app(app_id)

# Start the scraping process
app_ids = get_app_ids_from_json(json_file_path)

# Scrape all the apps using the extracted app IDs, skipping the already scraped ones
scrape_all_apps(app_ids)

# Function to count the number of scraped apps
def count_scraped_apps(scraped_data_path):
    # List all files in the scraped_data folder
    scraped_files = os.listdir(scraped_data_path)
    
    # Filter files to count only those ending with '_data.json' (the files storing app data)
    json_files = [file for file in scraped_files if file.endswith('_data.json')]
    
    # Return the count of JSON files
    return len(json_files)

# Example usage: Count how many apps have been scraped
scraped_apps_count = count_scraped_apps(scraped_data_path)
print(f"Total apps scraped: {scraped_apps_count}")




# from google_play_scraper import reviews, Sort

# # Function to scrape reviews for a given app ID
# def scrape_reviews(app_id, num_reviews=10):
#     try:
#         # Fetch reviews (sorted by newest first, you can also sort by helpfulness or rating)
#         result, continuation_token = reviews(
#             app_id,
#             lang='en',      # Language
#             country='us',   # Country
#             sort=Sort.NEWEST,  # Sort by newest
#             count=num_reviews  # Number of reviews to fetch
#         )

#         return result  # Return the list of reviews

#     except Exception as e:
#         print(f"Failed to scrape reviews for {app_id}: {str(e)}")
#         return []

# # Example usage: Scrape 10 reviews for the app 'com.clue.android'
# app_id = "com.clue.android"
# app_reviews = scrape_reviews(app_id, num_reviews=10)

# # Print fetched reviews
# for review in app_reviews:
#     print(f"User: {review['userName']}, Rating: {review['score']}, Review: {review['content']}")
