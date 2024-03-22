import csv
import re
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()
urls = []

with open('apartment_links_3.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        urls.extend(row)

headers = {
  'authority': 'www.njuskalo.hr',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'accept-language': 'hr-HR,hr;q=0.8',
  'cache-control': 'max-age=0',
  'referer': 'https://www.njuskalo.hr/prodaja-stanova',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'sec-gpc': '1',
  'upgrade-insecure-requests': '1',
  'user-agent': ua.random
}

csv_header = ["Price", "Living area", "County", "City", "Neighborhood", "Number of rooms", "Type of flat", "Number of floors"]

with open('apartment_info_3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    
    with requests.Session() as session:
        for counter, url in enumerate(urls, start=1):
            response = session.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            price = soup.select_one('dd.ClassifiedDetailSummary-priceDomestic').text.replace(" ", "").replace("€", "").replace(".", "")
            values = soup.select('span.ClassifiedDetailBasicDetails-textWrapContainer')
            result = f"Cijena: {price}"
            for i, value in enumerate(values, start=1):
                text = value.get_text(strip=True)
                if(i != 1):
                    if i % 2 != 0:
                        result += text + ": "
                    elif i == 2:
                        location = text.split(", ")
                        result += f"County: {location[0]}\n"
                        result += f"City: {location[1]}\n"
                        result += f"Neighborhood: {location[2]}\n"
                    else:
                        result += text + "\n"

            price_pattern = r"Cijena:\s*(\d+)"
            county_pattern = r"County:\s*([^\n]+)"
            city_pattern = r"City:\s*([^\n]+)"
            neighborhood_pattern = r"Neighborhood:\s*([^\n]+)"
            city_pattern = r"City:\s*([^\n]+)"
            number_of_rooms_pattern = r"Broj soba:\s*([^\n]+)"
            type_of_flat_pattern = r"Tip stana:\s*([^\n]+)"
            number_of_floors_pattern = r"Broj etaža:\s*([^\n]+)"
            living_area_pattern = r"Stambena površina:\s*(\d+)"


            price = re.search(price_pattern, result).group(1)
            county = re.search(county_pattern, result).group(1)
            city = re.search(city_pattern, result).group(1)
            neighborhood = re.search(neighborhood_pattern, result).group(1)
            number_of_rooms = re.search(number_of_rooms_pattern, result).group(1)
            type_of_flat = re.search(type_of_flat_pattern, result).group(1)
            number_of_floors = re.search(number_of_floors_pattern, result).group(1)
            living_area = re.search(living_area_pattern, result).group(1)

            writer.writerow([price, living_area, county, city, neighborhood, number_of_rooms, type_of_flat, number_of_floors])

            progress_percentage = (counter / len(urls)) * 100
            print(f"Progress: {progress_percentage:.2f}%")