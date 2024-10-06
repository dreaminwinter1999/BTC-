import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

btc = yf.download('BTC-USD', start='2019-01-01', end='2024-08-05')
btc.to_csv('BTC-USD.csv')
df = pd.read_csv('BTC-USD.csv')

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

df['dayofweek'] = df.index.dayofweek

df = df[(df['dayofweek'] == 5) | (df['dayofweek'] == 2)]

initial_investment = 1000
cash_closed = 0
cash_high = 0
btc_balance = 0

capital_closed = []
capital_high = []

for i in range(len(df)):
    if df['dayofweek'].iloc[i] == 5:
        btc_to_buy = initial_investment / df['Open'].iloc[i]
        btc_balance += btc_to_buy

    elif df['dayofweek'].iloc[i] == 2:
        cash_from_sale_closed = btc_balance * df['Close'].iloc[i]
        cash_closed += cash_from_sale_closed

        cash_from_sale_high = btc_balance * df['High'].iloc[i]
        cash_high += cash_from_sale_high

        btc_balance = 0

    capital_closed.append(cash_closed)
    capital_high.append(cash_high)

plt.figure(figsize=(10, 6))
dates = df.index[df['dayofweek'] == 2]
capital_closed = capital_closed[:len(dates)]
capital_high = capital_high[:len(dates)]
plt.plot(dates, capital_closed, label='Closed Price Strategy', color='blue')
plt.plot(dates, capital_high, label='High Price Strategy', color='green')
plt.xlabel('Date')
plt.ylabel('Total Capital (USD)')
plt.title('Total Capital Growth Comparison: Closed vs High Price Strategies')
plt.savefig('BTC-USD.png')
plt.legend()
plt.grid(True)
plt.show()

print(f"Final capital with Closed price strategy: {cash_closed:.2f} USD")
print(f"Final capital with High price strategy: {cash_high:.2f} USD")