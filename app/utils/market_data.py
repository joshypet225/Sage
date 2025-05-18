import httpx
import os
import logging
from typing import Optional, Dict, List, Union


class MarketData:
    def __init__(self):
        self.coinlib_url = os.getenv("COINLIB_URL")
        self.coinlib_key = os.getenv("COINLIB_API_KEY")
        self.coinranking_url = os.getenv("COINRANKING_URL")
        self.coinranking_key = os.getenv("COINRANKING_API_KEY")
        self.session = httpx.AsyncClient(timeout=30.0)
        self.coinranking_headers = {"x-access-token": self.coinranking_key}

    async def fetch_token_data(self, symbol: str) -> Optional[float]:
        """
        Try fetching from Coinlib first. If it fails, fallback to Coinranking.
        """
        price = await self._fetch_from_coinlib(symbol)
        if price is not None:
            return price
        return await self._fetch_from_coinranking(symbol)

    async def _fetch_from_coinlib(self, symbol: str) -> Optional[float]:
        try:
            url = f"{self.coinlib_url}/coin?key={self.coinlib_key}&symbol={symbol.upper()}"
            response = await self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return float(data["price_usd"])
        except Exception as e:
            logging.warning(f"[Coinlib] Failed for {symbol}: {str(e)}")
            return None

    async def _fetch_from_coinranking(self, symbol: str) -> Optional[float]:
        try:
            url = f"{self.coinranking_url}/coins"
            response = await self.session.get(url, headers=self.coinranking_headers, params={"search": symbol})
            response.raise_for_status()
            coins = response.json().get("data", {}).get("coins", [])
            for coin in coins:
                if coin["symbol"].upper() == symbol.upper():
                    return float(coin["price"])
            return None
        except Exception as e:
            logging.error(f"[Coinranking] Failed for {symbol}: {str(e)}")
            return None

    async def fetch_multiple_token_data(self, symbols: List[str]) -> Dict[str, Union[float, str]]:
        results: Dict[str, Union[float, str]] = {}
        for symbol in symbols:
            price = await self.fetch_token_data(symbol)
            results[symbol.upper()] = price if price is not None else "Price not found or error occurred"
        return results

    async def fetch_price_history(self, symbol: str, days: int = 7) -> Union[Dict, str]:
        """
        Only Coinranking supports historical prices, so use it directly.
        """
        try:
            url = f"{self.coinranking_url}/coins"
            response = await self.session.get(url, headers=self.coinranking_headers, params={"search": symbol})
            response.raise_for_status()
            coins = response.json().get("data", {}).get("coins", [])
            uuid = next((coin["uuid"] for coin in coins if coin["symbol"].upper() == symbol.upper()), None)
            if not uuid:
                return f"UUID for token {symbol} not found."

            history_url = f"{self.coinranking_url}/coin/{uuid}/history"
            params = {"timePeriod": f"{days}d"}
            history_response = await self.session.get(history_url, headers=self.coinranking_headers, params=params)
            history_response.raise_for_status()
            return history_response.json()
        except Exception as e:
            logging.exception(f"Error fetching price history for {symbol}")
            return {"error": str(e)}

    async def close(self):
        await self.session.aclose()
