from utils import place_order,send_to_telegram,get_signal,get_signal_fast
import time
import os
from datetime import datetime

if __name__ == '__main__':
    while True:# 持續執行
        side,n1,n2 = get_signal_fast() # 取得交易訊號
        時間 = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 時間
        print('''
 /\_/\  
( o   o )
=(  =^=  )=
 (        )
  (      )
''')
        print(f'<比特幣自動交易程序> side:{side} n1:{n1} n2:{n2} current_time:{時間}') #打印信息
        
        if side != 'PASS': # 判斷是否出現方向
            send_to_telegram(message=side)# 發送電報
            place_order(side) # 根據訊號方向下單
        time.sleep(60*15) # 等15分鐘出現下一根k棒
        os.system("cls") # 清除屏幕
