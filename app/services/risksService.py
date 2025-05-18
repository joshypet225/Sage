import logging
from typing import List, Dict, Union
from app.services import yieldsService
from app.utils import cache
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

async def analyze_risks(pools: List[Dict]) -> Dict[str, Union[str, List[Dict]]]:
    """
    Analyze a list of yield pools and detect potential risks.

    Args:
        pools (List[Dict]): List of pool dictionaries.

    Returns:
        Dict[str, Union[str, List[Dict]]]: Risk analysis result.
    """
    logger.debug(f"Analyzing risks for {len(pools)} pool(s).")

    if not pools or not isinstance(pools, list):
        return {"results": [], "error": "Invalid input: expected a list of pool dictionaries."}

    full_pools = []
    for pool in pools:
        symbol = pool.get("symbol")
        if not symbol:
            continue

        cached_pool = cache.pool_cache.get_pool(symbol)
        if cached_pool:
            full_pools.append(cached_pool[0])  # Take first cached entry
        else:
            result = await yieldsService.fetch_yield_info(symbol)
            if result.get("results"):
                full_pools.append(result["results"][0])

    if not full_pools:
        return {"results": [], "error": "No valid pool data found."}

    # Run risk analysis
    return yieldsService.detect_risks(full_pools)
