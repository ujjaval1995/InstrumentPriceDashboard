import csv
import math
from datetime import datetime
from typing import Dict, List, Optional


class PriceData:
    def __init__(self):
        self.prices: Dict[str, List[Dict]] = {}
        self.tickers: List[str] = []

    def load_from_csv(self, filepath: str):
        grouped = {}

        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if not row:
                    continue

                ticker = (row.get("ticker") or "").strip().upper()
                date = (row.get("date") or "").strip()
                price_text = row.get("price")

                if not ticker or not date or price_text is None:
                    continue

                try:
                    price = float(price_text)
                except (TypeError, ValueError):
                    continue

                grouped.setdefault(ticker, []).append({
                    "date": date,
                    "price": price,
                })

        for ticker in grouped:
            grouped[ticker].sort(
                key=lambda item: datetime.strptime(item["date"], "%Y-%m-%d")
            )

        self.prices = grouped
        self.tickers = sorted(grouped.keys())
        print(f"Loaded {len(self.tickers)} instruments from {filepath}")



    def get_all_tickers(self) -> List[str]:
        return self.tickers

    def get_prices(self, ticker: str) -> Optional[List[Dict]]:
        ticker = ticker.strip().upper()
        return self.prices.get(ticker)

    def calculate_stats(self, ticker: str) -> Optional[Dict]:
        prices = self.get_prices(ticker)
        if not prices or len(prices) < 2:
            return None

        price_list = [p["price"] for p in prices]

        total_return = ((price_list[-1] / price_list[0]) - 1) * 100

        daily_returns = []
        for i in range(1, len(price_list)):
            daily_return = (price_list[i] - price_list[i - 1]) / price_list[i - 1]
            daily_returns.append(daily_return)

        if daily_returns:
            mean_return = sum(daily_returns) / len(daily_returns)
            variance = sum((r - mean_return) ** 2 for r in daily_returns) / len(daily_returns)
            volatility = math.sqrt(variance) * 100
        else:
            volatility = 0.0

        max_drawdown = self._calculate_max_drawdown(price_list)

        return {
            "ticker": ticker,
            "total_return_pct": round(total_return, 2),
            "daily_volatility_pct": round(volatility, 2),
            "max_drawdown_pct": round(max_drawdown, 2),
        }

    @staticmethod
    def _calculate_max_drawdown(prices: List[float]) -> float:
        if not prices:
            return 0.0

        max_drawdown = 0.0
        peak = prices[0]

        for price in prices[1:]:
            if price > peak:
                peak = price
            else:
                drawdown = ((peak - price) / peak) * 100
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

        return max_drawdown


price_data = PriceData()
