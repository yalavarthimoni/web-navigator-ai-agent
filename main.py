# backend/main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json, re
from typing import List
from .flipkart_scraper import scrape_flipkart
from .llm_interface import generate_response, USE_GPT4ALL

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/top5")
async def top5(query: str = Query(...)):
    # scrape first 30 results
    all_products = scrape_flipkart(query, max_cards=30)

    if not all_products:
        return []

    # --- If LLM available ---
    if USE_GPT4ALL:
        small_list = [
            {
                "name": p["name"],
                "price_int": p["price_int"],
                "rating": p["rating"]
            }
            for p in all_products
        ]
        prompt = (
            f"You are given a JSON list of products. Each has name, price_int, rating.\n"
            f"User asked: '{query}'.\n"
            "Pick the best 5 products that satisfy the request (respect budget if mentioned, prefer high rating). "
            "Return only JSON array of 5 indices (0-based).\n\n"
            f"Products:\n{json.dumps(small_list, ensure_ascii=False)}"
        )
        try:
            llm_out = generate_response(prompt, max_tokens=300)
            match = re.search(r"\[.*\]", llm_out, re.S)
            indices = json.loads(match.group(0)) if match else []
            chosen = []
            for i in indices:
                if 0 <= i < len(all_products) and len(chosen) < 5:
                    chosen.append(all_products[i])
            if chosen:
                return chosen
        except Exception as e:
            print("LLM failed:", e)

    # --- Fallback (if no LLM or failure) ---
    budget = None
    m = re.search(r"under\s*([0-9]+)k", query.lower())
    if m:
        budget = int(m.group(1)) * 1000
    if budget:
        candidates = [p for p in all_products if p["price_int"] and p["price_int"] <= budget]
        if not candidates:
            candidates = all_products
    else:
        candidates = all_products

    # sort by rating desc, then price asc
    candidates = sorted(candidates, key=lambda p: (-p["rating"], p["price_int"] or 10**9))
    return candidates[:5]
