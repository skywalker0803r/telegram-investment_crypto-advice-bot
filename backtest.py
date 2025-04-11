import backtrader as bt
import pandas as pd
import ccxt
import datetime

# 1. 設定 Binance API 連接
exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# 2. 抓取歷史 K 線資料
def fetch_binance_ohlcv(symbol='BTC/USDT', timeframe='1d', limit=100):
    # 抓取 K 線資料
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')  # 轉換時間戳為 datetime
    df.set_index('datetime', inplace=True)  # 設定 datetime 為索引
    return df[['open', 'high', 'low', 'close', 'volume']]

# 策略定義
class SMACross(bt.Strategy):
    def __init__(self):
        # 定義兩條簡單移動平均線（SMA）
        self.sma1 = bt.indicators.SMA(self.data.close, period=10)  # 10日SMA
        self.sma2 = bt.indicators.SMA(self.data.close, period=30)  # 30日SMA

    def next(self):
        # 進行買賣操作
        if not self.position:  # 如果目前沒有持倉
            if self.sma1[0] > self.sma2[0]:  # 當短期SMA上穿長期SMA
                self.buy()
        elif self.sma1[0] < self.sma2[0]:  # 如果短期SMA下穿長期SMA
            self.sell()

# 從 CSV 載入市場數據
df = fetch_binance_ohlcv(symbol='BTC/USDT', timeframe='1d', limit=1000)  # 可調整符號和時間範圍

# 將資料轉換成 Backtrader 可用的格式
data = bt.feeds.PandasData(dataname=df)

# 建立回測引擎
cerebro = bt.Cerebro()

# 添加策略到引擎
cerebro.addstrategy(SMACross)

# 添加資料
cerebro.adddata(data)

# 設定初始資金
cerebro.broker.setcash(100000)

# 執行回測
print(f'初始資金: {cerebro.broker.getvalue():.2f}')
cerebro.run()
print(f'最終資金: {cerebro.broker.getvalue():.2f}')

# 顯示回測結果圖
cerebro.plot()

