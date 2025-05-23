from utils import place_order,send_to_telegram,get_signal,get_signal_fast
import time
import os
from datetime import datetime
from binance.client import Client

# API SETTING
apiToken = "5850662274:AAGeKZqM1JfQfh3CrSKG6BZ9pEvDajdBUqs"
chatID = "1567262377"
api_key = "hGo9QzLRDRzHknp820Npo480n62A5dEjOTBt3HXfddNrIuBXvHuibmuGcKor3b1l"
api_secret = "1TNlq4E0ZWSvD1odE15r6uL0yRNWPiOQRr1BDifMiSpJraNIqCLLcdWhWqJJHQuL" 
client = Client(api_key=api_key,api_secret=api_secret)

# TRADING SETTING
pair='DOGEUSDT'
freq = '15m'
n_bar = 10000
n1 = 65
n2 = 95
quantity = 100

# MAIN
if __name__ == '__main__':
    while True:

        side,n1,n2,price = get_signal_fast(pair,freq,n_bar,client,n1,n2)

        message = f"交易對:{pair}\n當前價格:{price}\n多空:{side}\n雙均線參數: n1 {n1} n2 {n2}\n現在時間:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(message)
        send_to_telegram(message,apiToken,chatID)
        
        if side != 'PASS':
            order_result = place_order(symbol=pair,side='SELL',client=client,quantity = quantity)
            print(order_result)
            send_to_telegram(f'執行下單函數結果:{order_result}\n',apiToken,chatID)
        
        time.sleep(60*15) 
        os.system("cls")
