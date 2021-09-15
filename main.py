# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import ML


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import supertrend

import ccxt
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import schedule
import time

import warnings
warnings.filterwarnings('ignore')


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


exchange = ccxt.binanceus()

# command+b to go to the function info
# DOGE = exchange.fetch_ohlcv("DOGE/USD", timeframe='4h', limit=100)
# df = pd.DataFrame(DOGE, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volumn'])
# df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

def run_bot():
    print(f"Fetching new bar for {datetime.datetime.now().isoformat()}")
    DOGE = exchange.fetch_ohlcv("DOGE/USD", timeframe='1h', limit=300)
    df = pd.DataFrame(DOGE, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volumn'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df['RSI'] = ML.calculate_RSI(df)
    #df['TESTING'] = ML.linear_regression(df)

    supertrend_data = supertrend.supertrend(df)
    supertrend.check_buy_sell_signals(supertrend_data)
    print("**************************************")

schedule.every(5).seconds.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)


