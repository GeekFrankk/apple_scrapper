import json
#path for the masters file
master_json_path = './app_store_scraper/master_file.json'  

try:
    with open(master_json_path, 'r', encoding='utf-8') as master_file:
        data = json.load(master_file)

    # Extract the  appDescriptions (changes if needed in the future)
    descriptions = [item['appDescription'] for item in data if 'appDescription' in item]

    # Save to descriptions JSON file
    output_path =  './app_store_scraper/descriptions/descriptions.json' 
    with open(output_path, 'w', encoding='utf-8') as descriptions_file:
        json.dump(descriptions, descriptions_file, indent=4)

    print(f"Descriptions have been extracted and saved to '{output_path}'.")

except UnicodeDecodeError as e:
    print("An encoding error occurred:", e)
