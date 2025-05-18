from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Union
from app.services import risksService

router = APIRouter(prefix="/risks", tags=["Risks"])

@router.post("/detect")
async def detect_risks_endpoint(pools: List[Dict] = Body(...)) -> Dict[str, Union[str, List[Dict]]]:
    result = await risksService.analyze_risks(pools)

    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return result
