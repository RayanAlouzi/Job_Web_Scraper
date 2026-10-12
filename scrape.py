import csv
import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"


def get_text(parent, selector):
    """Return the stripped text of the first match, or 'N/A' if missing."""
    el = parent.select_one(selector)
    return el.get_text(strip=True) if el else "N/A"


def get_apply_link(card):
    """Return the href of the 'Apply' link, or 'N/A' if missing."""
    for link in card.select("a.card-footer-item"):
        if link.get_text(strip=True) == "Apply":
            return link.get("href", "N/A")
    return "N/A"


response = requests.get(URL, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

cards = soup.select("div.card-content")

with open("jobs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Company", "Location", "Details"])

    for card in cards:
        row = [
            get_text(card, "h2.title"),
            get_text(card, "h3.company"),
            get_text(card, "p.location"),
            get_apply_link(card),
        ]
        writer.writerow(row)

print(f"Saved {len(cards)} jobs to jobs.csv")