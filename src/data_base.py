"""main for stock tracker"""
import sqlite3

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

    def __innit__(self, ticker:str, type:str, date:list, quantity:float, price:float, fees: float, left:float) -> None:
        """Initializes values to the arguments"""
        self.ticker = ticker
        self.type = type
        self.date = date
        self.quantity = quantity
        self.price = price
        self.fees = fees
        self.left = left


class TransactionHandler:
    """Handles database related things"""
    def create_sql(self):
        """Creates SQL database and tables"""

        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER AUTO_INCREMENT
        ticker TEXT
        type TEXT
        year NUMERIC
        month NUMERIC
        day NUMERIC
        quantity REAL
        price REAL
        fees REAL
        left REAL        
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS profit (
        transaction_id INTEGER
        initial_price REAL
        final_price REAL
        profit REAL
        FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        )""")
        connection.close()

    def upload_transaction(self, transaction: Transaction):
        """Uploads the current transaction to the database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO transactions (ticker, type, year, month, day, quantity, price, fees, left)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?) """, (transaction.ticker, transaction.type, transaction.date[0],
                                                transaction.date[1], transaction.date[2], transaction.quantity,
                                                transaction.price, transaction.fees, transaction.quantity))
        connection.close()

    def read_data_base(self):
        """reads database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM transactions""")


if __name__ == "__main__":
    ...
