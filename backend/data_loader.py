import csv
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import math

class PriceData:
    """In-memory store for instrument price data from CSV"""
    
    def __init__(self):
        self.prices: Dict[str, List[Dict]] = {}  # ticker -> list of {date, price}
        self.tickers: List[str] = []
    
    def load_from_csv(self, filepath: str):
        """Load price data from CSV file (columns: date, ticker, price)"""
        try:
            ticker_data = {}
            
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ticker = row['ticker'].strip().upper()
                    date = row['date'].strip()
                    price = float(row['price'])
                    
                    if ticker not in ticker_data:
                        ticker_data[ticker] = []
                    
                    ticker_data[ticker].append({
                        'date': date,
                        'price': price
                    })
            
            # Sort by date for each ticker
            for ticker in ticker_data:
                ticker_data[ticker].sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
            
            self.prices = ticker_data
            self.tickers = sorted(list(ticker_data.keys()))
            
            print(f"Loaded {len(self.tickers)} instruments with price data")
        except FileNotFoundError:
            print(f"Warning: CSV file not found at {filepath}")
            self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate synthetic sample data for testing"""
        print("Generating synthetic sample data for 200 instruments...")
        import random
        
        base_date = datetime(2024, 1, 1)
        tickers = [f"INST{i:03d}" for i in range(1, 201)]
        
        for ticker in tickers:
            prices = []
            current_price = random.uniform(50, 200)
            
            for day in range(30):
                date = base_date + timedelta(days=day)
                # Random walk
                change = random.uniform(-0.05, 0.05)
                current_price *= (1 + change)
                current_price = max(current_price, 10)  # Floor price
                
                prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'price': round(current_price, 2)
                })
            
            self.prices[ticker] = prices
        
        self.tickers = sorted(tickers)
    
    def get_all_tickers(self) -> List[str]:
        """Return sorted list of all tickers"""
        return self.tickers
    
    def get_prices(self, ticker: str) -> List[Dict] | None:
        """Get price series for a specific ticker"""
        ticker = ticker.strip().upper()
        return self.prices.get(ticker)
    
    def calculate_stats(self, ticker: str) -> Dict | None:
        """Calculate statistics for a ticker"""
        prices = self.get_prices(ticker)
        if not prices or len(prices) < 2:
            return None
        
        price_list = [p['price'] for p in prices]
        
        # Total return %
        total_return = ((price_list[-1] / price_list[0]) - 1) * 100
        
        # Daily volatility (stdev of returns)
        daily_returns = []
        for i in range(1, len(price_list)):
            daily_return = (price_list[i] - price_list[i-1]) / price_list[i-1]
            daily_returns.append(daily_return)
        
        if daily_returns:
            mean_return = sum(daily_returns) / len(daily_returns)
            variance = sum((r - mean_return) ** 2 for r in daily_returns) / len(daily_returns)
            volatility = math.sqrt(variance) * 100  # Convert to percentage
        else:
            volatility = 0.0
        
        # Max drawdown
        max_drawdown = self._calculate_max_drawdown(price_list)
        
        return {
            'ticker': ticker,
            'total_return_pct': round(total_return, 2),
            'daily_volatility_pct': round(volatility, 2),
            'max_drawdown_pct': round(max_drawdown, 2)
        }
    
    @staticmethod
    def _calculate_max_drawdown(prices: List[float]) -> float:
        """Calculate maximum drawdown from peak to trough"""
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

# Global instance
price_data = PriceData()
