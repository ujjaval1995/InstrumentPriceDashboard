from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
from pydantic import BaseModel
import os
from data_loader import price_data

app = FastAPI(
    title="Instrument Price Dashboard API",
    description="API for instrument price tracking and analysis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PricePoint(BaseModel):
    date: str
    price: float


class PriceSeries(BaseModel):
    ticker: str
    prices: List[PricePoint]


class InstrumentStats(BaseModel):
    ticker: str
    total_return_pct: float
    daily_volatility_pct: float
    max_drawdown_pct: float


class Instrument(BaseModel):
    ticker: str


@app.on_event("startup")
async def startup_event():
    """Load CSV data on startup"""
    # Try to load CSV from current directory or data folder
    csv_paths = [
        "prices.csv",
        "data/prices.csv",
        "../prices.csv",
        "backend/prices.csv"
    ]
    
    for path in csv_paths:
        if os.path.exists(path):
            price_data.load_from_csv(path)
            break
    else:
        # If no CSV found, generate sample data
        print("No CSV file found, using generated sample data")
        price_data._generate_sample_data()


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "Instrument Price Dashboard API",
        "version": "1.0.0",
        "instruments_loaded": len(price_data.get_all_tickers())
    }


@app.get("/api/instruments", response_model=List[Instrument])
def get_instruments():
    """
    Get list of all available instruments (tickers).
    Returns up to 200 tickers.
    """
    tickers = price_data.get_all_tickers()
    return [{"ticker": t} for t in tickers]


@app.get("/api/prices/{ticker}", response_model=PriceSeries)
def get_prices(ticker: str):
    """
    Get full 30-day price time series for a specific ticker.
    
    Args:
        ticker: The instrument ticker symbol (e.g., 'AAPL')
    
    Returns:
        PriceSeries with dates and closing prices
    
    Raises:
        404: If ticker is not found
    """
    prices = price_data.get_prices(ticker)
    
    if prices is None:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker.upper()}' not found"
        )
    
    price_points = [
        PricePoint(date=p['date'], price=p['price'])
        for p in prices
    ]
    
    return PriceSeries(ticker=ticker.upper(), prices=price_points)


@app.get("/api/prices/{ticker}/stats", response_model=InstrumentStats)
def get_stats(ticker: str):
    """
    Get computed statistics for a ticker.
    
    Stats Include:
    - total_return_pct: (last_price / first_price - 1) * 100
    - daily_volatility_pct: Standard deviation of daily returns
    - max_drawdown_pct: Largest peak-to-trough decline
    
    Args:
        ticker: The instrument ticker symbol (e.g., 'AAPL')
    
    Returns:
        InstrumentStats with computed metrics
    
    Raises:
        404: If ticker is not found
    """
    stats = price_data.calculate_stats(ticker)
    
    if stats is None:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker.upper()}' not found or insufficient data"
        )
    
    return InstrumentStats(**stats)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
