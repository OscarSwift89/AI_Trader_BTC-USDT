import ccxt
import pandas as pd

exchange = ccxt.okx()
symbol = 'BTC/USDT'
timeframe = '1d'
since = exchange.parse8601('2023-01-01T00:00:00Z')
all_bars = []

# OKX单次最多只能取100根K线，所以要循环获取
done = False
while not done:
    bars = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=100)
    if not bars:
        break
    all_bars += bars
    if len(bars) < 100:
        done = True
    else:
        since = bars[-1][0] + 24 * 60 * 60 * 1000  # 下一天

df = pd.DataFrame(all_bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df.to_csv('btc_okx_2023_1d.csv')
print(df.head()) 