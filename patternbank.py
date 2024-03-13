import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
import time

urls = {
  "Geometric": ["https://patternbank.com/studio/7-geometric?licence=all&page="],
  "Floral": ["https://patternbank.com/studio/10-floral?licence=all&page="],
  "Animals/Birds": ["https://patternbank.com/studio/16-animals-birds?licence=all&page="],
  "Ethnic": ["https://patternbank.com/studio/19-ethnic?licence=all&page="],
  "Conversationals": ["https://patternbank.com/studio/22-conversationals?licence=all&page="],
  "Abstract": ["https://patternbank.com/studio/25-abstract?licence=all&page="],
  "Checks": ["https://patternbank.com/studio/28-checks?licence=all&page="],
  "Stripes": ["https://patternbank.com/studio/31-stripes?licence=all&page="],
  "Paisleys": ["https://patternbank.com/studio/34-paisleys?licence=all&page="],
  "Tropical": ["https://patternbank.com/studio/37-tropical?licence=all&page="],
  "Traditional": ["https://patternbank.com/studio/40-traditional?licence=all&page="],
  "Placements": ["https://patternbank.com/studio/43-placements?licence=all&page="],
  "Texture": ["https://patternbank.com/studio/55-texture?licence=all&page="],
  "Camouflage": ["https://patternbank.com/studio/58-camouflage?licence=all&page="],
  "Animal Skins": ["https://patternbank.com/studio/94-animal-skins?licence=all&page="],
  "Nature": ["https://patternbank.com/studio/101-nature?licence=all&page="],
  "Tribal": ["https://patternbank.com/studio/102-tribal?licence=all&page="],
  "Border": ["https://patternbank.com/studio/104-border?licence=all&page="]
}



def extract(url, category):
    response = requests.get(url)
    print(url, response.status_code, response.reason, response.url, category)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_items = soup.find_all('div', class_='product-col')
    if product_items:
        for product_item in product_items:
            image_tag = product_item.find('img')

            image_url = image_tag['data-src']
            title_element = product_item.find('span', class_='design-name')
            title = title_element.text.strip() if title_element else "Untitled"
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                category_folder = os.path.join('patternbank', category)
                os.makedirs(category_folder, exist_ok=True)
                image_filename = os.path.join(category_folder, f"{title}.jpg")
                with open(image_filename, 'wb') as f:
                    f.write(image_response.content)
                print(f"Image saved: {image_filename}")
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
                        print("------------ done wth ", full_url, " ------------")
                        break
                else:
                    break
            time.sleep(1) 


check_all_urls()
print("All done!")
