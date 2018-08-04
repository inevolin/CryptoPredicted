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


def init(exchange, symbol, INTERVAL, historymins, currentDateTime):
    currentDateTime = datetime.datetime.strftime(currentDateTime, "%Y-%m-%dT%H:%M")
    url = "http://cryptopredicted.com/api.php?type=exchangeChart&exchange="+exchange+"&symbol="+symbol+"&interval="+str(INTERVAL)+"&historymins="+str(historymins)+"&currentDateTime="+currentDateTime
    print(url)
    out = urllib.request.urlopen(url)
    js = json.loads(out.read().decode(out.info().get_param('charset') or 'utf-8'), object_pairs_hook=collections.OrderedDict)
    return js

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
    

def strategy_sma():

    # this is a basic strategy that uses two SMAs (of different size), and then buys/sells when there is a cross-over between both SMAs.
    
    portfolio = {}

    def buy():
        portfolio[dtit_s]['_buy']=( {'buyprice':lastPrice} )
    def sell():
        portfolio[dtit_s]['_sell']=( {'sellprice':lastPrice} )    

    def isIncreasingArr(arr, historyLen):
        if historyLen > len(arr):
            return False
        if historyLen < 2:
            return False
        i = len(arr) - historyLen + 1
        while i < len(arr):
            if arr[i] <= arr[i-1]:
                return False
            i+=1
        return True

    symbol = 'BTCUSDT'
    historymins = 60*24*5
    dtend = datetime.datetime.strptime('2018-03-13 13:40', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    inp = init('binance', symbol, 1, historymins, dtend)

    canBuy = True
    canSell = False

    incrementMinutes = 1

    maA = []
    sizeA = 40
    maB = []
    sizeB = 100
    bucket = []

    while dtit < dtend:
        #print(dtit)
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}
        idx = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
        if idx in inp:            
            lastPrice = (inp[idx]['open']+inp[idx]['close'])/2
            bucket.append(lastPrice)

            if len(bucket) >= sizeA and len(bucket) >= sizeB:
                avgA = sum(bucket[-sizeA:])/sizeA
                avgB = sum(bucket[-sizeB:])/sizeB

                LB = 10
                if len(maA) >= LB and len(maB) >= LB:
                    a = sum(maA[-LB:])/LB
                    b = sum(maB[-LB:])/LB
                    if b > a and avgA > avgB: # short SMA takes the lead (crossover)
                        buy()
                    elif a > b and avgB > avgA: # long SMA takes the lead (crossover)
                        sell()


                maA.append(avgA)
                maB.append(avgB)

        dtit += datetime.timedelta(minutes=incrementMinutes)

    #print( json.dumps(processPortfolio(portfolio, 0.5, 0.5)) ) # full output json
    print( json.dumps(processPortfolio(portfolio, 0.5, 0.5)['_']) ) # just the summary



def strategy_std():

    # this strategy uses a lagging moving average SMA(t-1) and the StdDev (std) of SMA's window to determine whether to buy/sell/hold for time 't'.
    
    portfolio = {}

    def buy():
        portfolio[dtit_s]['_buy']=( {'buyprice':lastPrice} )
    def sell():
        portfolio[dtit_s]['_sell']=( {'sellprice':lastPrice} )    

    def isIncreasingArr(arr, historyLen):
        if historyLen > len(arr):
            return False
        if historyLen < 2:
            return False
        i = len(arr) - historyLen + 1
        while i < len(arr):
            if arr[i] <= arr[i-1]:
                return False
            i+=1
        return True

    symbol = 'BTCUSDT'
    historymins = 60*24*1
    dtend = datetime.datetime.strptime('2018-03-12 13:40', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    inp = init('binance', symbol, 1, historymins, dtend)

    incrementMinutes = 1

    buck_len = 7
    prepare_to_buy = False
    prepare_to_sell = False
    bucket = []

    while dtit < dtend:
        #print(dtit)
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}
        idx = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
        if idx in inp:            
            recentPrice = (inp[idx]['open']+inp[idx]['close'])/2
            if len(bucket) == buck_len:
                npbuckets = np.array(bucket)
                mean = np.mean(npbuckets)
                std = np.std(npbuckets)

                portfolio[dtit_s]["ap"]= recentPrice
                portfolio[dtit_s]["temp"] = {"mean":mean, "std":std}

                dx = abs(recentPrice-mean)
                if dx >= 1*std and dx < 2*std:
                    pass #print("anomaly of 1 std")
                elif dx >= 2*std and dx < 3*std:
                    pass #print("anomaly of +2 std")
                    if (recentPrice > mean): # price is going up
                        prepare_to_sell = True
                    elif (recentPrice < mean): # price is going down
                        prepare_to_buy = True
                elif dx >= 3*std:
                    pass #print("anomaly of +3 std")
                else:
                    pass #print("all good - stable")
                    if prepare_to_buy:
                        portfolio[dtit_s]['_buy']=( {'buyprice':recentPrice} ) 
                        prepare_to_buy = False
                        
                    if prepare_to_sell:
                        portfolio[dtit_s]['_sell']=( {'sellprice':recentPrice} )    
                        prepare_to_sell = False

                bucket.pop(0)

            bucket.append(recentPrice)

        dtit += datetime.timedelta(minutes=incrementMinutes)

    #print( json.dumps(processPortfolio(portfolio, 0.5, 0.5)) ) # full output json
    print( json.dumps(processPortfolio(portfolio, 1, 1)['_']) ) # just the summary


