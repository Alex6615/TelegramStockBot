import threading
import time
from queue import Queue
import yfinance as yf
import json

def GetStock(stocknum, q):
    stock = yf.Ticker(f"{stocknum}.TW")
    hist = stock.history(period="max")
    result = hist.iloc[[-1],[3]].to_json()
    result = json.loads(result)['Close']
    result = list(result.values())[0]
    q.put(result)
    return result

'''
# 子執行緒的工作函數
def job():
  for i in range(5):
    print("Child thread:", i)
    time.sleep(1)

# 建立一個子執行緒
t = threading.Thread(target = job)

# 執行該子執行緒
t.start()

# 主執行緒繼續執行自己的工作
for i in range(3):
  print("Main thread:", i)
  time.sleep(1)

# 等待 t 這個子執行緒結束
t.join()

print("Done.")
'''

liststock  =  ['0056', '2330']

switch = 0
q = Queue()


# 子執行緒類別
class MyThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        global switch
        switch = switch + 1
        count = 0
        while switch >= 0 : 
            #print("child Thread", f"{self.num}" + f"--{count}")
            x = GetStock(str(self.num), q)
            #print(f"NUM:{self.num}---now is---{x}, count = {count}")
            count = count + 1
            print(q.get())
            time.sleep(1)
        
            

# 建立 len(liststock) 個子執行緒
threads = []
for i in range(len(liststock)):
    threads.append(MyThread(liststock[i]))
    x = threads[i].start()
    
# 主執行緒繼續執行自己的工作
# ...


# 等待所有子執行緒結束
for i in range(len(liststock)):
    threads[i].join()


print("Done.")