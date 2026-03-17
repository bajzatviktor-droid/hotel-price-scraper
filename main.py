from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/get_price', methods=['GET'])
def get_price():
    hotel_name = request.args.get('hotel')
    # A Directbooking kereső URL-je
    search_url = f"https://www.directbooking.ro/cauta.aspx?ss={hotel_name}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ez a rész próbálja megkeresni az első találat árát
        # Figyelem: az oldalak szerkezete változhat!
        price_tag = soup.find("span", {"class": "price-val"}) 
        if price_tag:
            return jsonify({"source": "DirectBooking", "price": price_tag.text.strip(), "currency": "EUR"})
        else:
            return jsonify({"error": "Nem találtam árat a listában"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # A Rendernek szüksége van a port beállításra
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
