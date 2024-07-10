from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.data import SocialSentiment
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming the tickers below are health/fitness tech AI companies founded by women.
        # The list can be updated with the actual tickers of interest.
        self.tickers = ["TICKER1", "TICKER2", "TICKER3"]
        self.data_list = [SocialSentiment(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"  # Daily analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            sentiment_data = data.get(("social_sentiment", ticker), [])
            if sentiment_data:
                # Use the most recent sentiment
                recent_sentiment = sentiment_data[-1]["twitterSentiment"]  # Using Twitter sentiment as an example
                sentiment_score = (recent_sentiment - 0.5) * 2  # Normalize between -1 and 1 (assuming sentiment range is 0 to 1)
            else:
                sentiment_score = 0

            # Retrieve EMA for sentiment score adjustment
            ema_data = EMA(ticker, data["ohlcv"], 10)  # 10-day EMA for simplicity
            if ema_data and len(ema_data) > 1:
                current_price = data["ohlcv"][-1][ticker]["close"]
                previous_ema = ema_data[-2]
                current_ema = ema_data[-1]
                
                # Entry strategy: Positive sentiment and price above EMA
                if sentiment_score > 0 and current_price > current_ema:
                    allocation_dict[ticker] = 0.3  # Allocating a percentage to each asset
                # Exit strategy: Negative sentiment or price below EMA
                else:
                    allocation_dict[ticker] = 0
            else:
                # Default to no allocation if insufficient data
                allocation_dict[ticker] = 0

        return TargetDataMember(allocation_dict)