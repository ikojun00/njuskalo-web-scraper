import csv
import re
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()
urls = []

with open('bjelovarsko-bilogorska_links.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    next(file)
    for row in reader:
        urls.append(row[2])

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

csv_header = ["Date", "Views", "Price", "Living area", "County", "City", "Neighborhood", "Number of rooms", "Type of flat", "Number of floors", "Furnishing", "Energy class", "Floor", "Year of construction", "Url"]

with open('bjelovarsko-bilogorska_info.csv', 'w', newline='', encoding='utf8') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    
    with requests.Session() as session:
        for counter, url in enumerate(urls, start=1):
            response = session.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            price = re.sub(r',.*', '', soup.select_one('dd.ClassifiedDetailSummary-priceDomestic').text.replace(" ", "").replace("€", "").replace(".", "").strip())
            date = soup.select_one('dd.ClassifiedDetailSystemDetails-listData').text.strip().split(' ')[0]
            views = soup.select('dd.ClassifiedDetailSystemDetails-listData')[2].text.strip().split(' ')[0]
            values = soup.select('span.ClassifiedDetailBasicDetails-textWrapContainer')
            result = ""
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

            county_pattern = r"County:\s*([^\n]+)"
            city_pattern = r"City:\s*([^\n]+)"
            neighborhood_pattern = r"Neighborhood:\s*([^\n]+)"
            number_of_rooms_pattern = r"Broj soba:\s*(\d+)"
            type_of_flat_pattern = r"Tip stana:\s*([^\n]+)"
            number_of_floors_pattern = r"Broj etaža:\s*([^\n]+)"
            living_area_pattern = r"Stambena površina:\s*(\d+)"
            furnishing_pattern = r"Namještenost i stanje:\s*([^\n]+)"
            energy_class_pattern = r"Energetski razred:\s*([^\n]+)"
            floor_pattern = r"Kat:\s*([^\n]+)"
            year_of_construction_pattern = r"Godina izgradnje:\s*([^\n]+)"

            county = re.search(county_pattern, result)
            county = county.group(1) if county else "Unknown"

            city = re.search(city_pattern, result)
            city = city.group(1) if city else "Unknown"

            neighborhood = re.search(neighborhood_pattern, result)
            neighborhood = neighborhood.group(1) if neighborhood else "Unknown"

            number_of_rooms = re.search(number_of_rooms_pattern, result)
            number_of_rooms = number_of_rooms.group(1) if number_of_rooms else "Unknown"

            type_of_flat = re.search(type_of_flat_pattern, result)
            type_of_flat = type_of_flat.group(1) if type_of_flat else "Unknown"

            number_of_floors = re.search(number_of_floors_pattern, result)
            number_of_floors = number_of_floors.group(1) if number_of_floors else "Unknown"

            living_area = re.search(living_area_pattern, result)
            living_area = living_area.group(1) if living_area else "Unknown"

            furnishing = re.search(furnishing_pattern, result)
            furnishing = furnishing.group(1) if furnishing else "Unknown"

            energy_class = re.search(energy_class_pattern, result)
            energy_class = energy_class.group(1) if energy_class else "Unknown"

            floor = re.search(floor_pattern, result)
            floor = floor.group(1) if floor else "Unknown"

            year_of_construction = re.search(year_of_construction_pattern, result)
            year_of_construction = year_of_construction.group(1) if year_of_construction else "Unknown"
            
            writer.writerow([date, views, price, living_area, county, city, neighborhood, number_of_rooms, type_of_flat, number_of_floors, furnishing, energy_class, floor, year_of_construction, url])

            progress_percentage = (counter / len(urls)) * 100
            print(f"Progress: {progress_percentage:.2f}%")