from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import os
import json
import re
from PIL import Image
from io import BytesIO


def clean_filename(name):
    return re.sub(r'[<>:"/\\|?!*]', '', name).strip()

def StartSearch():
    search = input("Search for images: ")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f"https://www.bing.com/images/search?q={search}")

    time.sleep(15)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Each image result is an <a class="iusc"> tag with a JSON attribute "m" containing the image URL
    results = soup.find_all("a", {"class": "iusc"})

    # Create subfolder based on search term e.g. scraped_images/pizza/
    output_dir = os.path.join("scraped_images", search.replace(" ", "_"))
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    if not results:
        print("No results found")
    else:
        saved = 0

        for item in results:
            if saved >= 5:  # stop after 5 images
                break

            try:
                m = json.loads(item["m"])  # The "m" attribute contains a JSON object with the image URL
                img_url = m["murl"]  # direct image URL
                raw_title = m.get("t", f"image_{saved}").replace(" ", "_")
                title = clean_filename(raw_title)

                print(f"Getting URL: {img_url}")

                r = requests.get(img_url, headers=headers, timeout=5)

                img = Image.open(BytesIO(r.content))
                img = img.convert("RGB") # Convert to RGB so we can always save as JPG

                filepath = os.path.join(output_dir, f"{title}.jpg")
                img.save(filepath, "JPEG")

                saved += 1
            except Exception as e:
                print(f"Skipping image due to error: {e}")
                continue
        print(f"Images saved to '{output_dir}'")
    StartSearch()

StartSearch()