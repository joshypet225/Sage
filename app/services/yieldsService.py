from typing import List
from app.utils.yieldsAggregator import YieldAggregator

aggregator = YieldAggregator()

async def fetch_yield_info(token: str):
    return await aggregator.get_yields_info(token)

async def fetch_live_yields(tokens: List[str]):
    return await aggregator.fetch_live_yields(tokens)

async def get_top_yields(tokens: List[str]):
    return await aggregator.fetch_top_yields(tokens)
