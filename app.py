from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS   # ✅ add this

app = Flask(__name__)
CORS(app)  # ✅ enable CORS for all routes

@app.route("/search")
def search():
    query = request.args.get("query")
    url = f"https://www.flipkart.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    product_cards = soup.select("div._1AtVbE")[:15]

    products = []
    for card in product_cards:
        name = card.select_one("div._4rR01T")
        price = card.select_one("div._30jeq3")
        link = card.select_one("a")
        if name and price and link:
            products.append({
                "name": name.text.strip(),
                "price": price.text.strip(),
                "link": "https://www.flipkart.com" + link["href"]
            })

    products = products[:5]  # only top 5
    return jsonify({"products": products})

if __name__ == "__main__":
    app.run(debug=True)
