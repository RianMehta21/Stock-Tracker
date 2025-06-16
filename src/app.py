""""The GUI for main.py"""
import tkinter as tk

root = tk.Tk()
root.geometry("1000x500")
root.title("Stock Tracker")

input_frame = tk.Frame(root)
input_frame.pack()
input_frame.columnconfigure(0, weight = 1)
input_frame.columnconfigure(1, weight = 1)
input_frame.columnconfigure(2, weight = 1)

options = ["buy", "short", "square off"]
drop_down = tk.OptionMenu(input_frame, tk.StringVar(value="Buy"), *options)
drop_down.grid(row = 0, column = 0)


ticker_input = tk.Entry(input_frame)
ticker_input.grid(row=0, column=1)

submit = tk.Button(input_frame, text = "Submit")
submit.grid(row=0, column=2)

root.mainloop()
