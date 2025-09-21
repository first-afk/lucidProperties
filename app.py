from flask import Flask, render_template
import json

app = Flask(__name__)

def load_listings():
    """Loads and sorts listings from the JSON file."""
    try:
        with open('listings.json', 'r') as f:
            listings = json.load(f)
        # Sort listings by the 'price' key, from lowest to highest
        sorted_listings = sorted(listings, key=lambda x: x.get('price', 0))
        return sorted_listings
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    listings = load_listings()
    return render_template('index.html', listings=listings)

if __name__ == '__main__':
    app.run(debug=True)