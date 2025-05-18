from fastapi import APIRouter, Body, HTTPException, logger
from typing import Dict
from app.services.rebalanceService import suggest_rebalance_strategy

router = APIRouter(prefix="/rebalance", tags=["Rebalancer"])

@router.post("/plan")
async def rebalance_plan(
    payload: Dict = Body(..., example={
        "current_holdings": {"ETH": 0.5, "DAI": 1000},
        "target_allocation": {"ETH": 0.4, "DAI": 0.6}
    })
):
    logger.info(f"Received rebalance request with payload: {payload}")
    """
    Suggest a portfolio rebalance strategy based on current holdings and target allocation.
    """
    current = payload.get("current_holdings")
    target = payload.get("target_allocation")

    if not current or not target:
        raise HTTPException(status_code=400, detail="Both 'current_holdings' and 'target_allocation' are required.")

    plan = await suggest_rebalance_strategy(current, target)
    logger.debug(f"Rebalance plan: {plan}")
    return {"strategy": plan}
