# get list of runs 

import requests
import json

url = "https://api.apify.com/v2/acts/apify~web-scraper/runs?token=apify_api_8AfFZEsvs0fn84FKmi9rTQpxZDfspo0iJfEP"

response = requests.get(url)

print(response.json())

# save the response to a json file as ac
with open('actors.json', 'w') as f:
    json.dump(response.json(), f)


# read the actors.json file
try:
    with open('actors.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: actors.json file not found")
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON format in actors.json")
    exit(1)

# extract all defaultDatasetId values using list comprehension
dataset_ids = [item['defaultDatasetId'] 
               for item in data['data']['items'] 
               if 'defaultDatasetId' in item]

# print number of dataset IDs found and the IDs
print(f"\nFound {len(dataset_ids)} dataset IDs:")
for dataset_id in dataset_ids:
    print(f"- {dataset_id}")

# save dataset IDs to a new json file
try:
    with open('dataset_ids.json', 'w') as f:
        json.dump(dataset_ids, f, indent=4)
    print("\nSuccessfully saved dataset IDs to dataset_ids.json")
except IOError:
    print("Error: Unable to write to dataset_ids.json")
