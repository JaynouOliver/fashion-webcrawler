import requests
import json
url = "https://api.apify.com/v2/datasets/iTXZprbyXjIm4G4Vj/items?token=apify_api_8AfFZEsvs0fn84FKmi9rTQpxZDfspo0iJfEP"

response = requests.get(url)

print(response.json())



# save response to json file
with open('response.json', 'w') as f:
    json.dump(response.json(), f)


#json struct is like this 
# [
#     {
#         "url": "https://www.westside.com/",
#         "crawl": {
#             "loadedUrl": "https://www.westside.com/",
#             "loadedTime": "2025-06-27T08:12:25.910Z",
#             "referrerUrl": "https://www.westside.com/",
#             "depth": 0,
#             "httpStatusCode": 200

# we need to extract the loadedUrl from the json file

# read json file
try:
    with open('response.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: response.json file not found")
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON format in response.json")
    exit(1)

# extract loadedUrl from the json file using list comprehension
loadedUrls = [item['crawl']['loadedUrl'] 
              for item in data 
              if 'crawl' in item and 'loadedUrl' in item['crawl']]

# Keep original variable name for compatibility
loadedUrl = loadedUrls

# print number of URLs found and the URLs
print(f"Found {len(loadedUrl)} URLs:")
for url in loadedUrl:
    print(f"- {url}")

# save all loadedUrls to another json file with proper formatting
try:
    with open('loadedUrls.json', 'w') as f:
        json.dump(loadedUrl, f, indent=4)
    print("Successfully saved URLs to loadedUrls.json")
except IOError:
    print("Error: Unable to write to loadedUrls.json")
