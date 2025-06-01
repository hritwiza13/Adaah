import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
from config import FILE_PATHS, SCRAPING_SETTINGS
import re
from urllib.parse import urljoin

class FashionScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.data = []
        
    def scrape_asos(self, category):
        """Scrape fashion items from ASOS"""
        base_url = f"https://www.asos.com/search/?q={category}"
        try:
            response = requests.get(base_url, headers=self.headers, timeout=SCRAPING_SETTINGS['timeout'])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find product cards
            products = soup.find_all('article', {'data-testid': 'product-card'})
            
            for product in products[:10]:  # Get top 10 items
                try:
                    # Extract product details
                    title = product.find('h3').text.strip()
                    img = product.find('img')
                    img_url = img.get('src') or img.get('data-src')
                    if img_url:
                        img_url = urljoin('https://www.asos.com', img_url)
                    
                    # Extract price
                    price = product.find('span', {'data-testid': 'current-price'})
                    price = price.text.strip() if price else 'N/A'
                    
                    # Extract brand
                    brand = product.find('h2')
                    brand = brand.text.strip() if brand else 'ASOS'
                    
                    self.data.append({
                        'source': 'ASOS',
                        'title': title,
                        'image_url': img_url,
                        'price': price,
                        'brand': brand,
                        'category': category,
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error parsing ASOS product: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping ASOS: {e}")

    def scrape_hm(self, category):
        """Scrape fashion items from H&M"""
        base_url = f"https://www2.hm.com/en_us/search-results.html?q={category}"
        try:
            response = requests.get(base_url, headers=self.headers, timeout=SCRAPING_SETTINGS['timeout'])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find product items
            products = soup.find_all('article', {'class': 'hm-product-item'})
            
            for product in products[:10]:  # Get top 10 items
                try:
                    # Extract product details
                    title = product.find('h3', {'class': 'item-heading'}).text.strip()
                    img = product.find('img')
                    img_url = img.get('src') or img.get('data-src')
                    if img_url:
                        img_url = urljoin('https://www2.hm.com', img_url)
                    
                    # Extract price
                    price = product.find('span', {'class': 'price'})
                    price = price.text.strip() if price else 'N/A'
                    
                    self.data.append({
                        'source': 'H&M',
                        'title': title,
                        'image_url': img_url,
                        'price': price,
                        'brand': 'H&M',
                        'category': category,
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error parsing H&M product: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping H&M: {e}")

    def scrape_zara(self, category):
        """Scrape fashion items from Zara"""
        base_url = f"https://www.zara.com/us/en/search?searchTerm={category}"
        try:
            response = requests.get(base_url, headers=self.headers, timeout=SCRAPING_SETTINGS['timeout'])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find product items
            products = soup.find_all('li', {'class': 'product-grid-product'})
            
            for product in products[:10]:  # Get top 10 items
                try:
                    # Extract product details
                    title = product.find('a', {'class': 'product-link'}).text.strip()
                    img = product.find('img')
                    img_url = img.get('src') or img.get('data-src')
                    if img_url:
                        img_url = urljoin('https://www.zara.com', img_url)
                    
                    # Extract price
                    price = product.find('span', {'class': 'price'})
                    price = price.text.strip() if price else 'N/A'
                    
                    self.data.append({
                        'source': 'Zara',
                        'title': title,
                        'image_url': img_url,
                        'price': price,
                        'brand': 'Zara',
                        'category': category,
                        'scraped_date': datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Error parsing Zara product: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping Zara: {e}")

    def scrape_all_sources(self, category):
        """Scrape fashion items from all sources"""
        self.data = []  # Reset data
        
        # Scrape from each source
        self.scrape_asos(category)
        time.sleep(SCRAPING_SETTINGS['delay'])  # Delay between sources
        
        self.scrape_hm(category)
        time.sleep(SCRAPING_SETTINGS['delay'])
        
        self.scrape_zara(category)
        
        # Sort by source and limit to top 10
        self.data.sort(key=lambda x: x['source'])
        return self.data[:10]

    def save_to_json(self, filename=FILE_PATHS['fashion_data']):
        """Save the scraped data to a JSON file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print(f"Fashion data saved to {filename}")

    def download_images(self, folder=FILE_PATHS['images_folder']):
        """Download all images from scraped items"""
        if not self.data:
            print("No data to download images from")
            return
            
        os.makedirs(folder, exist_ok=True)
            
        for item in self.data:
            if item['image_url']:
                try:
                    response = requests.get(item['image_url'], timeout=SCRAPING_SETTINGS['timeout'])
                    if response.status_code == 200:
                        # Create filename with source and category
                        filename = f"{folder}/{item['source']}_{item['category']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded image: {filename}")
                except Exception as e:
                    print(f"Error downloading image for {item['title']}: {e}")

# Example usage
if __name__ == "__main__":
    scraper = FashionScraper()
    
    # Scrape tops
    print("Scraping tops...")
    tops_data = scraper.scrape_all_sources('tops')
    
    # Scrape bottoms
    print("Scraping bottoms...")
    bottoms_data = scraper.scrape_all_sources('bottoms')
    
    # Save all data
    scraper.save_to_json()
    
    # Download images
    scraper.download_images() 