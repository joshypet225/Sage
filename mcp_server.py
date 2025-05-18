import logging
from typing import Dict, List, Union
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
from app.services.yieldsService import aggregator 
from app.services.context_handler import handle_context
from app.services import pricingService, risksService, rebalanceService, alertsService
from app.routes import alerts, mcp as mcp_routes
from app.routes import risks, yields, rebalance, alerts as alerts_module, pricing

# Load env and logging
load_dotenv()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MCP Configuration
mcp = FastMCP(
    name="Sage",
    description="Sage is a DeFi assistant that provides insights and recommendations for investment strategies.",
    context_handler=handle_context,
    context_handler_type="async",
    timeout=30,
    max_tokens=2000
)

# FastAPI App Setup
app = FastAPI(
    title="Sage",
    description="Sage is a DeFi assistant that provides insights and recommendations for investment strategies.",
    version="1.0.0"
)

# # Register routers
# app.include_router(mcp_routes.router)
# app.include_router(yields.router)
# app.include_router(risks.router)
# app.include_router(rebalance.router)
# app.include_router(alerts.router)
# app.include_router(pricing.router)

# MCP Tools
@mcp.tool()
async def add_subscription(user_id: str, token: str) -> str:
    return await alertsService.add_subscription(user_id, token)

@mcp.tool()
async def check_alerts(threshold: float = 5.0) -> List[Dict]:
    return await alertsService.check_alerts(threshold)

@mcp.tool()
async def list_user_alerts(user_id: str) -> List[Dict]:
    return await alertsService.list_user_alerts(user_id)

@mcp.tool()
async def get_top_yields(tokens: List[str]) -> Dict:
    from app.services.yieldsService import aggregator
    return await aggregator.fetch_top_yields(tokens)

@mcp.tool()
async def get_yield_info(token: str) -> Dict:
    from app.services.yieldsService import aggregator
    return await aggregator.get_yields_info(token)

@mcp.tool()
async def get_live_yields(tokens: List[str]) -> Dict:
    from app.services.yieldsService import aggregator
    return await aggregator.fetch_live_yields(tokens)

@mcp.tool()
def detect_risks(pools: List[str]) -> Dict:
    return risksService.analyze_risks(pools)

@mcp.tool()
async def get_price_history(symbol: str, days: int = 7) -> Union[str, Dict]:
    return await pricingService.get_price_history(symbol, days)

@mcp.tool()
async def get_token_price(symbol: str) -> Union[str, Dict]:
    return await pricingService.get_token_price(symbol)

@mcp.tool()
async def get_token_prices(symbols: List[str]) -> Dict[str, Union[str, Dict]]:
    return await pricingService.get_token_prices(symbols)

# MCP Resources

@mcp.resource("alerts://tokens/{token}")
async def get_token_alerts(token: str) -> Union[str, List[Dict]]:
    logger.debug(f"Getting alerts for {token}")
    alert_list = await alertsService.check_alerts(threshold=5.0)
    token_alerts = [alert for alert in alert_list if alert["token"] == token]
    return token_alerts if token_alerts else f"No alerts found for {token}."

@mcp.resource("yields://token-yields/tokens/{token}")
async def get_token_yields(token: str) -> Dict:
    logger.debug(f"Fetching yield info for token: {token}")
    return await aggregator.get_yields_info(token)

@mcp.resource("yields://token-yields/top-yields/{tokens}")
async def get_top_yields_resource(tokens: str) -> Dict:
    logger.debug(f"Fetching top yields for tokens: {tokens}")
    token_list = [t.strip() for t in tokens.split(",") if t.strip()]
    if not token_list:
        return "No valid tokens provided."
    return await aggregator.fetch_top_yields(token_list)

@mcp.resource("yields://token-yields/live-yields/{tokens}")
async def get_live_yields_resource(tokens: str) -> Dict:
    logger.debug(f"Fetching live yields for tokens: {tokens}")
    token_list = [t.strip() for t in tokens.split(",") if t.strip()]
    if not token_list:
        return "No valid tokens provided."
    return await aggregator.fetch_live_yields(token_list)


@mcp.resource("risks://detect-risks/{pools}")
def detect_risks_resource(pools: str) -> Union[str, Dict]:
    pool_list = [p.strip() for p in pools.split(",") if p.strip()]
    if not pool_list:
        return "No valid pool addresses provided."
    return risksService.analyze_risks(pool_list)

@mcp.resource("rebalance://rebalance-portfolio/{current_holdings}/{target_allocation}")
async def rebalance_portfolio(current_holdings: str, target_allocation: str) -> Union[str, Dict]:
    try:
        current = {k: float(v) for k, v in (item.split(":") for item in current_holdings.split(","))}
        target = {k: float(v) for k, v in (item.split(":") for item in target_allocation.split(","))}
    except ValueError:
        return "Invalid format. Use key:value pairs like ETH:50,USDC:50"
    
    if not current or not target:
        return "Both 'current_holdings' and 'target_allocation' are required."
    
    return await rebalanceService.suggest_rebalance_strategy(current, target)

@mcp.resource("pricing://token-prices/{symbol}")
async def get_token_price_resource(symbol: str) -> Union[str, Dict]:
    if not symbol:
        return "No valid token symbol provided."
    result = await pricingService.get_token_prices([symbol])
    return result if "error" not in result else f"Error: {result['error']}"

@mcp.resource("pricing://token-prices/{symbol}/history/{days}")
async def get_price_history_resource(symbol: str, days: int) -> Union[str, Dict]:
    VALID_DAYS = {1, 7, 30, 90, 365}
    if days not in VALID_DAYS:
        return f"Invalid 'days' value. Must be one of: {sorted(VALID_DAYS)}"
    result = await pricingService.get_price_history(symbol, days)
    return result if not isinstance(result, str) else f"Error: {result}"

@mcp.resource("greeting://welcome-to-sage")
def root() -> Dict:
    return {"message": "Welcome to Sage!"}

# Mount the MCP server
app.mount("/mcp", mcp.app)

# Optional: Startup hook for logging
@app.lifespan("startup")
async def on_startup():
    logger.info("🚀 Sage server started and MCP mounted at /mcp")

