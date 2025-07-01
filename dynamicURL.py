from apify_client import ApifyClient
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv
import requests
load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = "moJRLRc85AitArpNN"
RUN_TIMEOUT_SECS = 120  # 2 minutes per run

# Load URLs from JSON file
with open("loadedUrls.json", "r") as f:
    urls = json.load(f)

def run_apify_for_url(url):
    client = ApifyClient(APIFY_TOKEN)
    run_input = {
        "runMode": "DEVELOPMENT",
        "startUrls": [{"url": url}],
        "keepUrlFragments": True,
        "respectRobotsTxtFile": True,
        "linkSelector": "a[href]",
        "globs": [{"glob": "**/products/**"}],
        "pseudoUrls": [],
        "excludes": [],
        "pageFunction": """async function pageFunction(context) {
            const $ = context.jQuery;
            const productLinks = [];
            $('a[href*="/products/"]').each((i, el) => {
                const href = $(el).attr('href');
                let url = href;
                if (href && !href.startsWith('http')) {
                    url = new URL(href, context.request.loadedUrl).href;
                }
                productLinks.push(url);
            });
            const uniqueProductLinks = [...new Set(productLinks)];
            context.log.info(`Found ${uniqueProductLinks.length} product links on ${context.request.url}`);
            return {
                page: context.request.url,
                productUrls: uniqueProductLinks
            };
        }""",
        "injectJQuery": True,
        "proxyConfiguration": {"useApifyProxy": True},
        "proxyRotation": "RECOMMENDED",
        "initialCookies": [],
        "useChrome": True,
        "headless": True,
        "ignoreSslErrors": False,
        "ignoreCorsAndCsp": False,
        "downloadMedia": True,
        "downloadCss": True,
        "maxRequestRetries": 3,
        "maxPagesPerCrawl": 0,
        "maxResultsPerCrawl": 0,
        "maxCrawlingDepth": 0,
        "maxConcurrency": 50,
        "pageLoadTimeoutSecs": 60,
        "pageFunctionTimeoutSecs": 60,
        "waitUntil": ["networkidle2"],
        "preNavigationHooks": "[async (crawlingContext, gotoOptions) => {}]",
        "postNavigationHooks": "[async (crawlingContext) => {}]",
        "breakpointLocation": "NONE",
        "closeCookieModals": False,
        "maxScrollHeightPixels": 5000,
        "debugLog": False,
        "browserLog": False,
        "customData": {},
    }

    # Start the run
    run = client.actor(ACTOR_ID).call(run_input=run_input, timeout_secs=RUN_TIMEOUT_SECS)
    run_id = run["id"]
    start_time = time.time()

    while True:
        status = client.run(run_id).get()["status"]
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        if time.time() - start_time > RUN_TIMEOUT_SECS:
            client.run(run_id).abort(gracefully=True)
            print(f"Run for {url} aborted after {RUN_TIMEOUT_SECS} seconds.")
            break
        time.sleep(5)
    run_id = run["id"]
    start_time = time.time()

    # Poll for completion or timeout
    while True:
        status = client.run(run_id).get()["status"]
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        if time.time() - start_time > RUN_TIMEOUT_SECS:
            client.run(run_id).abort(gracefully=True)
            print(f"Run for {url} aborted after {RUN_TIMEOUT_SECS} seconds.")
            break
        time.sleep(5)

    # Fetch results
    results = []
    if "defaultDatasetId" in run:
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(item)
    return {"url": url, "results": results}

# Run all URLs concurrently
all_results = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(run_apify_for_url, url) for url in urls]
    for future in as_completed(futures):
        all_results.append(future.result())

