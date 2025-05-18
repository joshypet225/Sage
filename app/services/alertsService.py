from typing import Dict, List
from app.services.yieldsService import fetch_live_yields

# In-memory subscription registry (to replace with Cosmos DB later)
subscribers: Dict[str, List[str]] = {}  # token: [user_id_1, user_id_2, ...]


async def add_subscription(user_id: str, token: str) -> str:
    """
    Registers a user to receive yield alerts for a token.

    Args:
        user_id (str): Unique user identifier.
        token (str): Token symbol to subscribe to.

    Returns:
        str: Confirmation message.
    """
    token = token.upper()
    if token not in subscribers:
        subscribers[token] = []
    if user_id not in subscribers[token]:
        subscribers[token].append(user_id)
    return f"User {user_id} subscribed to {token} yield alerts."


async def check_alerts(threshold: float = 5.0) -> List[Dict]:
    """
    Checks subscribed tokens for high-yield opportunities and returns alerts.

    Args:
        threshold (float): APY threshold to trigger alerts (default: 5.0).

    Returns:
        List[Dict]: List of triggered alerts for subscribed users.
    """
    alerts = []

    for token, users in subscribers.items():
        result = await fetch_live_yields([token])
        for entry in result.get("results", []):
            if entry.get("apy", 0) >= threshold:
                for user in users:
                    alerts.append({
                        "user_id": user,
                        "token": token,
                        "project": entry.get("project"),
                        "chain": entry.get("chain"),
                        "apy": entry.get("apy"),
                    })

    return alerts

#List alerts for a specific user
async def list_user_alerts(user_id: str) -> List[Dict]:
    """
    Lists all alerts for a specific user.

    Args:
        user_id (str): Unique user identifier.

    Returns:
        List[Dict]: List of alerts for the specified user.
    """
    alerts = []
    for token, users in subscribers.items():
        if user_id in users:
            result = await fetch_live_yields([token])
            for entry in result.get("results", []):
                alerts.append({
                    "user_id": user_id,
                    "token": token,
                    "project": entry.get("project"),
                    "chain": entry.get("chain"),
                    "apy": entry.get("apy"),
                })
    return alerts
