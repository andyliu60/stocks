#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import tushare as ts
from ifttt import Notification
from datetime import datetime

class Stock(object):
    
    def __init__(self, stock_f):
        self.stock = stock_f
        self.name = self.stock['name']
        self.symbol = self.stock['symbol']
        self.cost = self.stock['cost']
        
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, stock_data_f):
        self.__price = stock_data_f.close[0]

    @property
    def change(self):
        return self.__change

    @change.setter
    def change(self, stock_data_f):
        self.__change = '%+.2f%%' % round(stock_data_f.pct_chg[0],4)

    @property
    def pchange(self):
        return self.__pchange

    @pchange.setter
    def pchange(self, stock_data_f):
        self.__pchange = round((self.price - self.cost) / self.cost * 100, 2)

token = '27ecfe3c4981fc3d653e9cd70cfedf1e87787d01253f6282706a4e2e'
ifttt_event = 'stock_event'
pro = ts.pro_api(token)
stocks = ({'name':'永辉超市', 'symbol':'601933.SH', 'cost':9.499},{'name':'大华股份', 'symbol':'002236.SZ', 'cost':25.073})
today = datetime.now().day

for stock in stocks:
    mystock = Stock(stock)
    stock_df = pro.daily(ts_code=mystock.symbol)
    mystock.price = stock_df
    mystock.change = stock_df
    mystock.pchange = stock_df
    stock_trade_day = datetime.strptime(stock_df.trade_date[0], '%Y%m%d').day
    print(mystock.name, mystock.symbol, mystock.cost, mystock.price, mystock.change, mystock.pchange)

    if stock_trade_day != today:
        Notification(value1 = mystock.name, value2 = '数据没有更新', event = ifttt_event).sent()
    else:
        Notification(value1 = mystock.name, value2 = '收盘价：%.2f' % mystock.price + ' | ' + '涨跌幅：' + mystock.change + ' |  ' + '盈亏：%+.2f%%' % mystock.pchange, event = ifttt_event).sent()
