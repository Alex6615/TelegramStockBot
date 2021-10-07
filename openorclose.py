import time, threading
from stock import *
import time
import datetime


#判斷開盤OR收盤
def OpenorClose():
    today = time.strftime("%Y %a %b %d ", time.localtime())
    #計算開盤的時間戳
    opentime = today + "09:00:00"
    opentimestamp = time.mktime(time.strptime(opentime,"%Y %a %b %d %H:%M:%S"))
    #計算收盤的時間戳
    endtime = today + "13:30:00"
    closetimestamp = time.mktime(time.strptime(endtime,"%Y %a %b %d %H:%M:%S"))
    #目前的時間戳
    now  = time.time()
    if ( opentimestamp <= now <= closetimestamp ) :
        print("盤中")
        return 0
    elif (now < opentimestamp) :
        print("尚未開盤")
        return 1
    else :
        print("已收盤")
        return 2

if __name__ == "__main__" :
    pass