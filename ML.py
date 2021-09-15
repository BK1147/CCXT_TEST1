from sklearn.linear_model import LinearRegression
import ta

def linear_regression(df):
    lm = LinearRegression()
    X = df[['RSI']]
    Y = df[['Close']]

    lm.fit(X,Y)

    Yhat = lm.predict(X)

    return Yhat



def calculate_RSI(df,period=14):
    rsi = ta.momentum.rsi(df['Close'])
    return rsi

