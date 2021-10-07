import os
import threading
from multiprocessing import Process
import time
import json
from typing import Counter
import yfinance as yf
#from openorclose import OpenorClose
from decimal import Decimal
from queue import Queue



def KGetStock(stocknum):
    global flag
    global q
    while flag == 1 :
        #print(f"num : {stocknum} flag = {flag}")
        try :
            x = GetQueue(q)
            print(x)
            stock = yf.Ticker(f"{stocknum}.TW")
            hist = stock.history(period="max")
            time.sleep(2)
            result = hist.iloc[[-1],[3]].to_json()
            result = json.loads(result)['Close']
            result = list(result.values())[0]
            result = float(Decimal(result).quantize(Decimal("0.00")))
            #print(f"{stocknum} : {result}")
            #print(result)
            q.put(result)
        except :
            result = 1
    return result


def counter(sec=15):
    global flag
    time_left = int(sec)
    while time_left > 0:
        print('倒计时(s):',time_left)
        time.sleep(1)
        time_left = time_left - 1

def GetQueue(q):
    if q.empty() == True :
        time.sleep(1)
        return "NULL"
    else :
        time.sleep(1)
        return q.get()

def job(x):
    print("Thread", x)
    x = x + 1
    time.sleep(1)


    

#========================================================================#
if __name__ == "__main__" :

    q = Queue(maxsize=0)
    #倒數的秒數 
    sec = 15
    #控制迴圈
    flag = 1

    #多行程
    p = Process(target=counter, args=(sec,))
    p.start()
    
    #多執行緒
    target = ["2330", "0056","00878", "0050"]
    threads = []
    for i,j in zip(target, range(0,len(target))) :
        threads.append(threading.Thread(target = KGetStock, args = (i,)))
        print(f"{i} thread start. ")
        threads[j].start()
    
    
    #將flag 變 0 中斷 getstock 的 while loop
    p.join()
    flag = 0
    print('Child process end.')
    
    for i in threads :
        i.join()
        print(f"{i} thread end. ")
#========================================================================#