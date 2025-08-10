# Stock Tracker

A desktop app to track stock purchases, shorts, and calculate profits in real time using Yahoo Finance data.

## Features
- Add buy or short transactions
- Track remaining shares
- See profit/loss in real time
- Store data locally in SQLite
- Simple GUI with Tkinter

## Installation
1. Clone this repository:
```bash
git clone https://github.com/RianMehta21/stock-tracker.git
cd stock-tracker
```
2. Install dependencies:
```commandline
pip install -r requirements.txt
```

3. Run the progam
```commandline
python app.py
```

## Screenshots

### Input Transaction Tab
Form for recording new **BUY** or **SHORT** trades.
![Input tab](images/input_page.png)

### Portfolio Tab
Displays active positions with real-time prices and profit/loss.
![Portfolio tab](images/portfolio_page.png)
