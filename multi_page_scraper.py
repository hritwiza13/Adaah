import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.parse import urljoin
import re

class PinterestScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.data = []

    def get_page(self, url):
        """Get the HTML content of a page"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_page(self, html):
        """Parse the HTML content and extract data"""
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        # Find all pin containers
        pin_containers = soup.find_all('div', {'data-test-pin-id': True})
        
        for pin in pin_containers:
            try:
                # Get pin ID
                pin_id = pin.get('data-test-pin-id')
                
                # Get image URL
                img = pin.find('img')
                if img:
                    img_url = img.get('src')
                    if not img_url:
                        img_url = img.get('data-src')
                else:
                    img_url = None
                
                # Get pin title/description
                title_elem = pin.find('div', {'data-test-id': 'pinTitle'})
                title = title_elem.text.strip() if title_elem else ''
                
                # Get pin link
                link_elem = pin.find('a', {'data-test-id': 'pin-closeup'})
                link = urljoin(self.base_url, link_elem['href']) if link_elem else None
                
                # Get pin creator
                creator_elem = pin.find('div', {'data-test-id': 'pin-creator'})
                creator = creator_elem.text.strip() if creator_elem else ''
                
                items.append({
                    'pin_id': pin_id,
                    'title': title,
                    'image_url': img_url,
                    'link': link,
                    'creator': creator
                })
            except (AttributeError, KeyError) as e:
                print(f"Error parsing pin: {e}")
                continue
        
        return items

    def get_next_page(self, html):
        """Find the URL of the next page"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for the next page button
        next_button = soup.find('button', {'data-test-id': 'pagination-next-button'})
        if next_button and not next_button.get('disabled'):
            # Extract the next page URL from the data attribute
            next_url = next_button.get('data-test-id-next-page')
            if next_url:
                return urljoin(self.base_url, next_url)
        
        return None

    def scrape(self, max_pages=5):
        """Scrape multiple pages"""
        current_url = self.base_url
        page_count = 0

        while current_url and page_count < max_pages:
            print(f"Scraping page {page_count + 1}: {current_url}")
            
            # Get the page content
            html = self.get_page(current_url)
            if not html:
                break

            # Parse the page
            items = self.parse_page(html)
            self.data.extend(items)
            print(f"Found {len(items)} pins on this page")

            # Find the next page
            current_url = self.get_next_page(html)
            
            # Be nice to the server
            time.sleep(3)  # Increased delay for Pinterest
            page_count += 1

        return self.data

    def save_to_json(self, filename='pinterest_data.json'):
        """Save the scraped data to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    # Replace this URL with the Pinterest board or search URL you want to scrape
    target_url = "https://www.pinterest.com/search/pins/?q=fashion"  # Example: fashion pins
    
    scraper = PinterestScraper(target_url)
    data = scraper.scrape(max_pages=3)  # Scrape 3 pages
    scraper.save_to_json()
    
    print(f"Scraped {len(data)} pins in total") 