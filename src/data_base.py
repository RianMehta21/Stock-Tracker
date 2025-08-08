"""main for stock tracker"""
import sqlite3
import yfinance as yf

class Transaction:
    """
    Represents a single transaction

    Instance Attributes:
        - id: id of the transaction
        - ticker: code of the stock
        - type: either buy/short
        - date: tuple in form of (year, month, day)
        - quantity: number of stocks
        - price: price of the buy/short
        - left: how many shares left
    """
    id: int
    ticker: str
    type: str
    date: list
    quantity: float
    price: float
    left: float

    def __init__(self, ticker:str, type:str, date:list, quantity:float, price:float, remaining:float, id=None) -> None:
        """Initializes values to the arguments"""
        self.ticker = ticker.upper()
        self.type = type
        self.date = date
        self.quantity = quantity
        self.price = price
        self.remaining = remaining
        if id:
            self.id = id

class Finance:
    """Handles finance related"""
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
        """gets the current market price of the stock"""
        stock = yf.Ticker(ticker)
        return stock.info["regularMarketPrice"]

    def calculate_profit(self, stock:Transaction, curr_price:int):
        """calculates gain/loss"""
        if stock.type == "BUY":
            gain = round(((curr_price - stock.price) * stock.remaining), 2)
        elif stock.type == "SHORT":
            gain = round(((stock.price - curr_price) * abs(stock.remaining)), 2)
        else:
            return
        return gain


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
        remaining REAL NOT NULL
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profit (
        transaction_id INTEGER,
        initial_price REAL,
        profit REAL,
        FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )""")
        connection.close()

    def upload_transaction(self, transaction: Transaction):
        """Uploads the current transaction to the database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO transactions (ticker, type, year, month, day, quantity, price, remaining)
        values(?, ?, ?, ?, ?, ?, ?, ?) """, (transaction.ticker, transaction.type, transaction.date[0],
                                                transaction.date[1], transaction.date[2], transaction.quantity,
                                                transaction.price, transaction.quantity))
        connection.commit()
        connection.close()

    def get_remaining(self, get_id:int):
        """returns the amount of stocks remaining for a given id"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions WHERE id = ?""", (get_id,))
        results = cursor.fetchall()[0]
        return results[8]

    def sell_transaction(self, sell_id:int, quantity:float):
        """Handles the selling of a ticker"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()

        cursor.execute("""UPDATE transactions SET remaining = (remaining - ?) WHERE id = ?""",
                           (quantity, sell_id))
        connection.commit()

        connection.close()

    def get_active_stocks(self) -> list:
        """gets stocks that haven't been sold"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions WHERE remaining > 0""")
        results = cursor.fetchall()
        transactions = []
        for transaction in results:
            transactions.append(Transaction(transaction[1], transaction[2],
                                            [transaction[3],transaction[4],transaction[5]], transaction[6],
                                            transaction[7], transaction[8], transaction[0]))

        connection.close()
        return transactions

    def delete_transaction(self,id:int):
        """deletes transaction"""
        connection = sqlite3.connect('transactions.db')
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM transactions WHERE id = ?""", (id,))
        connection.commit()
        connection.close()

    def delete_data_base(self):
        """deletes database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM transactions""")
        connection.commit()
        connection.close()

    def read_transaction(self):
        """gets stocks that haven't been sold"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions""")
        results = cursor.fetchall()
        for transaction in results:
            print(transaction)
        connection.close()

    def read_profit(self):
        """gets stocks that haven't been sold"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM profit""")
        results = cursor.fetchall()
        for transaction in results:
            print(transaction)
        connection.close()
