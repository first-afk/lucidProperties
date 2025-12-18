import requests
from bs4 import BeautifulSoup
import json
import re

# Schema Enums for validation/mapping
VALID_TITLES = [
    "Detached Duplex", "Semi Detached Duplex", "Terraced Duplexes",
    "Detached Bungalow", "Semi Detached Bungalow", "Terraced Bungalow",
    "Block of Flats"
]

def clean_price(price_text):
    """Extracts numeric price from string."""
    digits = re.findall(r'\d+', price_text)
    return int("".join(digits)) if digits else 0

def parse_features(text):
    """Extracts bed, bath, toilet, parking counts from text descriptions."""
    # Default values
    features = {'bedrooms': 0, 'bathrooms': 0, 'toilets': 0, 'parking_space': 0}
    
    text = text.lower()
    
    # Regex patterns for various features
    patterns = {
        'bedrooms': r'(\d+)\s*(?:bed|room)',
        'bathrooms': r'(\d+)\s*(?:bath)',
        'toilets': r'(\d+)\s*(?:toilet)',
        'parking_space': r'(\d+)\s*(?:car|park)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            features[key] = int(match.group(1))
            
    # Heuristic: If toilets not found, assume toilets = bathrooms + 1 (common in Nigeria)
    if features['toilets'] == 0 and features['bathrooms'] > 0:
        features['toilets'] = features['bathrooms'] + 1
        
    return features

def map_title(raw_title):
    """Maps raw listing titles to the Schema Enum."""
    raw_lower = raw_title.lower()
    
    if "semi detached duplex" in raw_lower: return "Semi Detached Duplex"
    if "terraced duplex" in raw_lower or "terrace" in raw_lower: return "Terraced Duplexes"
    if "detached duplex" in raw_lower: return "Detached Duplex"
    
    if "semi detached bungalow" in raw_lower: return "Semi Detached Bungalow"
    if "terraced bungalow" in raw_lower: return "Terraced Bungalow"
    if "detached bungalow" in raw_lower or "bungalow" in raw_lower: return "Detached Bungalow"
    
    if "flat" in raw_lower or "apartment" in raw_lower: return "Block of Flats"
    
    return "Detached Duplex" # Default fallback if ambiguous

def scrape_listings():
    url = "https://nigeriapropertycentre.com/for-rent/abuja"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Fetching listings...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    listings = []
    
    cards = soup.find_all('div', itemprop='itemListElement')

    for card in cards:
        try:
            # Extract Raw Elements
            title_el = card.find('h3', itemprop='name')
            price_el = card.find('span', class_='pull-sm-left')
            address_el = card.find('address')
            content_el = card.find('h4', class_='content-title')
            link_element = card.find('a', href=True)
            aux_links = card.find_all('ul', class_='aux-info')

            if title_el and price_el:
                raw_title = title_el.text.strip()
                price = clean_price(price_el.text)
                
                
                address = address_el.text.strip() if address_el else "Abuja"
                link = "https://nigeriapropertycentre.com" + link_element['href']
                
                # Parse Features (Try structured aux info first, then text fallback)
                features = {'bedrooms': 0, 'bathrooms': 0, 'toilets': 0, 'parking_space': 0}
                
                # Method A: Extract from icons/aux-info
                if aux_links:
                    aux_text = " ".join([li.text for li in aux_links])
                    features = parse_features(aux_text)
                
                # Method B: If missing, check content text
                if features['bedrooms'] == 0 and content_el:
                    features = parse_features(content_el.text)

                # Construct Object according to Schema
                listing = {
                    "title": map_title(raw_title),
                    "address": address,
                    "price": price,
                    "link": link,
                    "bedrooms": features['bedrooms'],
                    "bathrooms": features['bathrooms'],
                    "toilets": features['toilets'],
                    "parking_space": features['parking_space'],
                    "original_title": raw_title # Kept for display purposes
                }

                # Filter: Ensure price is within schema range
                if 5_000_000 <= listing['price'] <= 5_000_000_000:
                    listings.append(listing)
                    
        except Exception as e:
            continue

    with open('listings.json', 'w') as f:
        json.dump(listings, f, indent=4)
    
    print(f"Scraping complete. Saved {len(listings)} valid listings.")

if __name__ == "__main__":
    scrape_listings()