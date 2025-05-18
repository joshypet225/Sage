class PoolCache:
    def __init__(self):
        self.cache = {}

    def get_pool(self, symbol: str):
        """
        Get a pool's metadata from the cache.

        Args:
            symbol (str): The symbol of the pool (e.g., "ETH", "USDC").

        Returns:
            dict: Pool metadata or None if not cached.
        """
        return self.cache.get(symbol.upper())

    def set_pool(self, symbol: str, data: dict):
        """
        Cache a pool's metadata.

        Args:
            symbol (str): The symbol of the pool (e.g., "ETH", "USDC").
            data (dict): The metadata to cache.
        """
        self.cache[symbol.upper()] = data

    def clear_cache(self):
        """Clear the entire cache."""
        self.cache.clear()

    def is_cached(self, symbol: str) -> bool:
        """Check if a pool's metadata is cached."""
        return symbol.upper() in self.cache
