import os
import threading
from multiprocessing import Process
import time
import json
from typing import Counter
import yfinance as yf
from openorclose import OpenorClose
from decimal import Decimal
#from stock import GetStock

def GetStock(stocknum):
    global flag
    
    while flag == 1 :
        print(f"num : {stocknum} flag = {flag}")
        try :
            stock = yf.Ticker(f"{stocknum}.TW")
            hist = stock.history(period="max")
            time.sleep(5)
            result = hist.iloc[[-1],[3]].to_json()
            result = json.loads(result)['Close']
            result = list(result.values())[0]
            result = float(Decimal(result).quantize(Decimal("0.00")))
            print(result)
        except :
            result = 1
    return result



def counter(sec):
    global flag
    time_left = sec
    while time_left > 0:
        print('倒计时(s):',time_left)
        time.sleep(1)
        time_left = time_left - 1

        


def job(x):
    print("Thread", x)
    x = x + 1
    time.sleep(1)

#========================================================================
if __name__ == "__main__" :
     
    #倒數的秒數 
    sec = 15
    #控制迴圈
    flag = 1
    p = Process(target=counter, args=(sec,))
    p.start()
    
    target = ["2330", "0056","00878", "0050"]
    threads = []
    for i,j in zip(target, range(0,len(target))) :
        threads.append(threading.Thread(target = GetStock, args = (i,)))
        threads[j].start()
        
    p.join()
    #將flag 變 0 中斷 getstock 的 while loop
    flag = 0
    print('Child process end.')
    
    for i in threads :
        i.join()
    