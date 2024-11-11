import json

# Define the cleaning function to extract the required fields
def clean_app_data(app_data):
    cleaned_data = {
    "details": {
        "title": app_data.get("title", "Unknown"),
        "seller": app_data.get("seller", "Unknown"),
        "price": app_data.get("price", "Unknown"),
        "rating": app_data.get("rating", "N/A"),
        "stars": app_data.get("stars", "No stars rating"),
        "appDescription": app_data.get("appDescription", "No description available"),
        "category": app_data.get("category", "Unknown"),   
        "ageRating": app_data.get("ageRating", "Unknown"),   
    } 
    }
    return cleaned_data

# Path for the master JSON file
master_json_path = './app_store_scraper/master_file.json'

try:
    # Read the master JSON file
    with open(master_json_path, 'r', encoding='utf-8') as master_file:
        data = json.load(master_file)
    
    # Clean and extract only the necessary fields for each app
    cleaned_data_list = [clean_app_data(app) for app in data]
    
    output_path = './app_store_scraper/descriptions/descriptions.json'
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(cleaned_data_list, output_file, indent=4)
    
    print(f"Cleaned data has been saved to '{output_path}'.")

except FileNotFoundError:
    print(f"The file '{master_json_path}' was not found. Please check the path.")
except UnicodeDecodeError as e:
    print("An encoding error occurred:", e)
