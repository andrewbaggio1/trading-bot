#### PLACE MARKET ORDER OF NVDA STOCK ####
"""
from ib_insync import *
import time

# Connect to IBKR TWS or Gateway
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Use 7496 for TWS, 7497 for Gateway

# Define the contract for Nvidia stock
nvidia_contract = Stock('NVDA', 'SMART', 'USD')

# Define a market order to buy Nvidia stock
order = MarketOrder('BUY', 1)  # Change the quantity as needed

# Place the order
trade = ib.placeOrder(nvidia_contract, order)

# Wait for the order to be filled
while not trade.isDone():
    ib.sleep(1)

print(f'Order Status: {trade.orderStatus.status}')
print(f'Filled Quantity: {trade.orderStatus.filled}')
print(f'Average Fill Price: {trade.orderStatus.avgFillPrice}')

# Disconnect from IBKR
ib.disconnect()
"""

#### PRINT SUBSCRIPTION DATA ####

from ib_insync import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Initialize IB connection
ib = IB()

def connect_to_ibkr():
    try:
        ib.connect('127.0.0.1', 7497, clientId=1)
        logging.info("Successfully connected to TWS")
    except Exception as e:
        logging.error(f"Connection error: {e}")
        raise

def fetch_cme_depth_of_book(symbol='ES'):
    try:
        contract = Future(symbol, '202406', 'GLOBEX')
        ib.qualifyContracts(contract)
        ticker = ib.reqMktDepth(contract, numRows=5)
        ib.sleep(2)
        print(f"CME Depth of Book for {symbol}:")
        for entry in ticker.domBids:
            print(f"Bid: {entry.size} @ {entry.price}")
        for entry in ticker.domAsks:
            print(f"Ask: {entry.size} @ {entry.price}")
    except Exception as e:
        logging.error(f"Error fetching CME Depth of Book for {symbol}: {e}")

def fetch_us_securities_snapshot(symbol='AAPL'):
    try:
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        ticker = ib.reqMktData(contract, '', False, False)
        ib.sleep(2)
        print(f"US Securities Snapshot for {symbol}:")
        print(f"Last Price: {ticker.last}")
        print(f"Bid: {ticker.bid}")
        print(f"Ask: {ticker.ask}")
        print(f"Volume: {ticker.volume}")
    except Exception as e:
        logging.error(f"Error fetching US Securities Snapshot for {symbol}: {e}")

def fetch_nasdaq_totalview(symbol='AAPL'):
    try:
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        ticker = ib.reqMktDepth(contract, numRows=5)
        ib.sleep(2)
        print(f"NASDAQ TotalView for {symbol}:")
        for entry in ticker.domBids:
            print(f"Bid: {entry.size} @ {entry.price}")
        for entry in ticker.domAsks:
            print(f"Ask: {entry.size} @ {entry.price}")
    except Exception as e:
        logging.error(f"Error fetching NASDAQ TotalView for {symbol}: {e}")

def main():
    try:
        connect_to_ibkr()
        fetch_cme_depth_of_book()
        fetch_us_securities_snapshot()
        fetch_nasdaq_totalview()
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        ib.disconnect()

if __name__ == '__main__':
    main()