""""The GUI for main.py"""
import datetime
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox

from platformdirs.windows import get_win_folder

from data_base import *


class MyGUI:
    """Contains all GUI related functions"""

    def __init__(self):
        """Creates the GUI window and transaction handler"""
        self.root = tk.Tk()
        self.root.geometry("1250x600")
        self.root.title("Stock Tracker")

        style = ttk.Style()
        style.layout("TNotebook", [])
        style.configure("TNotebook", highlightbackground="#848a98", tabmargins=0)

        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.input_frame = tk.Frame(self.notebook, pady=100,padx=200)
        self.portfolio_frame = tk.Frame(self.notebook, pady=100, padx=50)

        self.notebook.add(self.input_frame, text="INPUT TRANSACTION")
        self.notebook.add(self.portfolio_frame, text="PORTFOLIO")

        self.finance = Finance()
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

        options = ["BUY", "SHORT"]
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

        self.root.bind("<Return>", self.submit)
        self.submit = ttk.Button(self.input_frame, text="Submit", command=self.submit)
        self.submit.grid(row=1, column=5, sticky="ew")

    def create_portfolio_page(self):
        """Sets up the portfiolio tab"""
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()
        self.active_table = ttk.Treeview(self.portfolio_frame,
                                    columns = ('id','ticker', 'quantity', 'price', 'current_price', 'net'),
                                    show = 'headings', selectmode=tk.BROWSE)
        self.active_table.heading('ticker', text='Ticker')
        self.active_table.heading('quantity', text='Quantity')
        self.active_table.heading('price', text='Cost Price')
        self.active_table.heading('current_price', text='Current Price')
        self.active_table.heading('net', text='Profit/Loss')

        self.active_table.column('ticker', width=120, anchor=tk.W, stretch=True)
        self.active_table.column('quantity', width=150, anchor=tk.CENTER, stretch=True)
        self.active_table.column('price', width=150, anchor=tk.CENTER, stretch=True)
        self.active_table.column('current_price', width=150, anchor=tk.CENTER, stretch=True)
        self.active_table.column('net', width=200, anchor=tk.CENTER, stretch=True)

        self.active_table["displaycolumns"] = ['ticker', 'quantity', 'price', 'current_price', 'net']

        self.active_table.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.portfolio_frame.columnconfigure(0, weight=1)
        self.portfolio_frame.rowconfigure(0, weight=1)

        quantity_text = "Enter quantity: "
        self.sell_quantity_input = ttk.Entry(self.portfolio_frame, width = 10, foreground="grey")
        self.sell_quantity_input.insert(0, quantity_text)
        self.sell_quantity_input.grid(row=3, column = 1, sticky = "e")

        price_text = "Enter price: "
        self.sell_price_input = ttk.Entry(self.portfolio_frame, width = 10, foreground="grey")
        self.sell_price_input.insert(0, price_text)
        self.sell_price_input.grid(row=3, column = 2, sticky = "e")

        def on_click(_, placeholder_text, widget) -> None:
            """
                Changes the input text to white so that it is easier for user to see what they are typing.
            """
            if widget.get() == placeholder_text:
                widget.delete(0, tk.END)
                widget.configure(foreground="white")

        def on_focus_out(_, placeholder_text, widget) -> None:
            """
                Changes the input text to gray again after checking that there is no possible input.
            """
            if widget.get() == "":
                widget.insert(0, placeholder_text)
                widget.configure(foreground="grey")

        self.sell_quantity_input.bind("<FocusIn>", lambda event: on_click(event, quantity_text, self.sell_quantity_input))
        self.sell_quantity_input.bind("<FocusOut>", lambda event: on_focus_out(event, quantity_text, self.sell_quantity_input))
        self.sell_price_input.bind("<FocusIn>", lambda event: on_click(event, price_text, self.sell_price_input))
        self.sell_price_input.bind("<FocusOut>", lambda event: on_focus_out(event, price_text, self.sell_price_input))

        self.sell_button = tk.Button(self.portfolio_frame, text="Sell", command = self.sell, fg="green")
        self.sell_button.grid(row=3, column = 3, sticky = "ew")

        self.active_table.bind("<BackSpace>", self.delete)
        self.delete_button = tk.Button(self.portfolio_frame, text="Delete", command = self.delete, fg="red")
        self.delete_button.grid(row=4, column=3)

        self.error_label = tk.Label(self.portfolio_frame, text="", fg="red", font=('Roboto', 12))
        self.error_label.grid(row = 4, column = 1, columnspan=2, sticky = "ew")

        for stock in self.transaction_handler.get_active_stocks():
            curr_price = self.finance.get_current_price(stock.ticker)
            gain = self.finance.calculate_profit(stock, curr_price)
            gain_str = '$' + str(gain) if gain > 0 else "-$" + str(abs(gain))
            if stock.type == "SHORT":
                quantity = (-1)*stock.remaining
            else:
                quantity = stock.remaining
            table_entry = (stock.id, stock.ticker, quantity, "$"+str(stock.price), "$"+str(curr_price), gain_str)
            item_id=self.active_table.insert(parent='', index = tk.END, values=table_entry)

            color = 'green' if gain > 0 else 'red'
            self.active_table.tag_configure(color, foreground=color)
            self.active_table.item(item_id, tags=color)

    def sell(self, _=None):
        """sells selected transaction"""
        focused = self.active_table.focus()
        if focused == "":
            self.error_label.configure(text="Select from table")
            return
        details = self.active_table.item(focused)
        sell_id = details["values"][0]

        sell_quantity = self.sell_quantity_input.get()
        sell_price = self.sell_price_input.get()

        try:
            sell_quantity = round(float(sell_quantity), 1)
        except ValueError:
            self.error_label.configure(text="Invalid quantity")
            return
        if sell_quantity <= 0:
            self.error_label.configure(text="Invalid quantity")
            return

        remaining = self.transaction_handler.get_remaining(sell_id)
        if remaining < sell_quantity:
            self.error_label.configure(text="Quantity exceeds available shares")
            return

        try:
            sell_price = round(float(sell_price), 1)
        except ValueError:
            self.error_label.configure(text="Invalid price")
            return
        if sell_price <= 0:
            self.error_label.configure(text="Invalid price")
            return

        self.transaction_handler.sell_transaction(sell_id, sell_quantity)
        self.create_portfolio_page()


    def delete(self, _=None):
        """deletes selected transaction"""
        if self.notebook.index(self.notebook.select()) != 1:
            return

        focused = self.active_table.focus()
        if focused == "":
            self.error_label.configure(text="Select from table")
            return
        if focused and tk.messagebox.showwarning(message='Are you sure you want to delete this transaction.'
                                                         '\nThis action cannot be undone!',
                                                        type=tk.messagebox.YESNO) == 'yes':
            details = self.active_table.item(focused)
            id = details['values'][0]
            self.transaction_handler.delete_transaction(id)
            self.create_portfolio_page()

    def submit(self, _=None):
        """Submits the input in the GUI to the backend"""
        if self.notebook.index(self.notebook.select()) != 0:
            return
        for widget in self.input_frame.grid_slaves():
            if widget.grid_info()["row"] == 2:
                widget.destroy()

        quantity = self.quantity_input.get()
        ticker = self.ticker_input.get()
        type = self.type_input.get()
        price = self.price_input.get()
        fee = self.fee_input.get()

        if not all([quantity, ticker, type, price, fee]):
            (tk.Label(self.input_frame, text="Fill all the values", fg = "red", font=('Roboto', 12))
             .grid(row=2, column=0, columnspan=6, sticky="nsew"))
            return
        elif not self.finance.check_ticker(ticker):
            (tk.Label(self.input_frame, text="Invalid ticker (Use country code suffix and check "
                                             "Yahoo Finance for accurate codes)", fg="red", font=('Roboto', 12))
             .grid(row=2, column=0, columnspan=6, sticky="nsew"))
            return
        else:
            try:
                quantity = round(float(quantity), 1)
            except ValueError:
                (tk.Label(self.input_frame, text="Invalid quantity", fg = "red", font=('Roboto', 12))
                 .grid(row=2, column=0, columnspan=6, sticky="nsew"))
                return
            try:
                price = float(price)
            except ValueError:
                (tk.Label(self.input_frame, text="Invalid price", fg = "red", font=('Roboto', 12))
                 .grid(row=2, column=0, columnspan=6, sticky="nsew"))
                return
            try:
                fee = float(fee)
            except ValueError:
                (tk.Label(self.input_frame, text="Invalid fee", fg = "red", font=('Roboto', 12))
                 .grid(row=2, column=0, columnspan=6, sticky="nsew"))
                return
        if quantity <= 0 or price <= 0 or fee< 0:
            (tk.Label(self.input_frame, text="Quantity, price, and fee should be positive", fg = "red", font=('Roboto', 12))
             .grid(row=2, column=0, columnspan=6, sticky="nsew"))
            return

        self.ticker_input.delete(0,tk.END)
        self.quantity_input.delete(0,tk.END)
        self.price_input.delete(0,tk.END)
        self.fee_input.delete(0,tk.END)

        today = datetime.date.today()
        date_today = [today.year, today.month, today.day]

        fee_weighted_price = round((price * quantity + fee) / quantity, 2)
        transaction = Transaction(ticker, type, date_today, quantity, fee_weighted_price, quantity)
        self.transaction_handler.upload_transaction(transaction)


gui = MyGUI()
