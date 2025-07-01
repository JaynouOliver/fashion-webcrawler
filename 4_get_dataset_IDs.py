# get list of runs 

import requests
import json

url = "https://api.apify.com/v2/acts/apify~web-scraper/runs?token=apify_api_8AfFZEsvs0fn84FKmi9rTQpxZDfspo0iJfEP"

response = requests.get(url)

data = response.json()

# print the data
print(data)

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
    with open('2.dataset_ids.json', 'w') as f:
        json.dump(dataset_ids, f, indent=4)
    print("\nSuccessfully saved dataset IDs to 2.dataset_ids.json")
except IOError:
    print("Error: Unable to write to 2.dataset_ids.json")
