# backend/flipkart_scraper.py
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def parse_price(price_str):
    digits = re.sub(r"[^\d]", "", price_str or "")
    return int(digits) if digits else None

def scrape_flipkart(query: str, max_cards=30):
    q = query.replace(" ", "+")
    url = f"https://www.flipkart.com/search?q={q}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    products = []
    cards = soup.select("div._1AtVbE")
    for card in cards:
        if len(products) >= max_cards:
            break
        name_tag = card.select_one("div._4rR01T") or card.select_one("a.s1Q9rs")
        price_tag = card.select_one("div._30jeq3")
        rating_tag = card.select_one("div._3LWZlK")
        link_tag = card.select_one("a._1fQZEK") or card.select_one("a.s1Q9rs")
        img_tag = card.select_one("img")

        if name_tag and price_tag and link_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            price_int = parse_price(price)
            rating = 0.0
            try:
                rating = float(rating_tag.get_text(strip=True)) if rating_tag else 0.0
            except:
                pass
            href = link_tag.get("href")
            full_url = "https://www.flipkart.com" + href if href and href.startswith("/") else href
            img = img_tag.get("src") if img_tag else None

            products.append({
                "name": name,
                "price": price,
                "price_int": price_int,
                "rating": rating,
                "url": full_url,
                "img": img
            })
    return products
