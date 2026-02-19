import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

BASE_URL = "https://ikman.lk"
SEARCH_URL = "https://ikman.lk/en/ads/sri-lanka/cars?page="

headers = {
    "User-Agent": "Mozilla/5.0"
}

car_data = []

def get_listing_links(page):
    url = SEARCH_URL + str(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    links = []
    for a in soup.find_all("a", href=True):
        if "/en/ad/" in a["href"]:
            links.append(BASE_URL + a["href"])

    return list(set(links))


def scrape_listing(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    try:
        price = soup.find("div", class_="amount--3NTpl").text.strip()
    except:
        price = None

    details = {}

    meta_sections = soup.find_all("div", class_="full-width--XovDn")

    for section in meta_sections:
        try:
            label = section.find("div", class_=lambda x: x and "label" in x).text.strip().replace(":", "")
            value_div = section.find("div", class_=lambda x: x and "value" in x)
            value = value_div.text.strip()
            details[label] = value
        except:
            continue

    car_data.append({
        "url": url,
        "price": price,
        "brand": details.get("Brand"),
        "model": details.get("Model"),
        "year": details.get("Year of Manufacture"),
        "condition": details.get("Condition"),
        "transmission": details.get("Transmission"),
        "body_type": details.get("Body type"),
        "fuel_type": details.get("Fuel type"),
        "engine_capacity": details.get("Engine capacity"),
        "mileage": details.get("Mileage")
    })


def main():
    for page in range(1, 400):
        print(f"Scraping page {page}")
        links = get_listing_links(page)

        for link in links:
            print("Scraping:", link)
            scrape_listing(link)

    df = pd.DataFrame(car_data)
    df.to_csv("ikman_cars_raw.csv", index=False)


if __name__ == "__main__":
    main()
