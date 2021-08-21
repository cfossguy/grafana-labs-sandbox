import pandas as pd
import os
import time

from dotenv import load_dotenv
from polygon import RESTClient

# sleep time - for polygon rate limits
sleep_time = 60
load_dotenv()
key = os.environ.get("api-key")

def getFinancialsData(tickers):
    for ticker in tickers:
        with RESTClient(key) as client:
            resp = client.reference_stock_financials(symbol=ticker, type="Q")
            print(resp.__dict__)
        if (tickers.index(ticker)+1) % 5 == 0:
            print(f"sleeping for: {sleep_time} seconds")
            time.sleep(sleep_time)

def getTickerData(tickers):
    ts = pd.Timestamp.today()

    for ticker in tickers:
        # get data for last 5 business days
        for x in range(1, 6):
            bd = pd.tseries.offsets.BusinessDay(n=x)
            pday = (ts - bd).date()

            # RESTClient can be used as a context manager to facilitate closing the underlying http session
            # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
            with RESTClient(key) as client:
                resp = client.stocks_equities_daily_open_close(ticker, pday)
                # resp2 = client.reference_stock_financials(symbol="AAPL", type="Q")
                print(resp.__dict__)
                # print(resp2.__dict__)
        print(f"sleeping for: {sleep_time} seconds")
        time.sleep(sleep_time)

def main():
    tickers = ["SQQQ","SPXU", "BIDU", "HBI", "MRK", "T", "VZ"]
    #tickers = ["T" , "VZ"]
    #getTickerData(tickers)
    getFinancialsData(tickers)

if __name__ == '__main__':
    main()
