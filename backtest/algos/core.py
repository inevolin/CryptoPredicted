import sys
sys.dont_write_bytecode = True

import math
import requests
import datetime
import random
import pprint
import sys
import json
import time
import copy
import collections
import urllib.request
from itertools import chain
import copy


def processPortfolio(portfolio, buy_ratio, sell_ratio=1, fee=0.001):

    # Reverse the portfolio order and remove all buys from the end,
    # this ensures our last trade is always a "sell", and if sell_ratio==1 then we can compute a valid ROI.
    # When sell_ratio is smaller than 1, then we won't have a clean exit and incomplete ROI.
    portfolio = collections.OrderedDict(reversed(sorted(portfolio.items())))
    for key, obj in portfolio.items():
        if '_buy' in obj:
            del obj['_buy']
        if '_sell' in obj:
            break
    portfolio = collections.OrderedDict(sorted(portfolio.items()))

    # iterate over dict and calculate profit/loss
    cash_start = 10000
    cash = cash_start
    crypto = 0
    lastBuyPrice = None    

    buytrades = 0
    selltrades = 0
    for key, obj in portfolio.items():
        if '_buy' in obj:
            if cash > 0:
                buyprice = obj['_buy']['buyprice']
                lastBuyPrice = buyprice
                crypto_x = cash*buy_ratio / buyprice
                crypto += crypto_x*(1-fee)
                obj['fee'] = crypto_x*fee
                cash -= cash*buy_ratio
                buytrades += 1
                if '_sell' in obj: del obj['_sell']
            else:
                del obj['_buy']
        
        if '_sell' in obj:
            if crypto > 0: 
                sellprice = obj['_sell']['sellprice']
                cash_x = crypto*sell_ratio * sellprice
                cash += cash_x*(1-fee)
                obj['fee'] = cash*fee
                crypto -= crypto*sell_ratio
                selltrades += 1
                if '_buy' in obj: del obj['_buy']
            else:
                del obj['_sell']

        obj['crypto'] = crypto
        obj['cash'] = cash
        portfolio[key] = collections.OrderedDict(sorted(portfolio[key].items()))

    portfolio['_'] = {
        'cash':cash,
        'margin': cash - cash_start,
        'ROI%': ((cash / cash_start)-1)*100,
        'crypto':crypto,
        'buytrades': buytrades,
        'selltrades': selltrades,
    }
    portfolio = collections.OrderedDict(sorted(portfolio.items()))

    return portfolio

def portfolioPriceEntry(portfolio, dtit, price, open, close, low, high):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    if dtit_s not in portfolio: portfolio[dtit_s] = {}

    portfolio[dtit_s]["ap"]= price # ap = actual price
    portfolio[dtit_s]["open"]= open
    portfolio[dtit_s]["close"]= close
    portfolio[dtit_s]["low"]= low
    portfolio[dtit_s]["high"]= high

def portfolioBuy(portfolio, dtit, buyprice, uncertainty_margin):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    if dtit_s not in portfolio: portfolio[dtit_s] = {}

    portfolio[dtit_s]['_buy']=(
        {
            'buyprice_default':buyprice,
            'buyprice':buyprice*(1+uncertainty_margin)
        }
    )
def portfolioSell(portfolio, dtit, sellprice, uncertainty_margin):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    if dtit_s not in portfolio: portfolio[dtit_s] = {}

    portfolio[dtit_s]['_sell']=(
        {
            'sellprice_default':sellprice,
            'sellprice':sellprice*(1-uncertainty_margin)
        }
    )
def createNewScatterTrace(name, yaxis, mode='lines'):
    return {
    'x':[],
    'y':[],
    'z':[],
    'name': name,
    'mode': mode,
    'yaxis':yaxis}

def addToScatterTrace(trace, dtit, value):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    trace['x'].append(dtit_s)
    trace['y'].append(value)

def getPriceExchange_v1(exchange, interval, base, quote, historymins, _dt):
    _dt = datetime.datetime.strftime(_dt, '%Y-%m-%dT%H:%M')
    url = 'https://cryptopredicted.com/PWA/api/?type=exchange&exchange='+exchange+'&base_cur='+base+'&quote_cur='+quote+'&interval='+str(interval)+'&historymins='+str(historymins)+'&currentDateTime=' + _dt
    print(url)
    response = requests.get(url)
    js = json.loads(response.text , object_pairs_hook=collections.OrderedDict)
    return js
    
def getPredictions_v1(exchange, interval, base, quote, historymins, _dt):
    _dt = datetime.datetime.strftime(_dt, '%Y-%m-%dT%H:%M')
    url = 'https://cryptopredicted.com/PWA/api/predictions/v1/list/?exchange='+exchange+'&base_cur='+base+'&quote_cur='+quote+'&interval='+str(interval)+'&historymins='+str(historymins)+'&currentDateTime=' + _dt+'&mode=production'
    response = requests.get(url)
    js = json.loads(response.text , object_pairs_hook=collections.OrderedDict)
    return js

def portfolioToChart_OHLC(portfolio, traces=[], file="./chart.html", shapes=[]):
    # this will use the portfolio and its _buy/_sell entries to generate an OHLC chart.
    import plotly
    import plotly.plotly as py
    import plotly.graph_objs as go

    opens = []
    highs = []
    lows = []
    closes = []
    dates = []

    annons = []
    
    for key, obj in portfolio.items():
        if key == "_": continue
        # dt = datetime.datetime.strptime(key, '%Y-%m-%d %H:%M') # if you use this, then plotly will display local dates -- but you must parse it everywhere below as well !
        dt = key
        opens.append(obj['open'])
        highs.append(obj['high'])
        lows.append(obj['low'])
        closes.append(obj['close'])
        dates.append( dt )
        if '_buy' in obj:
            annons.append(
                {
                    'x':dt,
                    'y':obj['_buy']['buyprice_default'],
                    'text':"B",
                    'arrowcolor': "black",
                }
            )

        if '_sell' in obj:
            annons.append(
                {
                    'x':dt,
                    'y':obj['_sell']['sellprice_default'],
                    'text':"S",
                    'arrowcolor': "blue",
                }
            )
        
    data = []
    trace = go.Candlestick(x=dates,
                        open=opens,
                        high=highs,
                        low=lows,
                        close=closes,
                        opacity=0.5)
    data.append(trace)

    for t in traces:
        trace = go.Scatter(
            name = t['name'],
            x = t['x'],
            y = t['y'],
            mode = t['mode'],#'lines', # +markers
            yaxis = t['yaxis'],
            connectgaps=True,
        )
        data.append(trace)

    layout = go.Layout(
        shapes = shapes,
        xaxis = dict(
            rangeslider = dict(
                visible = False
            ),
            type = "date",
        ),
        yaxis2= {
            'title': 'y2',
            'overlaying': 'y',
            'side': 'right',
            'showgrid':False,
            'autorange': True,
            'anchor': 'free',
            'position':0
        },
        yaxis3= {
            'title': 'y3',
            'overlaying': 'y',
            'side': 'right',
            'showgrid':False,
            'autorange': True,
            'anchor': 'free',
            'position': 0.3
        },
        yaxis4= {
            'title': 'y4',
            'overlaying': 'y',
            'side': 'right',
            'showgrid':False,
            'autorange': True,
            'anchor': 'free',
            'position': 0.6
        },
        annotations = annons,
       # dragmode = "pan"
    )
    
    fig = go.Figure(data=data,layout=layout)
    config = {'scrollZoom': True}
    plotly.offline.plot(fig, config=config, filename=file)

