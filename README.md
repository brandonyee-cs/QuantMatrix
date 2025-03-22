# QuantMatrix

A comprehensive financial market analysis system implemented in APL, with Python-based data scraping.

## Overview

QuantMatrix is a powerful tool for analyzing financial markets, identifying patterns, optimizing portfolios, and visualizing results. It leverages APL's array programming capabilities for efficient numerical computation and uses Python for reliable data acquisition.

## Features

- Data acquisition from Yahoo Finance via Python
- Statistical analysis of financial time series
- Technical pattern recognition (MACD, RSI, Bollinger Bands)
- Portfolio optimization and backtesting
- Machine learning for price prediction
- Visualization of financial data (charts, heatmaps, dashboards)

## Requirements

- Dyalog APL (version 18.0 or higher recommended)
- Python 3.7+ with pandas and yfinance packages
- Basic knowledge of financial analysis concepts

## Getting Started

1. Clone this repository
2. Install Python dependencies: `pip install pandas yfinance`
3. Load the workspace: `)LOAD QuantMatrix`
4. Initialize the system: `QuantMatrix.Init`
5. Fetch stock data: `QM.Data.RefreshStockData ⎕NS''`
6. Import data: `data ← QM.Data.ImportStock 'AAPL'`
7. Run analysis: `result ← QuantMatrix.Analyze data`

## Project Structure

- `src/*.apln`: APL source code modules
- `config/*.json`: Configuration files
- `stock_scraper.py`: Python script for data acquisition

## Example Usage

```apl
⍝ Initialize system
QuantMatrix.Init

⍝ Refresh stock data from Yahoo Finance
refreshArgs ← ⎕NS''
refreshArgs.Tickers ← 'AAPL' 'MSFT' 'GOOGL'
QM.Data.RefreshStockData refreshArgs

⍝ Import stock data
aapl ← QM.Data.ImportStock 'AAPL'

⍝ Analyze returns
args ← ⎕NS''
args.Data ← aapl
args.Type ← 'Returns'
returns ← QuantMatrix.Analyze args

⍝ Show available stocks
QM.Data.ListAvailableStocks
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Brandon Yee