"""Financial methods"""
import yfinance as yf


class Finance:
    """Handles finance related"""

    def check_ticker(self, ticker: str) -> bool:
        """Returns if ticker is a valid ticker"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                return True
            return False
        except:
            return False

    def get_current_price(self, ticker: str):
        """gets the current market price of the stock"""
        stock = yf.Ticker(ticker)
        return stock.info["regularMarketPrice"]

    def calculate_profit(self, start_price: float, end_price: float, stock_type: str, quantity: float):
        """calculates gain/loss"""
        if stock_type == "BUY":
            gain = round(((end_price - start_price) * quantity), 2)
        elif stock_type == "SHORT":
            gain = round(((start_price - end_price) * abs(quantity)), 2)
        else:
            return
        return gain
