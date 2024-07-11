from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Single asset strategy for simplicity
        self.ticker = "AAPL"

    @property
    def interval(self):
        # Using 1 day interval for daily moving averages
        return "1day"

    @property
    def assets(self):
        # List containing the stock we are interested in
        return [self.ticker]

    def run(self, data):
        # Accessing the historical data for the given ticker
        d = data["ohlcv"]
        
        # Calculating the short-term (50-day) and long-term (200-day) simple moving averages
        short_sma = SMA(self.ticker, d, 50)
        long_sma = SMA(self.ticker, d, 200)

        if len(short_sma) < 200 or len(long_sma) < 200:
            # Not enough data for calculation
            log("Not enough data for SMA calculation.")
            return TargetAllocation({})

        # Determine the crossover logic for buy/sell signals
        # Buy if the short-term SMA has crossed above the long-term SMA
        if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
            log("BUY signal")
            return TargetAllocation({self.ticker: 1.0})
        
        # Sell or avoid if the short-term SMA has crossed below the long-term SMA
        elif short_sma[-1] < long_sma[-1] and short_sma[-2] >= long_sma[-2]:
            log("SELL signal")
            return TargetAllocation({self.ticker: 0.0})
        
        # No change in position if there's no crossover
        else:
            log("No crossover signal. Holding position.")
            current_holding = data['holdings'].get(self.ticker, 0)
            return TargetAllocation({self.ticker: current_holding})