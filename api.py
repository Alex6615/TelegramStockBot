import queue
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
#This is a good time to set up the logging module, so you will know when (and why) things don't work as expected:
import logging
from stock import *
import threading
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token='1974376870:AAFS8m2TVLC_ozDpwmo3GNzXYVAwIxXABv4', use_context=True)

#For quicker access to the Dispatcher used by your Updater, you can introduce it locally:
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def cmds(update, context):
    textlist = ['/start', '/caps 輸入字串都轉換成大寫', '/sadd 加入目標號碼', '/sdel 移除目標號碼', '/list 查看目前目標', '/wloop 無窮迴圈測試', '/getstock 查看目標價格' ]
    for x in textlist :
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{x}")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

#-----------------------------------------------------------------------------

liststock  =  ['2330','0056']

def sdel(update, context):
    print("stock delete")
    global liststock
    targets = context.args
    for target in targets :
        liststock.remove(target)


def sadd(update, context):
    print("stock add")
    global liststock
    targets = context.args
    for target in targets :
        liststock.append(target)


def showlist(update, context):
    print("showlist")
    output = "目前追蹤的股票："
    for stock in liststock :
        output = output + f"\n{stock}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)    


def wloop(update, context):
    text_caps = "-----------------------------"
    while 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def GetStockPrice(update, context):
    result = ""
    for i in liststock:
        print(i)
        p = GetStock(i)
        gapfive = Gapfive(i)
        gapten = Gapten(i)
        gaptwenty = Gaptwenty(i)
        if (abs(gapfive) <= 2 or abs(gapten) <= 2 or abs(gaptwenty) <= 2) :
            
            if abs(gapfive) <= 2 :
                result = result + "--------------" + "\n" + "No.: "+ i + ";  Price : " + str(p) + "\n" + "五日:" + str(gapfive) + "\n"
            elif abs(gapten) <= 2 :
                result = result + "--------------" + "\n" + "No.: "+ i + ";  Price : " + str(p) + "\n" + "五日:" + str(gapten) + "\n"
            elif abs(gaptwenty) <= 2 :
                result = result + "--------------" + "\n" + "No.: "+ i + ";  Price : " + str(p) + "\n" + "五日:" + str(gaptwenty) + "\n"
            '''
            result = result + "--------------" + "\n" + "No.: "+ i + ";  Price : " + str(p) + "\n" + "五日:" + str(gapfive) + "\n" + "十日:" + str(gapten) + "\n" + "二十日:" + str(gaptwenty) + "\n" + "--------------" + "\n"
            '''
        else :
            result = result + "No.: "+ i + ";  Price : " + str(p) + "\n"
    text_caps = f"Result: \n{result}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def PollingStock(update, context):
    pass


    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

cmds_handler = CommandHandler('cmds', cmds)
dispatcher.add_handler(cmds_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

#移除目標股票
#輸入 /sdel
sdel_handler = CommandHandler('sdel', sdel)
dispatcher.add_handler(sdel_handler)

#添加目標股票
#輸入 /sadd
sadd_handler = CommandHandler('sadd', sadd)
dispatcher.add_handler(sadd_handler)

#列出目前追蹤的股票
#輸入 /list
list_handler = CommandHandler('list', showlist)
dispatcher.add_handler(list_handler)

#無窮迴圈測試
#輸入 /wloop
wloop_handler = CommandHandler('wloop', wloop)
dispatcher.add_handler(wloop_handler)

#獲取儲存列表的價位
#輸入 /getstock
getstock_handler = CommandHandler('getstock', GetStockPrice)
dispatcher.add_handler(getstock_handler)

#持續查詢儲存列表的價位
#輸入 /getstock
poll_handler = CommandHandler('poll', PollingStock)
dispatcher.add_handler(poll_handler)



updater.start_polling()
