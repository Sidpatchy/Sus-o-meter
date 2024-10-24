import asyncio

import requests
from browser_history import get_history
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

async def main():
    # Store browser history and bookmarks
    history = get_history().histories

    # Store sussy keywords
    with open("primary-dataset.txt", "r") as f:
        primary_dataset = [line.strip() for line in f.readlines()]

    with open("secondary-dataset.txt", "r") as f:
        secondary_dataset = [line.strip() for line in f.readlines()]

    # Precompile regular expressions
    primary_dataset_regex = [re.compile(entry) for entry in primary_dataset]
    secondary_dataset_regex = [re.compile(entry) for entry in secondary_dataset]

    # Variables to store the results
    total_detections = 0
    detected_urls = []
    total_secondary_detections = 0
    secondary_detections = []

    # Loop through history and print the title and URL
    for entry in tqdm(history, desc="Processing URLs", unit="URL"):
        date, url, title = entry

        for regex in primary_dataset_regex:
            if regex.search(url):
                total_detections += 1
                detected_urls.append(url)

    print(f"I found {total_detections} total URLs in the dataset.")

    print("\nAnalyzing URLs to minimize false-positives...")
    for url in tqdm(detected_urls, desc="Checking URLS", unit="URL"):
        title = await get_webpage_title(url)

        for regex in secondary_dataset_regex:
            if regex.search(title):
                total_secondary_detections += 1
                secondary_detections.append([url, title])

    print(f"\nAfter attempting to rule out false positives, I found {total_secondary_detections} total URLs.\n")

    if total_secondary_detections > 0:
        display_urls = input("Would you like to display the URLs I found? [Y/n] ")

        if display_urls.upper() == "Y" or display_urls == "":
            for i in secondary_detections:
                print(i)

    display_primary_urls = input("Would you like to display the URLs I found before I attempted to rule them out? [Y/n] ")

    if display_primary_urls.upper() == "Y" or display_primary_urls == "":
        for i in detected_urls:
            print(i)

    print("\n\nGoodbye!")


async def get_webpage_title(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.title.string.strip()
    except:
        return ""

if __name__ == "__main__":
    asyncio.run(main())
