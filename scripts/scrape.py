import argparse
import requests
from multiprocessing import Pool, cpu_count
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="whee")
parser.add_argument("--num-process", type=int, help="How many processes to spawn for scraping", required=True)
args = parser.parse_args()
NUM_PROCESSES=args.num_process

URL = "https://www.target.com/p/pok-233-mon-trading-card-game-kleavor-vstar-premium-collection/-/A-94091371"
def scrape(pid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(URL, headers=headers)
    if response:
        print(f"{pid}: got response!")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract Product Title
        title = soup.find("h1", {"data-test": "product-title"})
        title_text = title.text.strip() if title else "Title not found"

        # Extract Price
        cur_retail = soup.find("span", {"data-test": "current_retail"})

        print(f"Product: {title_text}")
        print(f"Price: {cur_retail}")
    else:
        print(f"Failed to fetch page, status code: {response.status_code}")

if __name__ == "__main__":
    with Pool(NUM_PROCESSES) as pool:
        pool.map(scrape, range(1, NUM_PROCESSES+1))
