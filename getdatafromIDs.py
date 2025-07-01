import json 
import requests


# get the list of dataset ids from dataset_ids.json
with open('dataset_ids.json', 'r') as f:
    dataset_ids = json.load(f)

# print the number of dataset ids
print(f"Found {len(dataset_ids)} dataset IDs")

# get the data from the dataset ids
# Initialize empty list to store all data
all_data = []

for x in dataset_ids:
    # Get data from each dataset ID
    url = f"https://api.apify.com/v2/datasets/{x}/items?token=apify_api_8AfFZEsvs0fn84FKmi9rTQpxZDfspo0iJfEP"
    response = requests.get(url)
    data = response.json()
    
    # Extend all_data with the results from this dataset
    all_data.extend(data)
    print(f"Added {len(data)} items from dataset {x}")

# Save the combined data to a single json file
with open('combined_data.json', 'w') as f:
    json.dump(all_data, f, indent=4)

print(f"Successfully combined {len(all_data)} total items into combined_data.json")