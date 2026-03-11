from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


search = input("Search after: ")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(f"https://www.bing.com/search?q={search}")

# Wait till the DOM is all loaded
time.sleep(15)

soup = BeautifulSoup(driver.page_source, "html.parser") # Parsing a structured tree out of HTML
results = soup.find("ol", {"id": "b_results"}) #  Find by tag and id

driver.quit() # Closes all browser windows and fully shuts down the ChromeDriver process

# Create the directory if it doesn't exist
output_dir = "scraped_searches"
os.makedirs(output_dir, exist_ok=True)

if not results:
    print("No results found")
else:
    links = results.find_all("li", {"class": "b_algo"})

    filepath = os.path.join(output_dir, f"{search}_results.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Search results for: {search}\n")
        f.write("=" * 50 + "\n\n")

        for item in links:
            title_tag = item.find(class_="tptt")
            url_tag = item.find(class_="b_attribution")

            title = title_tag.text if title_tag else "No title"

            if url_tag:
                a_tag = url_tag.find("a")
                url = a_tag.text.strip() if a_tag else url_tag.text.strip()  # fallback to raw text
            else:
                url = "No URL"

            if title == "No title" and url == "No URL":
                continue

            p_tag = item.find(class_="b_lineclamp2")
            if p_tag:
                summary = p_tag.text.strip() if p_tag else "No summary"
            else:
                summary = "No summary"

            print(title)
            print(url)
            print("Summary:", summary)
            print("---")

            f.write(f"Title: {title}\n")
            f.write(f"URL:   {url}\n")
            f.write(f"Summary:  {summary}\n")
            f.write("-" * 50 + "\n")

    print(f"\nResults saved to '{search}_results.txt'")