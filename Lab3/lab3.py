import argparse
import requests
from bs4 import BeautifulSoup
import json

parser = argparse.ArgumentParser(description="This script scrapes")
parser.add_argument("f", help="Name of file", type=str)
args = parser.parse_args()

req = requests.get("https://www.filmweb.pl/ranking/serial")

soup = BeautifulSoup(req.text, 'html.parser')
divs = soup.find_all('div', class_="rankingType__card")

lst = []
place = 0

for div in divs:
    place += 1
    polish_title = div.find('div', class_="rankingType__header").find('div', class_="rankingType__titleWrapper").find('h2', class_="rankingType__title").find('a').text
    original_title = div.find('div', class_="rankingType__header").find('p').text[:(len(div.find('div', class_="rankingType__header").find('p').text) - 4)]
    year = div.find('div', class_="rankingType__header").find('p').find('span').text
    genre = div.find('div', class_="rankingType__genres").text.replace("gatunek", "")
    rate_value = div.find('div', class_="rankingType__rateWrapper").find('div', class_="rankingType__rate").find('span', class_="rankingType__rate--value").text
    rate_count = div.find('div', class_="rankingType__rateWrapper").find('div', class_="rankingType__rate").find('span', class_="rankingType__rate--count").find('span').text.replace(" ", "")
    dict = {"place": place, "polish_title": polish_title, "original_title": original_title, "year": year, "genre": genre, "rate_value": rate_value, "rate_count": rate_count}
    lst.append(dict)

with open(f"./output/{args.f}.json", "w", encoding="utf-8") as f:
    json.dump(lst, f)
