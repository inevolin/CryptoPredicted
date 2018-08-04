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

    if crypto > 0: # if sell_ratio < 1 then there is a chance of unsold cryptos, let's sell them at last available price
        sellprice = obj['_sell']['sellprice']
        cash_x = crypto* 1 * sellprice
        cash += cash_x*(1-fee)
        obj['fee'] = cash*fee
        crypto -= crypto*1
        selltrades += 1
        portfolio[key]['*S*'] = True

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
    

def ema_corr(s, n):
    s = np.array(s)
    ema = []
    j = 1

    sma = sum(s[:n]) / n # calculate average of first 'n' values
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j += 1
        ema.append(tmp)

    return ema

def ema_simple(s, n): # simplified version
    ema = []
    multiplier = (2 / float(1 + n))

    ema.append(s[0])
    for i in range(1, len(s)):
        v = (s[i]*multiplier) + (ema[i-1]*(1-multiplier))
        ema.append( v )

    return ema


def calcEMAdata(js):
    dataArray = []
    OCs = []
    MIN = None
    MAX = None
    for key, obj in js.items():
        OC = (obj['open'] + obj['close'])/2
        if MIN==None or OC < MIN: MIN = OC
        if MAX==None or OC > MAX: MAX = OC
        OCs.append(OC)

        newObj = dict(obj)
        newObj['label'] = key
        dataArray.append(newObj)

    a = 7
    b = 24
    A = ema_simple(OCs, a)
    B = ema_simple(OCs, b)

    for i, _ in enumerate(A):
        A[i] = (A[i]-MIN)/(MAX-MIN)*100
        B[i] = (B[i]-MIN)/(MAX-MIN)*100

    dvs = []
    MIN = None
    MAX = None
    for i, _ in enumerate(A):
        dv = (A[i]-B[i])
        dvs.append(dv)
        if MIN==None or dv < MIN: MIN = dv
        if MAX==None or dv > MAX: MAX = dv
    #for i, _ in enumerate(dvs):
    #    dvs[i] = (dvs[i]-MIN)/(MAX-MIN)

    return (dataArray, A, B, dvs)


