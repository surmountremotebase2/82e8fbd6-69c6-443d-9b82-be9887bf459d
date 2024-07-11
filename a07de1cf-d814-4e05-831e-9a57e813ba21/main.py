from surmount.base_class import Strategy, TargetAllocation
from surmount.data import WestTexasIntermediate
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # List of oil stocks to potentially buy
        self.tickers = ["XOM", "CVX", "OXY", "SLB"]
        # Include West Texas Intermediate futures in the data list for analysis
        self.data_list = [WestTexasIntermediate()]

    @property
    def interval(self):
        # Setting daily interval for analysis
        return "1day"

    @property
    def assets(self):
        # The assets this strategy is interested in
        return self.tickers

    @property
    def data(self):
        # Data required for the strategy computation
        return self.data_list

    def run(self, data):
        # Default allocation is 0 for all tickers
        allocation_dict = {i: 0 for i in self.tickers}

        # Retrieving WTI data from the data dictionary
        wti_data = data[("west_texas_intermediate",)]
        
        if wti_data and len(wti_data) >= 20:
            # If there's enough data, calculate the 20-day moving average and standard deviation
            prices = pd.Series([d['value'] for d in wti_data])

            moving_average = prices.rolling(window=20).mean().iloc[-1]
            std_dev = prices.rolling(window=20).std().iloc[-1]

            # Check if the latest WTI price is one standard deviation below the moving average
            if prices.iloc[-1] < (moving branchaverage - std_dev):
                # If so, set an equal allocation of 25% to each oil stock as an example
                # This can be adjusted based on risk management preferences
                allocation = 0.25
                allocation_dict = {ticker: allocation for ticker in self.tickers}

        return TargetAllocation(allocation_dict)