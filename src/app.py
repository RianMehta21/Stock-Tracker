""""The GUI for main.py"""
import datetime
import tkinter as tk
from tkinter import StringVar, ttk
from typing import Optional

from data_base import *
from datetime import date


class MyGUI:
    """Contains all GUI related functions"""

    def __init__(self):
        """Creates the GUI window and transaction handler"""
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("Stock Tracker")

        style = ttk.Style()
        style.layout("TNotebook", [])
        style.configure("TNotebook", highlightbackground="#848a98", tabmargins=0)

        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.input_frame = tk.Frame(self.notebook, pady=100,padx=200)
        self.portfolio_frame = tk.Frame(self.notebook, pady=100, padx=200)

        self.notebook.add(self.input_frame, text="INPUT TRANSACTION")
        self.notebook.add(self.portfolio_frame, text="PORTFOLIO")

        self.transaction_handler = TransactionHandler()
        self.transaction_handler.create_sql()
        self.create_input_page()

        self.root.mainloop()

    def on_tab_change(self, _):
        """refresh portfolio page on tab click"""
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:
            self.create_portfolio_page()

    def create_input_page(self):
        """Sets up the input tab"""
        for i in range(6):
            self.input_frame.columnconfigure(i, weight=1)

        options = ["BUY", "SHORT", "SELL"]
        self.type_input = StringVar()
        self.type_input.set(options[0])
        self.drop_down = tk.OptionMenu(self.input_frame, self.type_input, *options)
        self.drop_down.grid(row=1, column=0, sticky="ew")


        self.ticker_header = tk.Label(self.input_frame, text="Ticker")
        self.ticker_header.grid(row=0, column=1)
        self.quantity_header = tk.Label(self.input_frame, text="Quantity")
        self.quantity_header.grid(row=0, column=2)
        self.price_header = tk.Label(self.input_frame, text="Price")
        self.price_header.grid(row=0, column=3)
        self.fee_header = tk.Label(self.input_frame, text="Fee")
        self.fee_header.grid(row=0,column=4)

        self.ticker_input = ttk.Entry(self.input_frame, width = 10)
        self.ticker_input.grid(row=1, column=1, sticky="ew")

        self.quantity_input = ttk.Entry(self.input_frame, width = 10)
        self.quantity_input.grid(row=1, column=2, sticky="ew")

        self.price_input = ttk.Entry(self.input_frame, width = 10)
        self.price_input.grid(row=1, column=3, sticky="ew")

        self.fee_input = ttk.Entry(self.input_frame, width = 10)
        self.fee_input.grid(row=1, column=4, sticky="ew")

        self.root.bind("<KeyRelease>", self.submit)
        self.submit = ttk.Button(self.input_frame, text="Submit", command=self.submit)
        self.submit.grid(row=1, column=5, sticky="ew")

    def create_portfolio_page(self):
        """Sets up the portfiolio tab"""
        for i in range(1):
            self.input_frame.columnconfigure(i, weight=0)

        active_list = tk.Listbox(self.portfolio_frame, width=800)
        active_list.grid(row=1, column=0, sticky="nsew")
        for stock in self.transaction_handler.get_active_stocks():
            active_list.insert(tk.END, stock)


    def submit(self, event = None):
        """Submits the input in the GUI to the backend"""
        if event:
            if event.keysym != "Return" or self.notebook.index(self.notebook.select()) != 0:
                return
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
                return
        if quantity <= 0 or price <= 0 or fee< 0:
            tk.Label(self.input_frame, text="Quantity, price, and fee should be positive", fg = "red", font=('Roboto', 12)).grid(row=2, column=1, columnspan=4)
            return

        self.ticker_input.delete(0,tk.END)
        self.quantity_input.delete(0,tk.END)
        self.price_input.delete(0,tk.END)
        self.fee_input.delete(0,tk.END)

        today = datetime.date.today()
        date_today = [today.year, today.month, today.day]
        transaction = Transaction(ticker, type, date_today, quantity, price, fee, quantity)
        self.transaction_handler.upload_transaction(transaction)


gui = MyGUI()
