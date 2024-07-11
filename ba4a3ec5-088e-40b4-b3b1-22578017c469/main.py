from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        # Although Asset data is not required for SMA, defining it for explicit clarity
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        # Using daily intervals to compute the moving average
        return "1day"

    @property
    def assets(self):
        # Return the tickers we're interested in (AAPL in this case)
        return self.tickers

    @property
    def data(self):
        # Return the required data sources
        return self.data_list

    def run(self, data):
        # Initialize holding variable for AAPL
        aapl_stake = 0
        
        # Accessing the closing prices of AAPL
        closes = [i["AAPL"]["close"] for i in data["ohlcv"]]
        
        # Calculate the 30-day simple moving average (SMA) for AAPL
        sma_30 = SMA("AAPL", data["ohlcv"], 30)

        if len(closes) > 0 and sma_30 is not None:
            # Latest available closing price
            current_price = closes[-1]
            
            # Latest 30-day SMA value
            current_sma = sma_30[-1]
            
            # Buy signal: Current price falls below the 30-day SMA
            if current_price < current_sma:
                log("Buying AAPL")
                aapl_stake = 1  # Adjust this value based on your allocation strategy
            # Sell signal: Current price hits above the 30-day SMA
            elif current_price > current_sma:
                log("Selling AAPL")
                aapl_stake = 0  # Sell all holdings
                
        # Return the target allocation
        return TargetAllocation({"AAPL": aapl_stake})