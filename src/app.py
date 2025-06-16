""""The GUI for main.py"""
import tkinter as tk
from tkinter import StringVar, ttk
import data_base


class MyGUI:
    """Contains all GUI related functions"""

    def __innit__(self):
        """Creates the GUI window"""
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("Stock Tracker")

        self.input_frame = tk.Frame(self.root, pady=100)
        self.input_frame.pack()
        for i in range(5):
            self.input_frame.columnconfigure(i, weight=1)

        self.header = tk.Label(self.input_frame, text="Ticker")
        self.header.grid(row=0, column=1)
        self.header = tk.Label(self.input_frame, text="Quantity")
        self.header.grid(row=0, column=2)
        self.header = tk.Label(self.input_frame, text="Price")
        self.header.grid(row=0, column=3)

        options = ["BUY", "SHORT", "SELL"]
        self.type = StringVar()
        self.type.set(options[0])
        self.drop_down = tk.OptionMenu(self.input_frame, self.type, *options)
        self.drop_down.grid(row=1, column=0)

        self.ticker_input = ttk.Entry(self.input_frame)
        self.ticker_input.grid(row=1, column=1)

        self.quantity_input = ttk.Entry(self.input_frame)
        self.quantity_input.grid(row=1, column=2)

        self.price_input = ttk.Entry(self.input_frame)
        self.price_input.grid(row=1, column=3)

        self.submit = ttk.Button(self.input_frame, text="Submit", command=self.submit)
        self.submit.grid(row=1, column=4)

        self.root.mainloop()

    def submit(self):
        """Submits the input in the GUI to the backend"""

        for widget in self.input_frame.grid_slaves():
            if widget.grid_info()["row"] == 2:
                widget.destroy()

        quantity = self.quantity_input.get()
        ticker = self.ticker_input.get()
        type = self.type.get()
        price = self.price_input.get()

        if not all([quantity, ticker, type, price]):
            tk.Label(self.input_frame, text="Fill all the values", fg = "red", font=('Helvetica', 12)).grid(row=2, column=2)
        else:
            try:
                quantity = int(quantity)
            except ValueError:
                tk.Label(self.input_frame, text="Invalid quantity input", fg = "red", font=('Helvetica', 12)).grid(row=2, column=2)
                return
            try:
                price = float(price)
            except ValueError:
                tk.Label(self.input_frame, text="Invalid price input", fg = "red", font=('Helvetica', 12)).grid(row=2, column=2)
                return


gui = MyGUI()
gui.__innit__()
