# Sage - Decentralized DeFi Assistant

Sage is a decentralized DeFi assistant that provides insights and recommendations for investment strategies, focusing on yield farming, risk analysis, portfolio rebalancing, and more. It integrates with multiple DeFi data sources to offer real-time updates on token prices, yields, risks, and other financial metrics.

## Features

- **Real-time Yield Data**: Fetch real-time yield data for DeFi tokens.
- **Yield Analysis**: Get top yield pools and detect risks based on APY, TVL, and other parameters.
- **Portfolio Rebalancing**: Suggest strategies to rebalance portfolios according to target allocations.
- **Alerts**: Receive alerts for specific token thresholds, such as price changes or yield drops.
- **Pricing**: Fetch historical price data and current prices for tokens.
- **Customizable**: Easily extensible for custom strategies and additional DeFi tools.

## Tech Stack

- **Backend**: 
  - [FastAPI](https://fastapi.tiangolo.com/) for REST API
  - [MCP](https://github.com/openai/mcp) for context-driven interactions
  - [httpx](https://www.python-httpx.org/) for async HTTP requests
- **APIs**:
  - [DeFi Llama](https://defillama.com/) and [Beefy Finance](https://api.beefy.finance/vaults)for yield data
  - [CoinLib API](https://coinlib.io/) and [CoinRanking API](https://coinranking.com/) for token pricing
- **Package Management**: [UV](https://www.uv.dev/) as package manager

## Installation
To get started with Sage, follow these steps:

### Prerequisites

1. Python 3.8+  
2. Install **uv** as the package manager:
   ```bash 
   pip install uv

## Steps to Install
1. Clone the repository
   ```bash
   git clone "https://github.com/joshypet225//Sage.git
   cd Sage

2. Install dependencies using uv package manage
   ```bash
   uv install mcp

3. Create a .env file in the root directory and add the necessary API keys and configuration:
   ```bash
   touch .env
Sample .env file
    ```bash
    COINLIB_API_URL=https://coinlib.io/api/v1/
    COINLIB_API_KEY=your_coinlib_api_key
    COINRANKING_API_URL= https://api.coinranking.com/v2
    COINRANKING_API_KEY=your_coinranking_api_key
    DEFI_LLAMA_YIELDS_API=https://yields.llama.fi/pools

4. Run the application
   ```bash
   uvicorn main:app --reload

5. Run the server
   ```bash
   mcp run mcp_server.py

Documentations and details are available in [Component Overview](components.txt)

     

