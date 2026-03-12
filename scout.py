import os, httpx

class MarketScout:
    def __init__(self):
        self.api_key = os.getenv("MARKET_API_KEY")
        self.base_url = "https://api.freecurrencyapi.com/v1/latest"

    async def get_live_rate(self, base="USD", target="ZAR"):
        """Fetches real-time market data. No simulation."""
        if not self.api_key:
            return None, "API_KEY_MISSING"
        
        try:
            params = {"apikey": self.api_key, "base_currency": base, "currencies": target}
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                data = response.json()
                rate = data['data'][target]
                return rate, "SUCCESS"
        except Exception as e:
            return None, str(e)
