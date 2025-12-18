# Abuja House Listing Scraper & Dashboard

A Python-based web application that scrapes real estate data from Nigerian property websites and visualizes it in a user-friendly dashboard. This project automates the collection of housing data in Abuja, presenting it in a clean, schema-compliant format sorted by price.

## 📌 Project Overview

This tool solves the problem of finding aggregated real estate data by combining web scraping with a local web server. It consists of two main components:
1.  **Backend Scraper:** A robust script that crawls property listing websites, extracts key features using Regular Expressions (price, bedrooms, bathrooms, toilets, parking), and standardizes the data according to a strict JSON schema.
2.  **Frontend Dashboard:** A Flask web application that renders the scraped data in a responsive, vibrant interface.

## 🚀 Features

* **Smart Parsing:** Uses Regex to extract amenity counts (beds, baths, toilets, parking) even from unstructured text descriptions.
* **Data Standardization:** Maps raw listing titles to a standardized set of property types (e.g., "Detached Duplex", "Block of Flats") to match ML-ready schemas.
* **Price Sorting:** Automatically arranges listings from lowest to highest price for easier budgeting.
* **Schema Compliance:** Ensures all data points (town, state, price range) adhere to a defined JSON structure.
* **Vibrant UI:** A custom-styled interface featuring a card-based layout with visual badges for property specs.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Web Framework:** Flask
* **Scraping:** Requests, BeautifulSoup4
* **Data Handling:** JSON, Regular Expressions (Regex)
* **Frontend:** HTML5, CSS3, Jinja2 Templating, FontAwesome

## 🔧 Installation & Usage
1. **Install Dependencies** <code>pip install requests beautifulsoup4 flask</code>
2. **Run the scraper**: This fetches the latest data and populates listings.json
   <code>python scraper.py</code>
3. **Start the web server** <code>python app.py</code>
 


