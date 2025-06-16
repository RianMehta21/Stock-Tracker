import tkinter
import sqlite3


class Transaction():
    """
    Represents a single transaction

    Instance Attributes:
        - ticker: code of the stock
        - type: either buy/short/square off
        - date: tuple in form of (year, month, day)
        - quantity: number of stocks
        - price: price of the buy/sell
        - fees: fee for the transaction
    """
    ticker: str
    type: str
    date: tuple
    quantity: int
    price: float
    fees: float

    def __innit__(self, ticker:str, type:str, date:tuple, quantity:int, price:float, fees: float) -> None:
        """Initializes values to the arguments"""
        self.ticker = ticker
        self.type = type
        self.date = date
        self.quantity = quantity
        self.price = price
        self.fees = fees

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
        quantity INTEGER
        price REAL
        fees REAL
        left INTEGER        
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

    def upload_transaction(self):
        """Uploads the current transaction to the database"""
        connection = sqlite3.connect("transactions.db")
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO transactions (ticker, type, year, month, day, quantity, price, fees, left)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?) """, (self.ticker, self.type, self.date[0], self.date[1],
                                                self.date[2], self.quantity, self.price, self.fees, self.quantity))
        connection.close()

if __name__ == "__main__":
    ...
