from apify_client import ApifyClient
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
ACTOR_ID = 'aYG0l9s7dbB7j3gbS'  # Your section/category crawler actor

# List of required domains
domains = [
    'https://www.virgio.com/',
    'https://www.tatacliq.com/',
    'https://nykaafashion.com/',
    'https://www.westside.com/'
]

# Create client
client = ApifyClient(APIFY_TOKEN)

# Convert domains to startUrls format
start_urls = [{"url": domain} for domain in domains]

run_input = {
    "startUrls": start_urls,
    "useSitemaps": False,
    "respectRobotsTxtFile": True,
    "crawlerType": "playwright:adaptive",
    "includeUrlGlobs": [],
    "excludeUrlGlobs": [],
    "keepUrlFragments": False,
    "ignoreCanonicalUrl": False,
    "ignoreHttpsErrors": False,
    "maxCrawlDepth": 20,
    "maxCrawlPages": 9999999,
    "initialConcurrency": 0,
    "maxConcurrency": 200,
    "initialCookies": [],
    "proxyConfiguration": {"useApifyProxy": True},
    "maxSessionRotations": 10,
    "maxRequestRetries": 3,
    "requestTimeoutSecs": 60,
    "minFileDownloadSpeedKBps": 128,
    "dynamicContentWaitSecs": 10,
    "waitForSelector": "",
    "softWaitForSelector": "",
    "maxScrollHeightPixels": 5000,
    "keepElementsCssSelector": "",
    "removeElementsCssSelector": "nav, footer, script, style, noscript, svg, img[src^='data:'],\n[role=\"alert\"],\n[role=\"banner\"],\n[role=\"dialog\"],\n[role=\"alertdialog\"],\n[role=\"region\"][aria-label*=\"skip\" i],\n[aria-modal=\"true\"]",
    "removeCookieWarnings": True,
    "blockMedia": True,
    "expandIframes": True,
    "clickElementsCssSelector": "[aria-expanded=\"false\"]",
    "htmlTransformer": "readableText",
    "readableTextCharThreshold": 100,
    "aggressivePrune": False,
    "debugMode": False,
    "debugLog": False,
    "saveHtml": False,
    "saveHtmlAsFile": False,
    "saveMarkdown": True,
    "saveFiles": False,
    "saveScreenshots": False,
    "maxResults": 9999999,
    "clientSideMinChangePercentage": 15,
    "renderingTypeDetectionPercentage": 10
}

print("Starting crawl for all domains...")
print(f"Domains to crawl: {domains}")

# Start the actor run
run = client.actor(ACTOR_ID).call(run_input=run_input, timeout_secs=60)
run_id = run['id']

print(f"Actor run started with ID: {run_id}")

# Poll for completion
while True:
    run_status = client.run(run_id).get()['status']
    print(f"Run status: {run_status}")
    if run_status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
        break
    time.sleep(10)

# Fetch results
results = []
if 'defaultDatasetId' in run:
    for item in client.dataset(run['defaultDatasetId']).iterate_items():
        results.append(item)

# Save all results to a single JSON file
output_filename = "fashion_websites_crawl_results.json"
with open(output_filename, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Crawl completed!")
print(f"Total results: {len(results)}")
print(f"Results saved to: {output_filename}")
print(f"Final run status: {run_status}")
