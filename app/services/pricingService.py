from typing import List, Dict, Union, Optional
from app.utils.market_data import MarketData
import logging

# Initialize the MarketData service
m_data = MarketData()

async def get_token_price(symbol: str) -> Optional[float]:
    """
    Fetch the current USD price for a single token symbol.
    
    Args:
        symbol (str): Token symbol (e.g., "ETH")
    
    Returns:
        Optional[float]: Price in USD or None if not found.
    """
    try:
        price = await m_data.fetch_token_data(symbol)
        if price is None:
            raise ValueError(f"Price for {symbol} not found.")
        return price
    except Exception as e:
        logging.exception(f"Error fetching price for {symbol}: {str(e)}")
        return None

async def get_token_prices(symbols: List[str]) -> Dict[str, Union[float, str]]:
    """
    Fetch the current USD prices for multiple token symbols.

    Args:
        symbols (List[str]): List of token symbols (e.g., ["ETH", "USDC"])
    
    Returns:
        Dict[str, Union[float, str]]: Mapping of symbols to prices or error messages.
    """
    try:
        return await m_data.fetch_multiple_token_data(symbols)
    except Exception as e:
        logging.exception("Error fetching multiple token prices")
        return {symbol: "Error fetching price" for symbol in symbols}

async def get_price_history(symbol: str, days: int) -> Union[Dict, str]:
    """
    Fetch historical price data for a token using Coinranking.

    Args:
        symbol (str): Token symbol (e.g., "ETH")
        days (int): Number of days to retrieve (valid: 1, 7, 30, 90, 365, etc.)
    
    Returns:
        Union[Dict, str]: Historical price data or error message.
    """
    try:
        return await m_data.fetch_price_history(symbol, days)
    except Exception as e:
        logging.exception(f"Failed to fetch price history for {symbol}")
        return f"Error fetching price history: {str(e)}"
