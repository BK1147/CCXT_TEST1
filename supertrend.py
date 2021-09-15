

"""
Calculation of values as per formula

Basic UPPERBAND = (HIGH+LOW)/2 + Multiplier*ATR
Basic LOWERBAND = (HIGH+LOW)/2 - Multiplier*ATR

The Average True Range(ATR) formula
TR = MAX[ (H-L), ABS(H-Cp), ABS(L - Cp) ]
ATR = (1/n) Sigma(TR_i)
"""
def calculate_true_range(df):
    print("Calculate True range")
    df['Previous_close'] = df['Close'].shift(1)
    df['High-Low'] = df['High'] - df['Low']
    df['High-PC'] = abs(df['High']-df['Previous_close'])
    df['Low-PC'] = abs(df['Low']-df['Previous_close'])
    TR = df[['High-Low','High-PC','Low-PC']].max(axis=1)
    return TR

def get_atr(df,period=10):
    print("Calculate average true range")
    df['TR'] = calculate_true_range(df)
    the_atr = df['TR'].rolling(period).mean()
    return the_atr

def supertrend(df,period=14,multiplier=3):
    print("Calculate the Supertrend")
    df['ATR'] = get_atr(df,period=period)
    df['upperband']= ((df['High']+df['Low'])/2) + (multiplier*df['ATR'])
    df['lowerband']= ((df['High']+df['Low'])/2) - (multiplier*df['ATR'])

    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current -1

        if df['Close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['Close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            # the spot where upper$lower bands are flat
            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]
            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df

def get_moving_avg (df,period=5):
    print("Caculate the Moving average for period {}".format(period))
    df['Moving_AVG_line'] = df['Close'].rolling(period).mean()
    return df

def check_buy_sell_signals(df):
    print("checking for buys and sell")
    print(df.tail(20))
    last_row_index = len(df.index)-1
    previous_row_index = last_row_index-1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("Changed to uptrend, buy")
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        print("Changed to downtrend, sell")