def strategy_brute_mthreaded():

    def buy(portfolio,dtit_s,recentPrice):
        portfolio[dtit_s]['_buy']=( {'buyprice':recentPrice} )
    def sell(portfolio, dtit_s,recentPrice):
        portfolio[dtit_s]['_sell']=( {'sellprice':recentPrice} )    

    symbol = 'BTCUSDT'
    historymins = 60*24*1
    dtend = datetime.datetime.strptime('2018-03-17 16:10', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    inp = init('binance', symbol, 1, historymins, dtend)

    import random
    def calc(incrementMinutes, dtit, dtend):
        portfolio = {}
        while dtit < dtend:
            dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if dtit_s not in portfolio:
                portfolio[dtit_s] = {}
            idx = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
            if idx in inp:            
                recentPrice = (inp[idx]['open']+inp[idx]['close'])/2
                portfolio[dtit_s]["ap"]= recentPrice

                rand = random.randint(0, 100)
                if rand >= 0 and rand < 10:
                    buy(portfolio, dtit_s, recentPrice)
                elif rand >= 10 and rand < 20:
                    sell(portfolio, dtit_s, recentPrice)

            dtit += datetime.timedelta(minutes=incrementMinutes)

        process = processPortfolio(portfolio, 1, 1)
        return process


    import threading
    class evalProcessor (threading.Thread):
        def __init__(self, threads, storage, tuple):
            threading.Thread.__init__(self)
            self.storage = storage
            self.tuple = tuple

        def run(self):
            print(self)
            val = calc(*self.tuple)
            
            if len(storage) < 10:
                storage.append(val)
            else:
                smallest = None
                smallestIdx = None
                for i, x in enumerate(storage):
                    if smallest == None || x['_']['%'] < smallest:
                        smallest = x['_']['%']
                        smallestIdx = i
                if val['_']['%'] > smallest:
                    storage[smallestIdx] = val

            if len(threads) > 0:
                threads.pop(0)
            



    incrementMinutes = 1
    buck_len = 5
    emaShortLen = 15
    emaLongLen = 50

    
    import time

    threads = []
    vals = []

    tup = (1, dtit, dtend)
    th = evalProcessor(threads, vals, tup)
    th.start()
    threads.append(th)
    while len(threads) >= 16:
        time.sleep(.1)


    smallest = None
    bestTop = None
    for x in vals:
        if smallest == None or x['val'] < smallest:
            smallest = x['val']
            bestTop = x['tup']
    print(smallest)
    print(bestTop)

#strategy_std_mthreaded()

def distribution_strictIncrease():
    dtend = datetime.datetime.strptime('2018-03-16 13:40', '%Y-%m-%d %H:%M')
    js = init('binance', 'BTCUSDT', 1, 60000, dtend)
    dataArray, A, B, dvs = calcEMAdata(js)

    # let's count the length of non-stop strictly rising (descending) bars
    # todo descending -

    prev = None
    dist = {}
    count = 0
    for x in dvs:
        if prev != None:
            if x > prev and prev > 0: # > 0 is increasing strictly only
                count += 1
            elif count > 0:
                if not count in dist:
                    dist[count] = 0
                dist[count]+=1
                count = 0

        prev = x

    from pprint import pprint
    pprint(dist)

    # count      amount      relative = amount/sum(all amount)  [calculated in excel]
    # 1          305         21,08%
    # 2          253         17,48%
    # 3          178         12,30%
    # 4          177         12,23%
    # 5          141         9,74%
    # 6          102         7,05%
    # 7          80          5,53%
    # 8          59          4,08%
    # 9          62          4,28%
    # 10          26         1,80%
    # 11          22         1,52%
    # 12          12         0,83%
    # 13          12         0,83%
    # 14          7          0,48%
    # 15          2          0,14%
    # 16          4          0,28%
    # 17          2          0,14%
    # 18          2          0,14%
    # 23          1          0,07%

    # 21% of increases happen just for one interval
    # 17% two steps
    # ...
            
def testDurationBuyToSellDuration_strictIncrease():
    dtend = datetime.datetime.strptime('2018-03-16 13:40', '%Y-%m-%d %H:%M')
    js = init('binance', 'BTCUSDT', 1, 60000, dtend)
    dataArray, A, B, dvs = calcEMAdata(js)

    # let's wait until there is a crossover in the histogram to enter "buy"
    # and  then wait until a local maximum has been reached, when so, sell immediately after that max's interval

    prev = None
    wait = 0
    crossover = False
    waits = {}
    for i, x in enumerate(dvs):
        if prev != None:
            
            if crossover:
                if x > prev:
                    wait += 1
                else: # max is 'prev', so we are one past max -- lets record and reset states
                    if not wait in waits:
                        waits[wait] = {'x': 0, 'r' : 0}
                    waits[wait]['x'] += 1
                    wait = 0
                    crossover = False

            if prev < 0 and x > 0: # cross-over
                # now we can start counting until we reach a max
                wait += 1
                crossover = True

        prev = x
    
    tot = 0
    for i,w in waits.items():
        tot += w['x']
    for i,w in waits.items():
        w['r'] = round(w['x']/tot*100,4)
    from pprint import pprint
    pprint(waits)


    # {1: {'r': 9.3537, 'x': 55},
    # 2: {'r': 11.3946, 'x': 67},
    # 3: {'r': 14.1156, 'x': 83},
    # 4: {'r': 12.585, 'x': 74},
    # 5: {'r': 12.415, 'x': 73},
    # 6: {'r': 10.7143, 'x': 63},
    # 7: {'r': 7.3129, 'x': 43},
    # 8: {'r': 5.7823, 'x': 34},
    # 9: {'r': 5.102, 'x': 30},
    # 10: {'r': 5.102, 'x': 30},
    # 11: {'r': 1.1905, 'x': 7},
    # 12: {'r': 1.5306, 'x': 9},
    # 13: {'r': 0.6803, 'x': 4},
    # 14: {'r': 1.3605, 'x': 8},
    # 15: {'r': 0.5102, 'x': 3},
    # 16: {'r': 0.3401, 'x': 2},
    # 17: {'r': 0.1701, 'x': 1},
    # 19: {'r': 0.1701, 'x': 1},
    # 24: {'r': 0.1701, 'x': 1}}

    # only in 9% of the cases there is a strictly non-increasing local maximum
    # in 14% of the cases it takes 3 intervals before such a maximum is reached
    # however, reaching this point does not mean it's the real local maximum, it's just the first consecutive non-increasing interval


def testDurationBuyToSellDuration_untilThreshold():
    
    cumulRoi = 1

    dtend = datetime.datetime.strptime('2018-03-11 23:00', '%Y-%m-%d %H:%M')
    js = init('binance', 'BTCUSDT', 1, 60*24*1, dtend)
    cumulRoi *= testDurationBuyToSellDuration_untilThreshold_help(js)

    print("******")
    print(cumulRoi*100)

    # cumulRoi = 1
    # for i in range (24):
    #     dtend = datetime.datetime.strptime('2018-03-16 '+str(i)+':00', '%Y-%m-%d %H:%M')
    #     js = init('binance', 'BTCUSDT', 1, 60, dtend)
    #     cumulRoi *= testDurationBuyToSellDuration_untilThreshold_help(js)

    # print("******")
    # print(cumulRoi*100)

    # when using a large range (e.g. 7 days) and then doing EMA on that range, the STDs will be much lower
    # so instead I run the calculations within a window of 24 hours that slides by 24 hour steps.
    # in reality however, we have a sliding window that ought to be updated in real-time (streaming API from Binance)

    # but even then the window is limited in size,
    # what if we make an entry 'buy' but never reach the threshold within the size of the window -- so it could leave us with a negative exit

def testDurationBuyToSellDuration_untilThreshold_help(js):
    
    dataArray, A, B, dvs = calcEMAdata(js)

    # let's wait until there is a crossover in the histogram to enter "buy"
    # and  then wait until we reach the first bar of size X

    n_dvs = np.array(dvs)
    std = np.std(n_dvs)
    #X = 3*std
    X=2.3*std

    prev = None
    wait = 0
    crossover = False
    waits = {}
    i_buy = 0
    ROIs = []
    trades = 0
    minutes = 0

    buyPrice = None
    sellPrice = None
    for i, x in enumerate(dvs):
        minutes += 1
        if prev != None:
            if crossover:
                if (x < X) and (wait > 0 and wait < 120): # we can also wait until we can make 1% or so, in addition to looking at STD of the MACD
                    wait += 1
                else: # max is 'prev', so we are one past max -- lets record and reset states
                    if not wait in waits:
                        waits[wait] = {'x': 0, 'r' : 0}
                    waits[wait]['x'] += 1


                    # sellPrice = (dataArray[i]['low'])
                    sellPrice = (dataArray[i]['open']+dataArray[i]['close'])/2

                    if sellPrice > buyPrice :

                        print("sell: " + dataArray[i]['label'] + " for " + str(dataArray[i]['open']))

                        fee = 0.001
                        ROI = (sellPrice*(1-fee))/(buyPrice*(1+fee))
                        #print("ROI: " + str(ROI))
                        ROIs.append(ROI)
                        trades += 1

                        wait = 0
                        crossover = False

                        buyPrice = None
                        sellPrice = None

            if not crossover and prev < 0 and x > 0: # cross-over
                # now we can start counting until we reach a max
                wait += 1
                crossover = True
                i_buy = i

                #buyPrice = (dataArray[i_buy]['high'])
                buyPrice = (dataArray[i_buy]['open']+dataArray[i_buy]['close'])/2
                print("buy: " + dataArray[i_buy]['label'] + " for " + str(dataArray[i_buy]['open']))
                sellPrice = None

            
        prev = x

    if buyPrice != None and sellPrice == None:
        ROIs.append(-1)
    
    tot = 0
    for i,w in waits.items():
        tot += w['x']
    for i,w in waits.items():
        w['r'] = round(w['x']/tot*100,4)
    from pprint import pprint
    pprint(waits)

    if len(ROIs) > 0:
        print("avg roi:" + str(sum(ROIs)/len(ROIs)) + " %")

    cumulRoi = 1
    for r in ROIs:
        cumulRoi *= r
    print("cumul roi:" + str(cumulRoi*100) + " %")
    
    print("trades:" + str(trades))
    print("#mintues: " + str(minutes) )
    
    return cumulRoi

    

#distribution_strictIncrease()
#testDurationBuyToSellDuration_strictIncrease()
#testDurationBuyToSellDuration_untilThreshold()