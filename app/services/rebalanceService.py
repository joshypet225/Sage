from app.services.pricingService import get_token_prices

async def suggest_rebalance_strategy(
    current_holdings: dict,
    target_allocation: dict
) -> dict:
    # Combine all symbols from current holdings and target allocation
    all_tokens = set(current_holdings) | set(target_allocation)
    prices = await get_token_prices(list(all_tokens))

    if "error" in prices:
        return {"error": prices["error"], "rebalance_plan": None}

    portfolio_value = 0.0
    current_usd_values = {}
    skipped = []

    # Calculate current portfolio value and individual token values
    for token, amount in current_holdings.items():
        token_price = prices.get(token.upper())  # Directly access token price by symbol
        if not token_price:
            skipped.append(token)
            continue
        usd_value = amount * token_price.get("usd", 0.0)
        current_usd_values[token.upper()] = usd_value
        portfolio_value += usd_value

    suggestions = {
        token.upper(): {
            "current_value_usd": round(current_usd_values.get(token.upper(), 0.0), 2),
            "desired_value_usd": round(target_allocation[token] * portfolio_value, 2),
            "adjusted_usd": round(target_allocation[token] * portfolio_value - current_usd_values.get(token.upper(), 0.0), 2),
            "action": (
                "buy" if (target_allocation[token] * portfolio_value - current_usd_values.get(token.upper(), 0.0)) > 0
                else "sell" if (target_allocation[token] * portfolio_value - current_usd_values.get(token.upper(), 0.0)) < 0
                else "hold"
            )
        }
        for token in target_allocation
    }

    return {
        "portfolio_value_usd": round(portfolio_value, 2),
        "rebalance_plan": suggestions,
        "skipped_tokens": skipped or None,
        "error": None
    }

