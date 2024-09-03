from ib_insync import *

# Connect to IBKR TWS running on the same machine
ib = IB()

def find_futures_contract(symbol):
    contracts = ib.reqMatchingSymbols(symbol)
    for contract in contracts:
        print(contract)

def check_market_data_availability():
    try:
        # Connect to TWS on localhost (127.0.0.1) and port 7497
        ib.connect('127.0.0.1', 7497, clientId=1)
        print("Successfully connected to TWS")

        # Check the correct contract for futures
        find_futures_contract('ES')

        # Define a list of various contracts to check for market data
        contracts = [
            Stock('AAPL', 'SMART', 'USD'),
            Stock('MSFT', 'SMART', 'USD'),
            Future(conId=11004968, exchange='GLOBEX'),  # Specify both conId and exchange
            Option('AAPL', '20240621', 150, 'C', 'SMART')
        ]

        for contract in contracts:
            # Request live market data
            ib.reqMarketDataType(1)  # 1 for live, 3 for delayed
            ticker = ib.reqMktData(contract)
            ib.sleep(2)  # Wait for data to be returned
            print(f"Market data for {contract.symbol} ({contract.secType}): {ticker.marketPrice()}")

            # Request delayed market data
            ib.reqMarketDataType(3)  # 1 for live, 3 for delayed
            ticker = ib.reqMktData(contract)
            ib.sleep(2)  # Wait for data to be returned
            print(f"Delayed market data for {contract.symbol} ({contract.secType}): {ticker.marketPrice()}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ib.disconnect()

# Run the market data availability check
check_market_data_availability()