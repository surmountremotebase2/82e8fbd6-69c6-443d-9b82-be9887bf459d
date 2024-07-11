from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.tickers = ["AAPL"]  # Define the ticker of interest

    @property
    def assets(self):
        return self.tickers  # Returns the list of tickers the strategy deals with
    
    @property
    def interval(self):
        return "1day"  # Set the interval for data retrieval

    def run(self, data):
        current_date = data["ohlcv"][-1]["AAPL"]["date"]  # Retrieves the date of the latest data point
        day_of_month = int(current_date.split("-")[2])  # Extracts the day of the month from the date
        
        allocation = 0  # Default allocation
        
        # Determines the allocation based on whether the day of the month is odd or even
        if day_of_month % 2 == 1:
            allocation = 1  # Buy AAPL on odd days
        else:
            allocation = 0  # Sell (or do not hold) AAPL on even days
        
        # Logs allocation decision
        log(f"Trading on {current_date}: Allocation set to {'100%' if allocation == 1 else '0%'} for {self.tickers[0]}")
        
        return TargetAllocation({self.tickers[0]: allocation})