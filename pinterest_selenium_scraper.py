from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import requests
from urllib.parse import urljoin
import re
from datetime import datetime
from config import PINTEREST_URLS, SCRAPING_SETTINGS, FILE_PATHS

class FashionPinterestScraper:
    def __init__(self, base_url, headless=SCRAPING_SETTINGS['headless']):
        self.base_url = base_url
        self.data = []
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Initialize the driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, SCRAPING_SETTINGS['timeout'])
        
        # Gender-specific fashion categories
        self.fashion_categories = {
            'women': {
                'tops': ['blouse', 't-shirt', 'shirt', 'sweater', 'tank top', 'crop top', 'tunic', 'cardigan', 'sweatshirt'],
                'bottoms': ['jeans', 'pants', 'skirt', 'shorts', 'leggings', 'joggers', 'palazzo', 'culottes'],
                'dresses': ['dress', 'gown', 'jumpsuit', 'romper', 'maxi', 'mini', 'midi', 'cocktail'],
                'outerwear': ['jacket', 'coat', 'blazer', 'vest', 'poncho', 'cape', 'parka'],
                'accessories': ['bag', 'jewelry', 'watch', 'scarf', 'hat', 'belt', 'sunglasses', 'gloves', 'tie', 'socks'],
                'footwear': ['shoes', 'boots', 'sneakers', 'sandals', 'heels', 'flats', 'loafers', 'mules', 'espadrilles'],
                'underwear': ['bra', 'panties', 'lingerie', 'shapewear', 'sleepwear'],
                'swimwear': ['bikini', 'one-piece', 'swimsuit', 'cover-up', 'beachwear']
            },
            'men': {
                'tops': ['shirt', 't-shirt', 'polo', 'sweater', 'hoodie', 'sweatshirt', 'vest', 'tank top'],
                'bottoms': ['jeans', 'pants', 'shorts', 'chinos', 'khakis', 'joggers', 'sweatpants'],
                'suits': ['suit', 'blazer', 'tuxedo', 'formal wear', 'business attire'],
                'outerwear': ['jacket', 'coat', 'blazer', 'vest', 'parka', 'windbreaker'],
                'accessories': ['tie', 'belt', 'watch', 'sunglasses', 'hat', 'gloves', 'scarf', 'socks'],
                'footwear': ['shoes', 'boots', 'sneakers', 'sandals', 'loafers', 'oxfords', 'derby', 'chelsea boots'],
                'underwear': ['boxers', 'briefs', 'undershirt', 'sleepwear'],
                'swimwear': ['swim trunks', 'board shorts', 'swim briefs', 'rash guard']
            }
        }
        
        # Gender-specific styles
        self.gender_styles = {
            'women': ['feminine', 'girly', 'elegant', 'romantic', 'bohemian', 'vintage', 'preppy', 'athletic'],
            'men': ['masculine', 'rugged', 'preppy', 'athletic', 'business', 'casual', 'streetwear', 'vintage']
        }
        
        # Size and fit patterns
        self.size_patterns = {
            'numeric': r'\b(?:XXS|XS|S|M|L|XL|XXL|XXXL)\b',
            'numeric_us': r'\b(?:0|2|4|6|8|10|12|14|16|18|20|22|24|26|28|30)\b',
            'alpha': r'\b(?:A|B|C|D|DD|E|F|G)\b',
            'shoe': r'\b(?:5|6|7|8|9|10|11|12|13)\b',
            'waist': r'\b(?:28|30|32|34|36|38|40|42|44)\b',
            'inseam': r'\b(?:28|30|32|34|36)\b'
        }
        
        self.fit_patterns = {
            'slim': ['slim', 'fitted', 'skinny', 'tapered', 'narrow'],
            'regular': ['regular', 'standard', 'classic', 'straight'],
            'relaxed': ['relaxed', 'loose', 'oversized', 'baggy', 'wide'],
            'petite': ['petite', 'short', 'small frame'],
            'tall': ['tall', 'long', 'extended length'],
            'plus': ['plus', 'curvy', 'full figured']
        }

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page to load more content"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 10
        
        while scroll_attempts < max_attempts:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(2)
            
            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Break if no more content
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                
            last_height = new_height

    def extract_size_and_fit(self, text):
        """Extract size and fit information from text"""
        size_info = {
            'size': None,
            'size_type': None,
            'measurements': {
                'waist': None,
                'inseam': None,
                'bust': None,
                'hip': None
            }
        }
        
        fit_info = {
            'fit': None,
            'fit_details': []
        }
        
        # Extract size information
        for size_type, pattern in self.size_patterns.items():
            matches = re.findall(pattern, text.upper())
            if matches:
                size_info['size'] = matches[0]
                size_info['size_type'] = size_type
                break
        
        # Extract measurements
        measurement_patterns = {
            'waist': r'waist[:\s]*(\d{2,3})',
            'inseam': r'inseam[:\s]*(\d{2,3})',
            'bust': r'bust[:\s]*(\d{2,3})',
            'hip': r'hip[:\s]*(\d{2,3})'
        }
        
        for measurement, pattern in measurement_patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                size_info['measurements'][measurement] = match.group(1)
        
        # Extract fit information
        for fit_type, keywords in self.fit_patterns.items():
            if any(keyword in text.lower() for keyword in keywords):
                fit_info['fit'] = fit_type
                fit_info['fit_details'].extend(
                    [keyword for keyword in keywords if keyword in text.lower()]
                )
        
        return {
            'size': size_info,
            'fit': fit_info
        }

    def detect_gender(self, text):
        """Detect gender from text"""
        gender_keywords = {
            'women': ['women', 'woman', 'female', 'ladies', 'girls', 'feminine', 'she', 'her'],
            'men': ['men', 'man', 'male', 'gentlemen', 'boys', 'masculine', 'he', 'his']
        }
        
        text = text.lower()
        gender_scores = {'women': 0, 'men': 0}
        
        for gender, keywords in gender_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    gender_scores[gender] += 1
        
        # Return the gender with the highest score, or None if no clear gender
        max_score = max(gender_scores.values())
        if max_score > 0:
            return max(gender_scores.items(), key=lambda x: x[1])[0]
        return None

    def extract_fashion_details(self, title, description):
        """Extract fashion-specific details from text"""
        details = {
            'gender': None,
            'category': None,
            'subcategory': None,
            'colors': [],
            'season': None,
            'style': None,
            'occasion': None,
            'material': None,
            'size_and_fit': None
        }
        
        # Combine title and description for analysis
        text = f"{title} {description}".lower()
        
        # Detect gender
        details['gender'] = self.detect_gender(text)
        
        # Detect category based on gender
        if details['gender']:
            for category, items in self.fashion_categories[details['gender']].items():
                for item in items:
                    if item in text:
                        details['category'] = category
                        details['subcategory'] = item
                        break
                if details['category']:
                    break
        
        # Detect colors
        colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'brown', 'gray', 'beige', 'navy', 'burgundy']
        for color in colors:
            if color in text:
                details['colors'].append(color)
        
        # Detect season
        seasons = {
            'summer': ['summer', 'hot', 'beach', 'swim', 'vacation'],
            'winter': ['winter', 'cold', 'snow', 'warm', 'cozy'],
            'spring': ['spring', 'floral', 'light', 'fresh'],
            'fall': ['fall', 'autumn', 'cozy', 'layered']
        }
        for season, keywords in seasons.items():
            if any(keyword in text for keyword in keywords):
                details['season'] = season
        
        # Detect style based on gender
        if details['gender']:
            for style in self.gender_styles[details['gender']]:
                if style in text:
                    details['style'] = style
                    break
                
        # Detect occasion
        occasions = {
            'work': ['work', 'office', 'business', 'professional'],
            'party': ['party', 'evening', 'night', 'celebration'],
            'wedding': ['wedding', 'bridal', 'formal'],
            'sports': ['sports', 'athletic', 'gym', 'workout'],
            'beach': ['beach', 'swim', 'vacation']
        }
        for occasion, keywords in occasions.items():
            if any(keyword in text for keyword in keywords):
                details['occasion'] = occasion
                
        # Detect material
        materials = ['cotton', 'silk', 'wool', 'leather', 'denim', 'linen', 'suede', 'velvet', 'lace', 'knit']
        for material in materials:
            if material in text:
                details['material'] = material
        
        # Extract size and fit information
        details['size_and_fit'] = self.extract_size_and_fit(text)
        
        return details

    def parse_pins(self):
        """Parse pins from the current page with fashion-specific details"""
        items = []
        
        try:
            # Wait for pins to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="pin"]')))
            
            # Find all pins
            pins = self.driver.find_elements(By.CSS_SELECTOR, '[data-test-id="pin"]')
            
            for pin in pins:
                try:
                    # Get pin ID
                    pin_id = pin.get_attribute('data-test-pin-id')
                    if not pin_id:
                        continue
                    
                    # Get image URL
                    try:
                        img = pin.find_element(By.TAG_NAME, 'img')
                        img_url = img.get_attribute('src') or img.get_attribute('data-src')
                        if not img_url:
                            continue
                    except NoSuchElementException:
                        continue
                    
                    # Get title/description
                    try:
                        title = pin.find_element(By.CSS_SELECTOR, '[data-test-id="pinTitle"]').text
                    except NoSuchElementException:
                        title = ''
                    
                    # Get description
                    try:
                        description = pin.find_element(By.CSS_SELECTOR, '[data-test-id="pinDescription"]').text
                    except NoSuchElementException:
                        description = ''
                    
                    # Get pin link
                    try:
                        link = pin.find_element(By.CSS_SELECTOR, '[data-test-id="pin-closeup"]').get_attribute('href')
                    except NoSuchElementException:
                        link = None
                    
                    # Get creator
                    try:
                        creator = pin.find_element(By.CSS_SELECTOR, '[data-test-id="pin-creator"]').text
                    except NoSuchElementException:
                        creator = ''
                    
                    # Extract fashion details
                    fashion_details = self.extract_fashion_details(title, description)
                    
                    # Get engagement metrics
                    try:
                        saves = pin.find_element(By.CSS_SELECTOR, '[data-test-id="pin-saves"]').text
                        saves = int(re.sub(r'[^0-9]', '', saves)) if saves else 0
                    except (NoSuchElementException, ValueError):
                        saves = 0
                    
                    items.append({
                        'pin_id': pin_id,
                        'title': title,
                        'description': description,
                        'image_url': img_url,
                        'link': link,
                        'creator': creator,
                        'fashion_details': fashion_details,
                        'engagement': {
                            'saves': saves,
                            'scraped_date': datetime.now().isoformat()
                        }
                    })
                    
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    print(f"Error parsing pin: {e}")
                    continue
                    
        except TimeoutException:
            print("Timeout waiting for pins to load")
            
        return items

    def scrape(self, max_pages=SCRAPING_SETTINGS['max_pages'], scroll_pages=SCRAPING_SETTINGS['scroll_pages']):
        """Scrape multiple pages of Pinterest"""
        try:
            # Load the initial page
            self.driver.get(self.base_url)
            time.sleep(SCRAPING_SETTINGS['delay'])  # Wait for initial load
            
            page_count = 0
            while page_count < max_pages:
                print(f"Scraping page {page_count + 1}")
                
                # Scroll to load more content
                for _ in range(scroll_pages):
                    self.scroll_to_bottom()
                    time.sleep(SCRAPING_SETTINGS['delay'])
                
                # Parse pins from current page
                items = self.parse_pins()
                self.data.extend(items)
                print(f"Found {len(items)} fashion items on this page")
                
                # Try to click next page button
                try:
                    next_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-id="pagination-next-button"]'))
                    )
                    if not next_button.get_attribute('disabled'):
                        next_button.click()
                        time.sleep(SCRAPING_SETTINGS['delay'])  # Wait for new page to load
                        page_count += 1
                    else:
                        print("No more pages available")
                        break
                except TimeoutException:
                    print("No next page button found")
                    break
                
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            self.driver.quit()
            
        return self.data

    def save_to_json(self, filename=FILE_PATHS['fashion_data']):
        """Save the scraped data to a JSON file"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print(f"Fashion data saved to {filename}")

    def download_images(self, folder=FILE_PATHS['images_folder']):
        """Download all images from scraped pins"""
        if not self.data:
            print("No data to download images from")
            return
            
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
            
        # Download each image
        for item in self.data:
            if item['image_url']:
                try:
                    # Get image data
                    response = requests.get(item['image_url'], timeout=SCRAPING_SETTINGS['timeout'])
                    if response.status_code == 200:
                        # Create filename with category and ID
                        category = item['fashion_details']['category'] or 'uncategorized'
                        filename = f"{folder}/{category}_{item['pin_id']}.jpg"
                        # Save image
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                        print(f"Downloaded image: {filename}")
                except Exception as e:
                    print(f"Error downloading image for pin {item['pin_id']}: {e}")

    def analyze_trends(self):
        """Analyze fashion trends from scraped data"""
        trends = {
            'gender_distribution': {'women': 0, 'men': 0},
            'categories': {},
            'colors': {},
            'styles': {},
            'seasons': {},
            'occasions': {},
            'materials': {},
            'sizes': {},
            'fits': {}
        }
        
        for item in self.data:
            details = item['fashion_details']
            
            # Count gender distribution
            if details['gender']:
                trends['gender_distribution'][details['gender']] += 1
            
            # Count categories
            if details['category']:
                category_key = f"{details['gender']}_{details['category']}" if details['gender'] else details['category']
                trends['categories'][category_key] = trends['categories'].get(category_key, 0) + 1
            
            # Count colors
            for color in details['colors']:
                trends['colors'][color] = trends['colors'].get(color, 0) + 1
            
            # Count styles
            if details['style']:
                trends['styles'][details['style']] = trends['styles'].get(details['style'], 0) + 1
            
            # Count seasons
            if details['season']:
                trends['seasons'][details['season']] = trends['seasons'].get(details['season'], 0) + 1
                
            # Count occasions
            if details['occasion']:
                trends['occasions'][details['occasion']] = trends['occasions'].get(details['occasion'], 0) + 1
                
            # Count materials
            if details['material']:
                trends['materials'][details['material']] = trends['materials'].get(details['material'], 0) + 1
            
            # Count sizes
            if details['size_and_fit']['size']['size']:
                size_key = f"{details['size_and_fit']['size']['size_type']}_{details['size_and_fit']['size']['size']}"
                trends['sizes'][size_key] = trends['sizes'].get(size_key, 0) + 1
            
            # Count fits
            if details['size_and_fit']['fit']['fit']:
                trends['fits'][details['size_and_fit']['fit']['fit']] = trends['fits'].get(details['size_and_fit']['fit']['fit'], 0) + 1
        
        return trends

# Example usage
if __name__ == "__main__":
    # Choose your target URL from the configuration
    target_url = PINTEREST_URLS['women']['trends']  # Change this to any URL from PINTEREST_URLS
    
    # Create scraper with custom settings
    scraper = FashionPinterestScraper(
        target_url,
        headless=SCRAPING_SETTINGS['headless']
    )

    # Scrape with settings from config
    data = scraper.scrape(
        max_pages=SCRAPING_SETTINGS['max_pages'],
        scroll_pages=SCRAPING_SETTINGS['scroll_pages']
    )

    # Save data with configured filename
    scraper.save_to_json()

    # Download images to configured folder
    scraper.download_images()
    
    # Analyze trends
    trends = scraper.analyze_trends()
    print("\nFashion Trends Analysis:")
    print(json.dumps(trends, indent=4))
    
    print(f"\nScraped {len(data)} fashion items in total") 