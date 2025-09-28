# backend/browser_controller.py
from playwright.async_api import async_playwright

class BrowserController:
    def __init__(self):
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def scrape_flipkart_laptops(self, query: str):
        await self.page.goto("https://www.flipkart.com")
        await self.page.wait_for_timeout(2000)

        # Close login popup if exists
        try:
            await self.page.click("button._2KpZ6l._2doB4z", timeout=2000)
        except:
            pass

        await self.page.fill("input[name='q']", query)
        await self.page.press("input[name='q']", "Enter")
        await self.page.wait_for_timeout(3000)

        products = await self.page.query_selector_all("div._1AtVbE")
        data = []
        for prod in products:
            try:
                name_el = await prod.query_selector("div._4rR01T")
                price_el = await prod.query_selector("div._30jeq3")
                rating_el = await prod.query_selector("div._3LWZlK")
                if name_el and price_el:
                    name = await name_el.inner_text()
                    price = await price_el.inner_text().replace("₹","").replace(",","")
                    rating = float(await rating_el.inner_text()) if rating_el else 0
                    data.append({
                        "name": name,
                        "price": price,
                        "rating": rating
                    })
            except:
                continue
        return data

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()
