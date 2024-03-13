import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
import time

urls = {
  "Abstract": [
      "https://symplico.com/collections/abstract/Abstract?page="],
  "Tropical": [
      "https://symplico.com/collections/tropical/Tropical?page="],
  "Ajrakh": [
      "https://symplico.com/collections/ajrakh/Ajrakh?page="],
  "Ikat": [
      "https://symplico.com/collections/ikat/Ikat?page="],
  "Patola": [
      "https://symplico.com/collections/patola/Patola?page="],
  "Paisley": [
      "https://symplico.com/collections/paisley/Paisley?page="],
  "Bagru": [
      "https://symplico.com/collections/bagru/Bagru?page="],
  "Ethnic": [
      "https://symplico.com/collections/ethnic/Ethnic?page="],
  "Pichwai": [
      "https://symplico.com/collections/pichwai/Pichwai?page="],
  "Sanganeri": [
      "https://symplico.com/collections/sanganeri/Sanganeri?page="],
  "Bandhani": [
      "https://symplico.com/collections/bandhani/Bandhani?page="],
  "Mughal": [
      "https://symplico.com/collections/mughal/Mughal?page="],
  "Batik": [
      "https://symplico.com/collections/batik/Batik?page="],
  "Indigo": [
      "https://symplico.com/collections/indigo/Indigo?page="],
  "Contemporary": [
      "https://symplico.com/collections/contemporary/Contemporary?page="],
  "Floral": [
      "https://symplico.com/collections/floral/Floral?page="],
  "Watercolor": [
      "https://symplico.com/collections/watercolor/Watercolor?page="],
  "Shapes": [
      "https://symplico.com/collections/shapes/Shapes?page="],
  "Stripes": [
      "https://symplico.com/collections/stripes/Stripes?page="],
  "Pantone": [
      "https://symplico.com/collections/pantone/Pantone?page="],
  "Geometric": [
      "https://symplico.com/collections/geometric/Geometric?page="],
  "Animal": [
      "https://symplico.com/collections/animal/Animal?page="],
  "Summer": [
      "https://symplico.com/collections/summer/Summer?page="],
  "Kids": [
      "https://symplico.com/collections/kids/Kids?page="],
  "Christmas": [
      "https://symplico.com/collections/christmas/Christmas?page="],
  "Seasonal": [
      "https://symplico.com/collections/seasonal/Seasonal?page="],
  "Small Prints": [
      "https://symplico.com/collections/small-prints/Small-Prints?page="],
  "Large Prints": [
      "https://symplico.com/collections/large-prints/Large-Prints?page="],
  "Figure": [
      "https://symplico.com/collections/figure/Figure?page="],
  "Madhubani": [
      "https://symplico.com/collections/madhubani/Madhubani?page="]
}


def extract(url, category):
    response = requests.get(url)
    print(url, response.status_code, response.reason, response.url, category)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_items = soup.find_all('li', class_='product')
    if product_items:
        for product_item in product_items:
            image_tag = product_item.find('a', class_='card-media').find('img')

            srcset = image_tag['data-srcset']
            image_url = srcset.split()[0]

            parsed_image_url = urlparse(image_url)

            if not parsed_image_url.scheme:
                image_url = urljoin(url, image_url)
            title = product_item.find('a', class_='card-title')['data-product-title']
            image_response = requests.get(image_url)


            if image_response.status_code == 200:
                category_folder = os.path.join('images', category)
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
                        break
                else:
                    break
            time.sleep(1) 


check_all_urls()
print("All done!")
