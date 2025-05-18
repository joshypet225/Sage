from fastapi import APIRouter, HTTPException, Body, logger
from app.services.yieldsService import get_top_yields
from typing import List
from app.services.yieldsService import fetch_yield_info

router = APIRouter(prefix="/defi", tags=["DeFi"])

@router.get("/yields/top-yields")
async def get_top_yields_endpoint(tokens: List[str] = Body(..., example=["ETH", "DAI", "USDC"])):
    """
    Fetch top 3 yield opportunities for each specified token.
    """
    logger.info(f"Fetching top yields for tokens: {tokens}")
    if not tokens or not isinstance(tokens, list):
        raise HTTPException(status_code=400, detail="`tokens` must be a list of token symbols.")
    
    result = await get_top_yields(tokens)
    logger.debug(f"Top yields for tokens {tokens}: {result}")
    return {"yields": result}

@router.get("/yields/{token}/info")
async def get_yield_info(token: str):
    """
    Fetch yield info for a specific token.
    """
    logger.info(f"Fetching yield info for token: {token}")
    if not token:
        raise HTTPException(status_code=400, detail="`token` must be a non-empty string.")
    
    result = await fetch_yield_info(token)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    logger.debug(f"Yield info for {token}: {result}")
    return {"yield_info": result}