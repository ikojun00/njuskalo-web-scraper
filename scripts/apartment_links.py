import csv
import re
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()
county = "vrbovsko"

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'accept-language': 'hr-HR,hr;q=0.6',
  'cache-control': 'max-age=0',
  'referer': 'https://www.njuskalo.hr/prodaja-stanova',
  'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
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

csv_header = ["Date", "Price", "Url"]

with open(f'{county}_links.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    rows = 0
    
    with requests.Session() as session:
        response = session.get(f"https://www.njuskalo.hr/prodaja-stanova/{county}", headers=headers)
        apartment_links = []

        counter = 0
        while True:
            soup = BeautifulSoup(response.text, 'html.parser')
            apartments = soup.select("li.EntityList-item.EntityList-item--VauVau.bp-radix__faux-anchor") + soup.select("li.EntityList-item.EntityList-item--Regular.bp-radix__faux-anchor")
            
            for apartment in apartments:
                link = f"https://www.njuskalo.hr{apartment['data-href']}"
                if link not in apartment_links:
                    apartment_links.append(link)
                    date = apartment.select_one("time.date").text
                    price = re.sub(r',.*', '', apartment.select_one('li.price-item').text.replace(" ", "").replace("€", "").replace(".", "").strip())
                    writer.writerow([date, price, link])
                    rows += 1
            
            try:
                next_page = soup.select_one("li.Pagination-item.Pagination-item--next > button")['data-page']
            except:
                break
            
            counter += 1
            print(f"{counter}. page done!")

            response = session.get(f"https://www.njuskalo.hr/prodaja-stanova/{county}?page={next_page}", headers=headers)
    
        print(f"{rows} rows!")
                
                