""""The GUI for main.py"""
import datetime
import tkinter as tk
from tkinter import StringVar, ttk
from data_base import *
from datetime import date


class MyGUI:
    """Contains all GUI related functions"""

    def __innit__(self):
        """Creates the GUI window"""
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("Stock Tracker")

        self.input_frame = tk.Frame(self.root, pady=100)
        self.input_frame.pack()
        for i in range(8):
            self.input_frame.columnconfigure(i, weight=1)

        options = ["BUY", "SHORT", "SELL"]
        self.type_input = StringVar()
        self.type_input.set(options[0])
        self.drop_down = tk.OptionMenu(self.input_frame, self.type_input, *options)
        self.drop_down.grid(row=1, column=0)


        self.ticker_header = tk.Label(self.input_frame, text="Ticker")
        self.ticker_header.grid(row=0, column=1)
        self.quantity_header = tk.Label(self.input_frame, text="Quantity")
        self.quantity_header.grid(row=0, column=2)
        self.price_header = tk.Label(self.input_frame, text="Price")
        self.price_header.grid(row=0, column=3)
        self.fee_header = tk.Label(self.input_frame, text="Fee")
        self.fee_header.grid(row=0,column=4)

        self.ticker_input = ttk.Entry(self.input_frame, width = 10)
        self.ticker_input.grid(row=1, column=1)

        self.quantity_input = ttk.Entry(self.input_frame, width = 10)
        self.quantity_input.grid(row=1, column=2)

        self.price_input = ttk.Entry(self.input_frame, width = 10)
        self.price_input.grid(row=1, column=3)

        self.fee_input = ttk.Entry(self.input_frame, width = 10)
        self.fee_input.grid(row=1, column=4)

        self.submit = ttk.Button(self.input_frame, text="Submit", command=self.submit)
        self.submit.grid(row=1, column=5)

        self.root.mainloop()

    def submit(self):
        """Submits the input in the GUI to the backend"""

        for widget in self.input_frame.grid_slaves():
            if widget.grid_info()["row"] == 2:
                widget.destroy()

        quantity = self.quantity_input.get()
        ticker = self.ticker_input.get()
        type = self.type_input.get()
        price = self.price_input.get()
        fee = self.fee_input.get()

        if not all([quantity, ticker, type, price]):
            tk.Label(self.input_frame, text="Fill all the values", fg = "red", font=('Roboto', 12)).grid(row=2, column=2, columnspan=2)
            return
        else:
            try:
                quantity = float(quantity)
            except ValueError:
                tk.Label(self.input_frame, text="Invalid quantity", fg = "red", font=('Roboto', 12)).grid(row=2, column=2, columnspan=2)
                return
            try:
                price = float(price)
            except ValueError:
                tk.Label(self.input_frame, text="Invalid price", fg = "red", font=('Roboto', 12)).grid(row=2, column=2, columnspan=2)
                return
            try:
                fee = float(fee)
            except ValueError:
                tk.Label(self.input_frame, text="Invalid fee", fg = "red", font=('Roboto', 12)).grid(row=2, column=2, columnspan=2)
        self.ticker_input.delete(0,tk.END)
        self.quantity_input.delete(0,tk.END)
        self.price_input.delete(0,tk.END)
        self.fee_input.delete(0,tk.END)

        today = datetime.date.today()
        date_today = [today.year, today.month, today.day]
        #TODO: fix this
        #transaction = Transaction(ticker, type, date_today, quantity, price, fees, quantity)



gui = MyGUI()
gui.__innit__()
transaction_handler = TransactionHandler()
transaction_handler.create_sql()
transaction_handler.read_data_base()
