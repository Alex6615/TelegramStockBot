import decimal
import requests as req
import pandas as pd
import yfinance as yf
import time
import json
import threading
from queue import Queue
from decimal import Decimal


def GetStock(stocknum):
    try :
        stock = yf.Ticker(f"{stocknum}.TW")
        hist = stock.history(period="max")
        result = hist.iloc[[-1],[3]].to_json()
        result = json.loads(result)['Close']
        result = list(result.values())[0]
        result = Decimal(result).quantize(Decimal("0.00"))
        return float(result)
    except :
        return 0


#取週平均
def Stockfive(stocknum):
    try :
        stock = yf.Ticker(f"{stocknum}.TW")
        hist = stock.history(period="max")
        #print(hist)
        result = hist.iloc[-5:,-4].to_json()
        result = json.loads(result)
        result = list(result.values())
        #print(result)
        #result = json.loads(result)['Close']
        #result = list(result.values())[0]
        avg = 0
        temp = 0
        for res in result :
            temp = temp + float(res)
        avg = temp / len(result)
        avg = Decimal(avg).quantize(Decimal("0.00"))
        return float(avg)
       
    except :
        return 0

#取10日平均
def Stockten(stocknum):
    try :
        stock = yf.Ticker(f"{stocknum}.TW")
        hist = stock.history(period="max")
        #print(hist[-10:])
        result = hist.iloc[-10:,-4].to_json()
        result = json.loads(result)
        result = list(result.values())
        
        #result = json.loads(result)['Close']
        #result = list(result.values())[0]
        avg = 0
        temp = 0
        for res in result :
            temp = temp + Decimal(res)
        avg = temp / len(result)
        avg = Decimal(avg).quantize(Decimal("0.00"))
        return float(avg)
       
    except :
        return 0

#取20日平均
def Stocktwenty(stocknum):
    try :
        stock = yf.Ticker(f"{stocknum}.TW")
        hist = stock.history(period="max")
        #print(hist[-10:])
        result = hist.iloc[-20:,-4].to_json()
        result = json.loads(result)
        result = list(result.values())
        #result = json.loads(result)['Close']
        #result = list(result.values())[0]
        avg = 0
        temp = 0
        for res in result :
            temp = temp + Decimal(res)
        avg = temp / len(result)
        avg = Decimal(avg).quantize(Decimal("0.00"))
        return float(avg)
       
    except :
        return 0

#5日差距
def Gapfive(stocknum):
    p = GetStock(stocknum)
    five = Stockfive(stocknum)
    result  = p - five
    result = Decimal(result).quantize(Decimal("0.00"))
    return float(result)

#10日差距
def Gapten(stocknum):
    p = GetStock(stocknum)
    ten = Stockten(stocknum)
    result  = p - ten
    result = Decimal(result).quantize(Decimal("0.00"))
    return float(result)

#20日差距
def Gaptwenty(stocknum):
    p = GetStock(stocknum)
    twenty = Stocktwenty(stocknum)
    result  = p - twenty
    result = Decimal(result).quantize(Decimal("0.00"))
    return float(result)





if __name__ == "__main__" :
    print("---teststart----")

    