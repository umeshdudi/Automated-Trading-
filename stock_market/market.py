import yfinance as yf
import pandas as pd

dataF = yf.download("EURUSD=X", start="2024-09-15", end="2024-10-4", interval='15m')
dataF.iloc[:,:]
#dataF.Open.iloc


def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]
    
    # Bearish Pattern
    if (open>close and 
    previous_open<previous_close and 
    close<previous_open and
    open>=previous_close):
        return 1

    # Bullish Pattern
    elif (open<close and 
        previous_open>previous_close and 
        close>previous_open and
        open<=previous_close):
        return 2
    
    # No clear pattern
    else:
        return 0

signal = []
signal.append(0)
for i in range(1,len(dataF)):
    df = dataF[i-1:i+1]
    signal.append(signal_generator(df))
#signal_generator(data)
dataF["signal"] = signal

dataF.signal.value_counts()
#dataF.iloc[:, :]


from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails



access_token= '66aa1f73bfe89df64e5fd82e2ec2824f-0f1a8c6590e150e540b2232f94bd334d'
accountID = '001-001-12631774-001'
def get_candles(n):
    access_token= '66aa1f73bfe89df64e5fd82e2ec2824f-0f1a8c6590e150e540b2232f94bd334d'
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o))>1)



import oandapyV20.exceptions as oanda_exceptions

def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open', 'Close', 'High', 'Low'])

    for i, candle in enumerate(candles):
        dfstream.loc[i] = [float(str(candle.bid.o)),
                           float(str(candle.bid.c)),
                           float(str(candle.bid.h)),
                           float(str(candle.bid.l))]

    signal = signal_generator(dfstream.iloc[:-1, :])
    
    client = API(access_token)
    
    SLTPRatio = 2.0
    previous_candleR = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])
    
    SLBuy = dfstream['Open'].iloc[-1] - previous_candleR
    SLSell = dfstream['Open'].iloc[-1] + previous_candleR

    TPBuy = dfstream['Open'].iloc[-1] + previous_candleR * SLTPRatio
    TPSell = dfstream['Open'].iloc[-1] - previous_candleR * SLTPRatio

    print(dfstream.iloc[:-1, :])
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)

    # Only use the generated signal here
    if signal == 1:  # Sell
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000,
                                 takeProfitOnFill=TakeProfitDetails(price=TPSell).data,
                                 stopLossOnFill=StopLossDetails(price=SLSell).data)
    elif signal == 2:  # Buy
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000,
                                 takeProfitOnFill=TakeProfitDetails(price=TPBuy).data,
                                 stopLossOnFill=StopLossDetails(price=SLBuy).data)
    else:
        print("No trading signal.")
        return

    try:
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    except oanda_exceptions.V20Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

trading_job()

#scheduler = BlockingScheduler()
#scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2022-01-12 12:00:00', timezone='America/Chicago')
#scheduler.start()


