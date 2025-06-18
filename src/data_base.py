"""main for stock tracker"""
import sqlite3
import yfinance as yf

class Transaction:
    """
    Represents a single transaction

    Instance Attributes:
        - ticker: code of the stock
        - type: either buy/short/sell
        - date: tuple in form of (year, month, day)
        - quantity: number of stocks
        - price: price of the buy/sell
        - fees: fee for the transaction
        - left: how many shares left
    """
    ticker: str
    type: str
    date: list
    quantity: float
    price: float
    fees: float
    left: float

    def __init__(self, ticker:str, type:str, date:list, quantity:float, price:float, fees: float, left:float) -> None:
        """Initializes values to the arguments"""
        self.ticker = ticker
        self.type = type
        self.date = date
        self.quantity = quantity
        self.price = price
        self.fees = fees
        self.left = left

class Finance:
    def check_ticker(self, ticker:str) ->bool:
        """Returns if ticker is a valid ticker"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                return True
            return False
        except:
            return False

    def get_current_price(self, ticker:str):
        stock = yf.Ticker(ticker)
        return stock.info["previousClose"]

class TransactionHandler:
    """Handles database related things"""
    def create_sql(self):
        """Creates SQL database and tables"""

        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        type TEXT,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        quantity REAL NOT NULL,
        price REAL NOT NULL,
        fees REAL NOT NULL,
        remaining REAL NOT NULL
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profit (
        transaction_id INTEGER,
        initial_price REAL,
        final_price REAL,
        profit REAL,
        FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )""")
        connection.close()

    def upload_transaction(self, transaction: Transaction):
        """Uploads the current transaction to the database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO transactions (ticker, type, year, month, day, quantity, price, fees, remaining)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?) """, (transaction.ticker, transaction.type, transaction.date[0],
                                                transaction.date[1], transaction.date[2], transaction.quantity,
                                                transaction.price, transaction.fees, transaction.quantity))
        connection.commit()
        connection.close()

    def read_data_base(self):
        """reads database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions""")
        results = cursor.fetchall()
        print(results)

    def get_active_stocks(self):
        """gets stocks that haven't been sold"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions WHERE remaining > 0""")
        results = cursor.fetchall()
        transactions = []
        for transaction in results:
            transactions.append(Transaction(transaction[1], transaction[2],
                                            [transaction[3],transaction[4],transaction[5]], transaction[6],
                                            transaction[7], transaction[8], transaction[9]))
        return transactions

    def delete_data_base(self):
        """deletes database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM transactions""")
        connection.commit()
        connection.close()


if __name__ == "__main__":
    ...
