from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from datetime import datetime

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Initialize with the ticker we're interested in
        self.ticker = "AAPL"
        # Ideally, we would track order state, but for simplicity, we're just making decisions based on date

    @property
    def assets(self):
        # The only asset we are interested in is AAPL
        return [self.ticker]

    @property
    def interval(self):
        # Assuming daily checks are sufficient for our strategy
        return "1day"
    
    @property
    def data(self):
        # No additional data is needed since we're trading based on date
        return []

    def run(self, data):
        # Get today's date
        today = datetime.now().date()
        
        allocation_dict = {}
        
        # Check if today is the 15th of the month, if so, buy (allocate 100% to) AAPL
        if today.day == 15:
            log(f"Buying {self.ticker} on {today}")
            allocation_dict[self.ticker] = 1.0  # Buy / allocate 100% to AAPL
        
        # Check if today is the 30th of the month, if so, sell (allocate 0% to) AAPL
        elif today.day == 30:
            log(f"Selling {self.ticker} on {today}")
            allocation_dict[self.ticker] = 0  # Sell / allocate 0% to AAPL
        else:
            # If it's not the 15th or 30th, do not change the current allocation.
            # However, in a real strategy, we would return the current allocation (not addressed here due to simplicity).
            log(f"No action for {self.ticker} on {today}")
            return None  # Indicate no change, though in practice, maintaining state or indicating a hold is necessary

        return TargetAllocation(allocation_dict)