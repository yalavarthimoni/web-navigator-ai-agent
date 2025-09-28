# backend/agent.py
from .browser_controller import BrowserController

class WebAgent:
    def __init__(self):
        self.browser = BrowserController()

    async def start(self):
        await self.browser.start()

    async def get_top5_laptops(self, instruction: str):
        all_laptops = await self.browser.scrape_flipkart_laptops(instruction)
        if not all_laptops:
            return []

        # Sort by rating desc, price asc
        sorted_laptops = sorted(all_laptops, key=lambda x: (-x["rating"], int(x["price"])))
        top5 = [l["name"] for l in sorted_laptops[:5]]
        return top5

    async def close(self):
        await self.browser.close()
