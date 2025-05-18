from mcp.server.fastmcp import Context
from app.services.yieldsService import fetch_live_yields
from tabulate import tabulate

async def handle_context(context: Context) -> dict:
    """
    Analyzes user prompt and returns yield info on tracked tokens.
    """
    prompt = context.prompt.lower()
    tracked_tokens = ["ETH", "USDC", "DAI", "WBTC", "stETH"]
    
    # Extract tokens mentioned in the user prompt
    tokens = [t for t in tracked_tokens if t.lower() in prompt]

    # If no tokens are mentioned, ask for token input
    if not tokens:
        return {
            "output": "Please mention a token you'd like to get yields for, such as ETH, DAI, or USDC.",
            "data": None
        }

    # Fetch live yield data from external service
    result = await fetch_live_yields(tokens)

    # Error handling if the data fetch fails or returns empty results
    if "error" in result or not result.get("results"):
        return {
            "output": "Error fetching yield data or no results found. Please try again later.",
            "data": None
        }

    # Prepare data for tabulated output
    table_data = []
    for entry in result["results"]:
        table_data.append([
            entry.get("token"),
            entry.get("project"),
            entry.get("chain"),
            f"{entry.get('apy', 0):.2f}%",
            f"${entry.get('tvlUsd', 0):,.2f}",
            entry.get("url")
        ])

    # Define the headers for the tabulated data
    headers = ["Token", "Project", "Chain", "APY", "TVL (USD)", "URL"]
    table = tabulate(table_data, headers=headers, tablefmt="grid")

    # Construct the output to return
    output = f"Here are the latest yields I found for the tokens you mentioned:\n\n{table}"

    return {
        "output": output,
        "data": result["results"]
    }
