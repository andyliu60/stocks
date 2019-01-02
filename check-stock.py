#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import tushare as ts
from ifttt import Notification
from datetime import datetime

token = '27ecfe3c4981fc3d653e9cd70cfedf1e87787d01253f6282706a4e2e'
pro = ts.pro_api(token)
ifttt_event = 'stock_event'

stocks = ({'name':'永辉超市', 'symbol':'601933.SH'},{'name':'大华股份', 'symbol':'002236.SZ'})
today = datetime.now().day

for stock in stocks:
    stock_df = pro.daily(ts_code=stock['symbol'])
    stock_trade_day = datetime.strptime(stock_df.trade_date[0], '%Y%m%d').day

    if stock_trade_day != today:
        Notification(value1 = stock['name'], value2 = '数据没有更新', event = stock['event']).sent()
    else:
        stock_price = stock_df.close[0]
        stock_pchange = '%+.2f%%' % round(stock_df.pct_chg[0],4)
        Notification(value1 = stock['name'], value2 = '收盘价：%.2f' % stock_price + ' | ' + '涨跌幅：' + stock_pchange, event = ifttt_event).sent()
