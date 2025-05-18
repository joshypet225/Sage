from fastapi import APIRouter, HTTPException, logger
from app.services.pricingService import get_token_prices
from app.utils.logging import get_logger

router = APIRouter(prefix="/pricing", tags=["Pricing"])

@router.get("/token-prices")
async def get_prices(tokens: str = "ETH,DAI,USDC"):
    """
    Fetch real-time token prices, market caps, and 24hr stats from CoinGecko.
    
    Args:
        tokens (str): Comma-separated list of token symbols (e.g. ETH,DAI,USDC)

    Returns:
        dict: Price data or an error message.
    """
    logger.info(f"Fetching prices for tokens: {tokens}")
    symbol_list = [t.strip().upper() for t in tokens.split(",") if t.strip()]
    
    if not symbol_list:
        raise HTTPException(status_code=400, detail="No valid token symbols provided.")

    result = await get_token_prices(symbol_list)

    if "error" in result:
        return {"error": result["error"], "data": []}
    
    logger.debug(f"Fetched prices: {result}")
    return {"data": result, "error": None}
