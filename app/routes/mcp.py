from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/.well-known/mcp-server.json")
async def mcp_metadata():
    return JSONResponse(
        status_code=200,
        content={
            "name": "Sage",
            "description": "Sage is a DeFi assistant that provides insights and recommendations for investment strategies.",
            "version": "1.0.0",
            "context_endpoint": "/handle_context"
        },
        media_type="application/json"
    )
