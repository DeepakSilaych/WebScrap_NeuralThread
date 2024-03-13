import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
import time

urls = {
  "Floral Prints": ["https://www.rococodesigns.in/floral-prints?page="],
  "Tropical And Animal":["https://www.rococodesigns.in/tropicalandanimalprint?page="],
  "Ethenic Prints":["https://www.rococodesigns.in/ethnic-prints?page="],
  "Kids Prints":["https://www.rococodesigns.in/kids-prints?page="],
  "Abstract Art" : ["https://www.rococodesigns.in/abstract-art?page="],
  "Taste of Africa" : ["https://www.rococodesigns.in/taste-of-africa?page="],
  "Graphic Geometric Print" : ["https://www.rococodesigns.in/graphic-geometric-print?page="],
  "Toile Print" : ["https://www.rococodesigns.in/toile-print?page="],
}


def extract(url, category):
    response = requests.get(url)
    print(url, response.status_code, response.reason, response.url, category)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_items = soup.find_all(attrs={'data-hook': 'product-list-grid-item'})
    if product_items:
        for product_item in product_items:
            image_tag = product_item.find('img')
            title = product_item.find('h3', class_='s__03qxBT').text.strip()
            src = image_tag['src']
            image_url = src.split()[0]

            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                category_folder = os.path.join('images', category)
                os.makedirs(category_folder, exist_ok=True)
                image_filename = os.path.join(category_folder, f"{title}.jpg")
                with open(image_filename, 'wb') as f:
                    f.write(image_response.content)
                print(f"Image saved: {image_filename}")
            else:
                print(f"Failed to download image for {title}")
        return True
    else:
        print(f"No .product list items found for {url}")
        return False



def check_all_urls():
    for category, url_list in urls.items():
        print(f"Category: {category}")
        
        for url in url_list:
            idx = 1
            while True:
                full_url = url + str(idx)
                print(f"Scraping images from: {full_url}")
                response = requests.get(full_url)
                if response.status_code == 200:
                    if extract(full_url, category):
                        print("")
                        idx += 1
                    else: # if url does not have any more pages, breaking the loop
                        break
                else:
                    break
            time.sleep(1) 


check_all_urls()
print("All done!")
