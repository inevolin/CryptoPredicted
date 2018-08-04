import datetime
import pprint
import sys
import json
import time
import copy
import collections
import urllib.request
from itertools import chain

import os
os.environ.setdefault('PATH', '') # fix numpy execution from php bug

import numpy as np


def init(crypto, INTERVAL, historymins, currentDateTime):
    currentDateTime = datetime.datetime.strftime(currentDateTime, "%Y-%m-%dT%H:%M")
    url = "http://cryptopredicted.com/api.php?type=predictionChart3&coin="+crypto+"&interval="+str(INTERVAL)+"&historymins="+str(historymins)+"&currentDateTime="+currentDateTime+"&featuresID=-1&batchsize=-1&neurons=-1&windowsize=-1&epochs=1000&hiddenlayers=-1&predicted_feature=price3"
    print(url)
    out = urllib.request.urlopen(url)
    js = json.loads(out.read().decode(out.info().get_param('charset') or 'utf-8'), object_pairs_hook=collections.OrderedDict)
    return js

def actualPrice(dt, curr):
    if dt in curr:
        return curr[dt]
    return None

def strategy_BuyThenSell_minmax(buy_ratio, predictionsARR, curr, interval):
    portfolio = {}

    # let's use min(Predic) to buy and max(Predic) to sell

    for predictions in predictionsARR:
        
        predts_min = min(predictions, key=predictions.get)
        predts_max = max(predictions, key=predictions.get)

        if predts_min == predts_max:
            return # make sure there is at least one prediction and not the same
        
        if not predts_min in portfolio:
            portfolio[predts_min] = {}
        if not predts_max in portfolio:
            portfolio[predts_max] = {}

        if actualPrice(predts_min, curr) == None or actualPrice(predts_max, curr) == None:
            return # make sure we are analyzing predictions for which the actual prices are already known.

        portfolio[predts_min]['_buy']=( {'predicted': predictions[predts_min], 'buyprice':actualPrice(predts_min,curr)} )    
        portfolio[predts_max]['_sell']=( {'predicted': predictions[predts_max], 'sellprice':actualPrice(predts_max,curr)} )   


    return processPortfolio(portfolio, buy_ratio)

def strategy_useFirstPredictionOnly(buy_ratio, predictionsARR, curr, interval):
    portfolio = {}

    # use only first prediction as indicator to make decision in current interval

    for predictions in predictionsARR:
        predts = list(predictions.keys())[0] # only get first one
        predictedval = predictions[predts] # only get first one

        # now get the most recently known price (the one prior to the first prediction)
        curDT = datetime.datetime.strptime(predts, "%Y-%m-%dT%H:%M") - datetime.timedelta(minutes=interval)
        curDT = datetime.datetime.strftime(curDT, "%Y-%m-%dT%H:%M")
        prev_val = actualPrice(curDT, curr)
        
        if not predts in portfolio:
            portfolio[predts] = {}
        if actualPrice(predts,curr) == None:
            return # make sure we are analyzing predictions for which the actual prices are already known.

        if predictedval < prev_val: # buy now
            portfolio[predts]['_buy']=( {'predicted': predictedval, 'buyprice':actualPrice(predts,curr)} )    

        elif predictedval > prev_val: # sell now
            portfolio[predts]['_sell']=( {'predicted': predictedval, 'sellprice':actualPrice(predts,curr)} )    

    return processPortfolio(portfolio, buy_ratio)
        
def processPortfolio(portfolio, buy_ratio, sell_ratio=1):
    # we process/backtest the portfolio and execute the _buy & _sell signals.

    fee = 0.001             # trade fee (e.g.: 0.1% binance)
    cash_start = 10000      # 

    # we must process sorted by time, so lets sort the entire portfolio
    # but we also make sure the last signal in the portfolio is a _sell (never a _buy)
    portfolio = collections.OrderedDict(reversed(sorted(portfolio.items())))
    for key, obj in portfolio.items():
        if '_buy' in obj:
            del obj['_buy']
        if '_sell' in obj:
            break
    portfolio = collections.OrderedDict(sorted(portfolio.items()))

    
    cash = cash_start
    crypto = 0
    lastBuyPrice = None    
    buytrades = 0
    selltrades = 0

    for key, obj in portfolio.items():
        if '_buy' in obj:
            if cash > 0: # can buy ?
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
            if crypto > 0: # can sell ?
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
        '%': ((cash / cash_start)-1)*100,
        'crypto':crypto,
        'buytrades': buytrades,
        'selltrades': selltrades,
    }

    # sort by key
    portfolio = collections.OrderedDict(sorted(portfolio.items()))
    return portfolio
    


import threading
class bt1Processor (threading.Thread):
    def __init__(self, interval, historymins, curDT, predictionsARR, curr):
        threading.Thread.__init__(self)
        self.interval = interval
        self.curDT = curDT
        self.predictionsARR = predictionsARR
        self.curr = curr
        self.historymins = historymins

    def run(self):
        js = init('BTC', self.interval, self.historymins, self.curDT)
        
        for ts, val in js["history"].items():
            if not ts in self.curr:
                self.curr[ts] = val
        for ts, val in js["history_extended"].items():
            if not ts in self.curr:
                self.curr[ts] = val

        for fid, predictions in js['predictions'].items():
            if not fid in self.predictionsARR:
                self.predictionsARR[fid] = []
            self.predictionsARR[fid].append(predictions)    

def processThreadsAwait(threads):
    for t in threads:
        try:
            t.join(timeout=30) # 30 sec per article
        except Exception as ex:
            print(ex)

def backtest1():
    interval = 10
    historymins = 30
    dtstart = datetime.datetime.strptime('2018-02-26 00:00', '%Y-%m-%d %H:%M')
    curDT = dtstart
    predictionsARR = {}
    curr = {}

    # each new datetime step has a different set of predictions
    # to backtest we need to obtain many of these, so lets use multithreading to get them from the server
    # we then merge the results into two dicts: curr (= price data) and predictionsARR (= predictions)
    threads = []
    for J in range(144):
        th = bt1Processor(interval, historymins, curDT, predictionsARR, curr)
        th.start()
        threads.append(th)
        if len(threads) == 25:
            processThreadsAwait(threads)
            threads=[]
        curDT += datetime.timedelta(minutes=10)
    processThreadsAwait(threads)

    curr = collections.OrderedDict(sorted(curr.items(), key=lambda x:x[0])) # sort by key
    portfolios = {}
    for fid, arr in predictionsARR.items():

        # choose one of the available strategies:
        portfolio = strategy_useFirstPredictionOnly(1, arr, curr, interval)
        #portfolio = strategy_BuyThenSell_minmax(1, arr, curr, interval)
        

        if portfolio != None and portfolio["_"] != None:
            portfolios[fid] = portfolio["_"]["%"]

    print(json.dumps( collections.OrderedDict(sorted(portfolios.items())) ))


backtest1()