import logging
import asyncio
from typing import List, Dict
import httpx
from app.utils.cache import PoolCache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HEADERS = {"accept": "application/json"}
TIMEOUT = httpx.Timeout(10.0)  # Set a max timeout for external API calls


class YieldAggregator:
    def __init__(self):
        self.pool_cache = PoolCache()

    async def _fetch_llama_yields(self, token: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                response = await client.get("https://yields.llama.fi/pools", headers=HEADERS)
                response.raise_for_status()
                data = response.json().get("data", [])
        except Exception as e:
            logger.warning(f"Llama API fetch failed: {e}")
            return []

        token_upper = token.upper()
        return [
            {
                "token": token_upper,
                "project": pool.get("project"),
                "chain": pool.get("chain"),
                "apy": pool.get("apy"),
                "tvlUsd": pool.get("tvlUsd", 0),
                "url": pool.get("url")
            }
            for pool in data
            if pool.get("symbol", "").upper() == token_upper
        ]

    async def _fetch_beefy_yields(self, token: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                response = await client.get("https://api.beefy.finance/vaults")
                response.raise_for_status()
                data = response.json()
        except Exception as e:
            logger.warning(f"Beefy API fetch failed: {e}")
            return []

        token_upper = token.upper()
        return [
            {
                "token": token_upper,
                "project": "Beefy",
                "chain": vault.get("chain", ""),
                "apy": vault.get("apy", 0),
                "tvlUsd": vault.get("tvl", 0),
                "url": f"https://app.beefy.finance/vault/{vault.get('id')}"
            }
            for vault in data
            if vault.get("symbol", "").upper() == token_upper and vault.get("apy", 0) > 0
        ]

    async def get_yields_info(self, token: str) -> Dict:
        token_upper = token.upper()
        cached = self.pool_cache.get_pool(token_upper)
        if cached:
            logger.debug(f"Using cached yield info for {token_upper}")
            return {"results": cached, "error": None}

        try:
            llama, beefy = await asyncio.gather(
                self._fetch_llama_yields(token_upper),
                self._fetch_beefy_yields(token_upper),
                return_exceptions=True
            )

            combined = []
            for result in [llama, beefy]:
                if isinstance(result, list):
                    combined.extend(result)
                else:
                    logger.warning(f"Yield source returned an error: {result}")

            if combined:
                self.pool_cache.set_pool(token_upper, combined)

            return {"results": combined, "error": None}
        except Exception as e:
            logger.exception(f"Unexpected error in get_yields_info for {token_upper}")
            return {"results": [], "error": str(e)}

    async def fetch_live_yields(self, tokens: List[str]) -> Dict:
        logger.debug(f"Fetching live yields for tokens: {tokens}")
        results = []
        try:
            for token in tokens:
                token_data = await self.get_yields_info(token)
                if token_data["error"]:
                    return {"results": [], "error": token_data["error"]}
                results.extend(token_data["results"])
            return {"results": results, "error": None}
        except Exception as e:
            logger.exception("Error in fetch_live_yields")
            return {"results": [], "error": str(e)}

    async def fetch_top_yields(self, tokens: List[str]) -> Dict:
        logger.debug(f"Fetching top yields for: {tokens}")
        try:
            all_results = []
            for token in tokens:
                info = await self.get_yields_info(token)
                if info.get("error"):
                    return {"yields": [], "error": info["error"]}
                all_results.extend(info["results"])

            top_yields = sorted(all_results, key=lambda x: x.get("apy", 0), reverse=True)[:3]
            return {"yields": top_yields, "error": None}
        except Exception as e:
            logger.exception("Error in fetch_top_yields")
            return {"yields": [], "error": str(e)}
