"""main for stock tracker"""
import datetime
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
        - remaining: how many shares remaining
    """
    id: int
    ticker: str
    type: str
    date: tuple[int, int, int]
    quantity: float
    price: float
    remaining: float

    def __init__(self, ticker: str, type: str, date: tuple[int, int, int], quantity: float, price: float, remaining: float,
                 id=None) -> None:
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

    def calculate_profit(self, start_price:float, end_price: float, stock_type:str, quantity:float):
        """calculates gain/loss"""
        if stock_type == "BUY":
            gain = round(((end_price - start_price) * quantity), 2)
        elif stock_type == "SHORT":
            gain = round(((start_price - end_price) * abs(quantity)), 2)
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
        CREATE TABLE IF NOT EXISTS profits (
        transaction_id INTEGER,
        sell_price REAL,
        profit REAL,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )""")
        connection.close()

    def upload_transaction(self, transaction: Transaction):
        """Uploads the current transaction to the database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO transactions (ticker, type, year, month, day, quantity, price, remaining)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?) """, (transaction.ticker, transaction.type, transaction.date[0],
                                             transaction.date[1], transaction.date[2], transaction.quantity,
                                             transaction.price, transaction.quantity))
        connection.commit()
        connection.close()

    def get_remaining(self, get_id: int):
        """returns the amount of stocks remaining for a given id"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions WHERE id = ?""", (get_id,))
        results = cursor.fetchall()[0]
        return results[8]

    def sell_transaction(self, sell_id: int, sell_quantity: float, sell_price: float, date:tuple[int, int, int]):
        """Handles the selling of a ticker"""
        year, month, day = date
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()

        cursor.execute("""UPDATE transactions SET remaining = (remaining - ?) WHERE id = ?""",
                       (sell_quantity, sell_id))
        connection.commit()
        cursor.execute("""SELECT price, type FROM transactions WHERE id = ?""", (sell_id,))
        results = cursor.fetchall()[0]
        finance = Finance()
        profit = finance.calculate_profit(results[0], sell_price, results[1], sell_quantity)
        cursor.execute(
            """INSERT INTO profits VALUES (?, ?, ?, ?, ?, ?)""",
            (sell_id, sell_price, profit, year, month, day))
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
                                            (transaction[3], transaction[4], transaction[5]), transaction[6],
                                            transaction[7], transaction[8], transaction[0]))

        connection.close()
        return transactions

    def delete_transaction(self, id: int):
        """deletes transaction"""
        connection = sqlite3.connect('transactions.db')
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM transactions WHERE id = ?""", (id,))
        connection.commit()
        connection.close()

    def get_profits(self, today):
        """Gets profit of all time, this month, and today and returns it in a list"""
        year, month, day = today
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT profit FROM profits WHERE year = ? AND month = ? AND day = ?""", (year, month, day))
        day_results = cursor.fetchall()
        cursor.execute("""SELECT profit FROM profits WHERE year = ? AND month = ?""", (year, month))
        month_results = cursor.fetchall()
        cursor.execute("""SELECT profit FROM profits""")
        all_results = cursor.fetchall()
        print(all_results)
        print(month_results)
        print(day_results)
        profits = []
        for prof in [all_results, month_results, day_results]:
            total = 0
            for entry in prof:
                total += sum(entry)
            profits.append(round(total,2))
        return profits

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
        cursor.execute("""SELECT * FROM profits""")
        results = cursor.fetchall()
        for transaction in results:
            print(transaction)
        connection.close()


def get_date():
    """returns todays date in a tuple of (year, month, date)"""
    today = datetime.date.today()
    return today.year, today.month, today.day
