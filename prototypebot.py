import easyquotation
from telegram.ext import Updater, CommandHandler
import json

quotation = easyquotation.use('sina')

def add(update, context):
    code = ''.join(context.args)
    with open('stocks.json', 'r') as f:
        stocks = json.load(f)
        f.close()

    if code in stocks:
        context.bot.send_message(chat_id=update.effective_chat.id, text='列表中已有本支股票')
        return
    stocks.append(code)
    with open('stocks.json', 'w') as f:
        f.write(json.dumps(stocks))
        f.close()


def delete(update, context):
    code = ''.join(context.args)
    with open('stocks.json', 'r') as f:
        stocks = json.load(f)
        f.close()
    if code in stocks:
        stocks.remove(code)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='列表中里没有该支股票，无需删除')

    with open('stocks.json', 'w') as f:
        f.write(json.dumps(stocks))
        f.close()


def price(update, context):
    with open('stocks.json', 'r') as f:
        stocklist = json.load(f)
        f.close()
    pricestr=''
    for code in stocklist:
        pricestr+=f"{code}:{quotation.real(code)[code]['now']}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=pricestr)

def list(update,context):
    with open('stocks.json', 'r') as f:
        stocklist = json.load(f)
        f.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(stocklist))


if __name__ == '__main__':
    updater = Updater('1974376870:AAFS8m2TVLC_ozDpwmo3GNzXYVAwIxXABv4')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('delete', delete))
    dispatcher.add_handler(CommandHandler('price', price))
    dispatcher.add_handler(CommandHandler('list', list))
    updater.start_polling()
