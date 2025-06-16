""""The GUI for main.py"""
import tkinter as tk
from tkinter import StringVar, ttk

root = tk.Tk()
root.geometry("1000x500")
root.title("Stock Tracker")

input_frame = tk.Frame(root)
input_frame.pack()
for i in range(5):
    input_frame.columnconfigure(i, weight = 1)

header = tk.Label(input_frame, text = "Ticker")
header.grid(row = 0, column = 1)
header = tk.Label(input_frame, text = "Quantity")
header.grid(row = 0, column = 2)
header = tk.Label(input_frame, text = "Price")
header.grid(row = 0, column = 3)

options = ["BUY", "BUY", "SHORT", "SELL"]
drop_down = ttk.OptionMenu(input_frame, StringVar(value = "BUY"), *options)
drop_down.grid(row = 1, column = 0)

ticker_input = ttk.Entry(input_frame)
ticker_input.grid(row=1, column=1)

quantity_input = ttk.Entry(input_frame)
quantity_input.grid(row=1, column=2)

price_input = ttk.Entry(input_frame)
price_input.grid(row=1, column=3)

submit = ttk.Button(input_frame, text = "Submit")
submit.grid(row=1, column=4)

root.mainloop()
