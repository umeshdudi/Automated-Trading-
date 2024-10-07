import yfinance as yf
import time
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from config import access_token, accountID

def trading_job():
    client = API(access_token)
    
    # Buy Order
    buy_order = MarketOrderRequest(instrument="EUR_USD", units=1000)
    r = orders.OrderCreate(accountID, data=buy_order.data)
    buy_response = client.request(r)
    print("Buy Order Response:", buy_response)

    # Wait for 5 seconds
    time.sleep(5)

    # Sell Order
    sell_order = MarketOrderRequest(instrument="EUR_USD", units=-1000)  # Sell the same amount
    r = orders.OrderCreate(accountID, data=sell_order.data)
    sell_response = client.request(r)
    print("Sell Order Response:", sell_response)

# Execute trading_job every 5 seconds for 1 minute
start_time = time.time()
while time.time() - start_time < 60:  # Run for 60 seconds
    trading_job()
