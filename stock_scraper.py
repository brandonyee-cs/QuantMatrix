#!/usr/bin/env python3
"""
QuantMatrix Stock Data Scraper

This script downloads historical stock data using the Yahoo Finance API 
and saves it to CSV files for use by the QuantMatrix APL system.
"""

import os
import argparse
import datetime as dt
import pandas as pd
import yfinance as yf
from typing import List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('stock_scraper')

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Download stock data and save to CSV files")
    
    parser.add_argument(
        "--tickers", 
        type=str, 
        nargs="+", 
        default=["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
        help="List of stock tickers to download (default: AAPL MSFT GOOGL AMZN META)"
    )
    
    parser.add_argument(
        "--start", 
        type=str, 
        default=(dt.datetime.now() - dt.timedelta(days=365*5)).strftime("%Y-%m-%d"),
        help="Start date in YYYY-MM-DD format (default: 5 years ago)"
    )
    
    parser.add_argument(
        "--end", 
        type=str, 
        default=dt.datetime.now().strftime("%Y-%m-%d"),
        help="End date in YYYY-MM-DD format (default: today)"
    )
    
    parser.add_argument(
        "--interval", 
        type=str, 
        choices=["1d", "1wk", "1mo"], 
        default="1d",
        help="Data interval (default: 1d)"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="data/stocks",
        help="Output directory for CSV files (default: data/stocks)"
    )
    
    return parser.parse_args()

def download_stock_data(
    ticker: str, 
    start_date: str, 
    end_date: str, 
    interval: str = "1d"
) -> Optional[pd.DataFrame]:
    """
    Download historical stock data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        interval: Data interval (1d, 1wk, 1mo)
        
    Returns:
        DataFrame with stock data or None if download fails
    """
    try:
        logger.info(f"Downloading data for {ticker} from {start_date} to {end_date}")
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date, interval=interval)
        
        if df.empty:
            logger.warning(f"No data returned for {ticker}")
            return None
            
        # Reset index to make Date a column
        df = df.reset_index()
        
        # Ensure column names match what APL code expects
        df = df.rename(columns={
            'Date': 'Date',
            'Open': 'Open',
            'High': 'High',
            'Low': 'Low',
            'Close': 'Close',
            'Volume': 'Volume'
        })
        
        # Format date as string in YYYY-MM-DD format
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # Select and order columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        return df
        
    except Exception as e:
        logger.error(f"Error downloading data for {ticker}: {str(e)}")
        return None

def save_to_csv(df: pd.DataFrame, ticker: str, output_dir: str) -> bool:
    """
    Save DataFrame to CSV file.
    
    Args:
        df: DataFrame with stock data
        ticker: Stock ticker symbol
        output_dir: Directory to save CSV file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Define output file path
        file_path = os.path.join(output_dir, f"{ticker}.csv")
        
        # Save to CSV
        df.to_csv(file_path, index=False)
        logger.info(f"Saved {ticker} data to {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving {ticker} data: {str(e)}")
        return False
        
def main():
    """Main function to download and save stock data."""
    args = parse_arguments()
    
    # Process each ticker
    successful = 0
    failed = 0
    
    for ticker in args.tickers:
        # Download data
        df = download_stock_data(
            ticker=ticker,
            start_date=args.start,
            end_date=args.end,
            interval=args.interval
        )
        
        if df is not None:
            # Save to CSV
            if save_to_csv(df, ticker, args.output_dir):
                successful += 1
            else:
                failed += 1
        else:
            failed += 1
    
    # Summary
    logger.info(f"Download complete. Successful: {successful}, Failed: {failed}")
    
if __name__ == "__main__":
    main()