import requests
from bs4 import BeautifulSoup
import json
import re

# The URL for Abuja property listings
URL = "https://nigeriapropertycentre.com/for-rent/abuja"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Fetching listings...")
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

listings_data = []

# Find all property cards on the page
property_cards = soup.find_all('div', itemprop='itemListElement')

for card in property_cards:
    try:
        title_element = card.find('h3', itemprop='name')
        content_element = card.find('h4', class_='content-title')
        price_element = card.find('span', class_='pull-sm-left')
        address_element = card.find('address')
        link_element = card.find('a', href=True)

        # Clean and extract text content
        if all([title_element, content_element, price_element, address_element, link_element]):
            title = title_element.text.strip()
            content = content_element.text.strip()
            # Remove currency symbol and commas, then convert to integer
            price_text = price_element.text.strip()
            # Use regex to find all digits
            price_digits = re.findall(r'\d+', price_text)
            price = int("".join(price_digits)) if price_digits else 0
            
            address = address_element.text.strip()
            link = "https://nigeriapropertycentre.com" + link_element['href']

            # Add to our list if the price is valid
            if price > 0:
                listings_data.append({
                    'title': title,
                    'content': content,
                    'price': price,
                    'address': address,
                    'link': link
                })
    except Exception as e:
        print(f"Skipped a card due to an error: {e}")

# Save the data to a JSON file
with open('listings.json', 'w') as f:
    json.dump(listings_data, f, indent=4)

print(f"Scraping complete! Found {len(listings_data)} listings.")