#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import place_order,send_to_telegram,get_signal,get_signal_fast
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

apiToken = os.getenv("API_TOKEN")
chatID = os.getenv("CHAT_ID")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# 逐一檢查環境變數是否正確載入
print("API_TOKEN:", os.getenv("API_TOKEN"))
print("CHAT_ID:", os.getenv("CHAT_ID"))
print("API_KEY:", os.getenv("API_KEY"))
print("API_SECRET:", os.getenv("API_SECRET"))

client = Client(api_key=api_key,api_secret=api_secret)

pair='DOGEUSDT'
freq = '15m'
n_bar = 10000
n1 = 65
n2 = 95
quantity = 100


if __name__ == '__main__':

    side,n1,n2,price = get_signal_fast(pair,freq,n_bar,client,n1,n2)

    message = f"交易對:{pair}\n當前價格:{price}\n多空:{side}\n雙均線參數: n1 {n1} n2 {n2}\n現在時間:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(message)
    send_to_telegram(message,apiToken,chatID)
        
    if side != 'PASS':
        order_result = place_order(symbol=pair,side='SELL',client=client,quantity = quantity)
        print(order_result)
        send_to_telegram(f'執行下單函數結果:{order_result}\n',apiToken,chatID)
