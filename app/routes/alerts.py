from fastapi import APIRouter, Request, HTTPException, logger
from app.services.alertsService import add_subscription, check_alerts
from app.utils.logging import get_logger

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/alerts/subscribe")
async def subscribe_alerts(request: Request):
    """
    Subscribe a user to alerts for a specific token.
    """
    logger.info("Subscribing user to alerts.")
    body = await request.json()
    user = body.get("user_id")
    token = body.get("token")

    if not user or not token:
        raise HTTPException(status_code=400, detail="Both 'user_id' and 'token' are required.")

    msg = await add_subscription(user, token)
    logger.debug(f"Subscription message: {msg}")
    return {"message": msg}


@router.get("/alerts/check")
async def get_alerts(threshold: float = 5.0):
    """
    Trigger alert checking across all token subscriptions.

    Args:
        threshold (float): APY threshold to trigger alerts.
    """
    logger.info(f"Checking alerts with threshold: {threshold}")
    alerts = await check_alerts(threshold=threshold)
    logger.debug(f"Alerts found: {alerts}")
    return {"alerts": alerts}
