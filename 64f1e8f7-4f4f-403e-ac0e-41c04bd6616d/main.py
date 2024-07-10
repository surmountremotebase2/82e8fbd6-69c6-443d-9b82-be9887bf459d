from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentinent, InsiderTrading
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # This example assumes tickers here are representative of health and fitness tech industries.
        # In a real scenario, this list should be populated with actual tickers of businesses founded by women in health and fitness tech.
        self.tickers = ["FTNS", "HLTH", "AIFIT", "WTECH"]  # Placeholder ticker symbols for companies of interest
        self.data_list = [SocialSentiment(ticker) for ticker in self.tickers] + \
                         [InsiderTrading(ticker) for ticker in self.tickers]
    
    @property
    def interval(self):
        return "1day"
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return self.data_list
    
    def run(self, data):
        # Initialize target allocation dictionary with 0 allocations
        allocation_dict = {ticker: 0.0 for ticker in self.tickers}
        positive_sentiment_tickers = []

        for ticker in self.tickers:
            sentiment_data = data.get(("social_sentiment", ticker), None)
            insider_data = data.get(("insider_trading", ticker), None)
            positive_sentiment = False
            insider_confidence = False
            
            # Check if there's a positive sentiment shift
            if sentiment_data and len(sentiment_data) > 0:
                # Example logic: If the latest sentiment is positive, mark this ticker
                if sentiment_data[-1]["twitterSentiment"] > 0.5:  # Adjust based on available metrics
                    positive_sentiment = True
            
            # Check for insider confidence, e.g., recent purchases by insiders could indicate confidence
            if insider_data and len(insider_data) > 0:
                latest_insider_action = insider_data[-1]["transactionType"]
                if 'Buy' in latest_insider_action:
                    insider_confidence = True
            
            # If both sentiment and insider trading indicators are positive, include this stock in the allocation
            if positive_sentiment and insider_confidence:
                positive_sentiment_tickers.append(ticker)
        
        # Equally distribute the allocation among positively identified stocks
        if positive_sentiment_tickers:
            equal_allocation = 1 / len(positive_sentiment_tickers)
            for ticker in positive_sentiment_tickers:
                allocation_dict[ticker] = equal_allocation
        
        return TargetAllocation(allocation_dict)