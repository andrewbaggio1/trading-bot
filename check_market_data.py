from ib_insync import *
import time

# Connect to IBKR TWS running on the same machine
ib = IB()

def check_market_data_availability():
    try:
        # Connect to TWS on localhost (127.0.0.1) and port 7497
        ib.connect('127.0.0.1', 7497, clientId=1)
        print("Successfully connected to TWS")

        # Define a sample contract to request market data
        contracts = [
            Stock('AAPL', 'SMART', 'USD'),
            Stock('MSFT', 'SMART', 'USD')
        ]

        for contract in contracts:
            # Request market data type (live or delayed)
            ib.reqMarketDataType(1)  # 1 for live, 3 for delayed
            ticker = ib.reqMktData(contract)
            ib.sleep(2)  # Wait for data to be returned
            print(f"Market data for {contract.symbol}: {ticker.marketPrice()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ib.disconnect()

# Run the market data availability check
check_market_data_availability()