def strategy_social(dtit, tup):

    # this is a basic strategy that uses two SMAs (of different size), and then buys/sells when there is a cross-over between both SMAs.
    
    portfolio = {}

    def buy():
        portfolio[dtit_s]['_buy']=( {'buyprice':currentPrice} )
    def sell():
        portfolio[dtit_s]['_sell']=( {'sellprice':currentPrice} )    

    def isIncreasingArr(arr, historyLen):
        i = len(arr) - historyLen
        if i < 0:
            return False
        while i < len(arr):
            if arr[i] < arr[i-1]:
                return False
            i+=1
        return True
    def isDecreasingArr(arr, historyLen):
        i = len(arr) - historyLen
        if i < 0:
            return False
        while i < len(arr):
            if arr[i] > arr[i-1]:
                return False
            i+=1
        return True

    def ema_simple(s, n): # simplified version
        ema = []
        multiplier = (2 / float(1 + n))
        ema.append(s[0])
        for i in range(1, len(s)):
            v = (s[i]*multiplier) + (ema[i-1]*(1-multiplier))
            ema.append( v )

        return ema



    incrementMinutes = 1
    bucket_social = []
    bucket_price = []

    while dtit < dtend:
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}
        idx = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
        if idx in inp:            
            currentPrice = (inp[idx]['close'])
            mentionData = inp[idx]['sentiments']['social_delta']
            bucket_social.append(mentionData)
            bucket_price.append(currentPrice)
            if len(bucket_social) >= 2:
                emaSocial = bucket_social
                emaSocial = ema_simple(emaSocial, 10)
                emaSocial = ema_simple(emaSocial, 10)

                emaPrice = bucket_price
                emaPrice = ema_simple(emaPrice, 10)
                emaPrice = ema_simple(emaPrice, 10)


                lxA, lxB, lxC, lxD = tup
                if isIncreasingArr(emaSocial, lxA) and isIncreasingArr(emaPrice, lxB):
                    #print(str(dtit_s) + "\t up \t " + str(isIncreasingArr(emaPrice, 5)) )
                    sell()
                elif isDecreasingArr(emaSocial, lxC) and isDecreasingArr(emaPrice, lxD):
                    #print(str(dtit_s) + "\t down \t " + str(isDecreasingArr(emaPrice, 5)))
                    buy()

            

        dtit += datetime.timedelta(minutes=incrementMinutes)

    
    out =processPortfolio(portfolio, 0.5, 0.5)
    #print( json.dumps(out['_']['%']) ) # just the summary
    return out['_']['%']


#strategy_sma()
#strategy_std()


import threading
class strategy_social_processor (threading.Thread):
    def __init__(self, args, threads, tup, pcts):
        threading.Thread.__init__(self)
        self.tup = tup
        self.args = args
        self.threads = threads
        self.pcts = pcts

    def run(self):
        try:
            pct = strategy_social(*(self.args), self.tup)
            print(str(pct) + "\t\t" + str(self.tup))
            key=round(pct,2)
            if not key in pcts:
                pcts[key] = []
            pcts[key].append(self.tup)
        except Exception as ex:
            print(ex)
            pass
        self.threads.pop(0)


symbol = 'BTCUSDT'
historymins = 60*24*10
dtend = datetime.datetime.strptime('2018-03-21 14:00', '%Y-%m-%d %H:%M')
dtstart = dtend - datetime.timedelta(minutes=historymins)
dtit = dtstart
inp = init('binance', symbol, 60, historymins, dtend)

pcts = {}
threads=[]
try:
    for lxA in range(3, 15):
        for lxB in range(3, 15):
            for lxC in range(3, 15):
                for lxD in range(3, 15):
                    tup = (lxA, lxB, lxC, lxD)
                    
                    th = strategy_social_processor((dtit,), threads, tup, pcts)
                    th.start()
                    threads.append(th)
                    while len(threads) >= 16:
                        time.sleep(.1)
                   
except KeyboardInterrupt:
    pass
except:
    pass

while len(threads) > 0:
    time.sleep(0.1)
print("----------")


import json
with open('pcts.txt', 'w') as file:
     file.write(json.dumps(pcts))
