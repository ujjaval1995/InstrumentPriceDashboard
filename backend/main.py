from typing import List
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data_loader import price_data

app = FastAPI(title="Instrument Price Dashboard API")

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
    csv_paths = [
        "../market_data.csv",
        "market_data.csv",
    ]

    for path in csv_paths:
        if os.path.exists(path):
            print(f"Loading data from {path}")
            price_data.load_from_csv(path)
            return

    print("No CSV found, using sample data instead")
    price_data._generate_sample_data()


@app.get("/")
def read_root():
    return {
        "message": "Instrument Price Dashboard API",
        "version": "1.0.0",
        "instruments_loaded": len(price_data.get_all_tickers()),
    }


@app.get("/api/instruments", response_model=List[Instrument])
def get_instruments():
    tickers = price_data.get_all_tickers()
    return [{"ticker": t} for t in tickers]


@app.get("/api/prices/{ticker}", response_model=PriceSeries)
def get_prices(ticker: str):
    prices = price_data.get_prices(ticker)

    if prices is None:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker.upper()}' not found")

    return PriceSeries(
        ticker=ticker.upper(),
        prices=[PricePoint(date=p["date"], price=p["price"]) for p in prices],
    )


@app.get("/api/prices/{ticker}/stats", response_model=InstrumentStats)
def get_stats(ticker: str):
    stats = price_data.calculate_stats(ticker)

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker.upper()}' not found or not enough data",
        )

    return InstrumentStats(**stats)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
