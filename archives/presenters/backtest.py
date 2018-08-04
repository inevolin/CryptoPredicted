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

import os
os.environ.setdefault('PATH', '') # fix numpy execution from php bug
import sys
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/')
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/presenters/')
from mysettings import dtNow
import DAL

import numpy as np

def init(crypto, INTERVAL, currentDateTime):
    currentDateTime = datetime.datetime.strftime(currentDateTime, "%Y-%m-%dT%H:%M")
    url = "http://cryptopredicted.com/api.php?type=predictionChart3&coin="+crypto+"&interval="+str(INTERVAL)+"&historymins=180&currentDateTime="+currentDateTime+"&featuresID=-1&batchsize=-1&neurons=-1&windowsize=-1&epochs=1000&hiddenlayers=-1&predicted_feature=price3"
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
    fee = 0.001
    # we must process sorted by time
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
        #obj['ap'] = actualPrice(key,curr)
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
    
def adjustDatetime(interval, currentDateTime):
    if interval <= 60:
        return currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % interval), second=0, microsecond=0) #"2018-01-26T12:00"
    else: 
        return currentDateTime.replace(hour=currentDateTime.hour-(currentDateTime.hour % int(interval/60)), minute=currentDateTime.minute-(currentDateTime.minute % 60), second=0, microsecond=0) #"2018-01-26T12:00"


import threading
class bt1Processor (threading.Thread):
    def __init__(self, interval, curDT, predictionsARR, curr):
        threading.Thread.__init__(self)
        self.interval = interval
        self.curDT = curDT
        self.predictionsARR = predictionsARR
        self.curr = curr

    def run(self):
        js = init('BTC', self.interval, self.curDT)
        
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
    out = {}
    dtstart = datetime.datetime.strptime('2018-02-26 00:00', '%Y-%m-%d %H:%M')
    curDT = dtstart
    predictionsARR = {}
    curr = {}
    threads = []
    for J in range(144):
        th = bt1Processor(interval, curDT, predictionsARR, curr)
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
        #portfolio = strategy_useFirstPredictionOnly(1, arr, curr, interval)
        portfolio = strategy_BuyThenSell_minmax(1, arr, curr, interval)
        if portfolio != None and portfolio["_"] != None:
            portfolios[fid] = portfolio["_"]["%"]

    print(json.dumps( collections.OrderedDict(sorted(portfolios.items())) ))


def getPriceData(coin, interval, historymins, _dt):
    try:
        currentDateTime = _dt.replace(second=0,microsecond=0) #- timedelta(minutes=interval)
        currentDateTime = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % interval))
        currentDateTime_T = datetime.datetime.strftime(currentDateTime, '%Y-%m-%dT%H:%M')
        print(str(currentDateTime_T))
        import currencyFilter as cm
        curr = cm.main([' ', coin, str(interval), historymins, currentDateTime_T ])
        return curr
    except KeyboardInterrupt:
        raise
    except:
        return None

def getPriceDataExchange(exchange, base, quote, historymins, _dt):
    try:
        currentDateTime = _dt.replace(second=0,microsecond=0) #- timedelta(minutes=interval)
        currentDateTime_T = datetime.datetime.strftime(currentDateTime, '%Y-%m-%dT%H:%M')
        #print(str(currentDateTime_T))
        import exchangeFilter as cm
        curr = cm.main([' ', exchange, symbol, historymins, currentDateTime_T ])
        return curr
    except KeyboardInterrupt:
        raise
    except Exception as ex:
        print(ex)
        return None

def getPriceExchange_v1(exchange, interval, base, quote, historymins, _dt):
    _dt = datetime.datetime.strftime(_dt, '%Y-%m-%dT%H:%M')
    url = 'https://cryptopredicted.com/PWA/api/?type=exchange&exchange='+exchange+'&base_cur='+base+'&quote_cur='+quote+'&interval='+str(interval)+'&historymins='+str(historymins)+'&currentDateTime=' + _dt
    response = requests.get(url)
    js = json.loads(response.text , object_pairs_hook=collections.OrderedDict)
    return js

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def portfolioToImage(portfolio):
    # https://stackoverflow.com/questions/8409095/matplotlib-set-markers-for-individual-points-on-a-line

    plt.clf() # clear all
    fig, ax2 = plt.subplots()

    data = []
    for ts, obj in portfolio.items():
        if 'ap' in obj:
            data.append(obj['ap'])

    ax2.set_ylabel('price')
    ax2.plot(data, color='black', marker='o', alpha=0.8) # wild guesses

    #############
    #max_tick = len(xpolated[0][concat_graph:])
    #ax1.xaxis.set_ticks(np.arange(len(dataset[concat_graph:, 1]), max_tick, 1))
    #ax2.xaxis.set_ticks(np.arange(len(dataset[concat_graph:, 1]), max_tick, 1))

    #ax2.xaxis.set_ticks(np.arange(0, 53, 1))
    ax2.xaxis.grid(True) # horiz.

    fig.set_size_inches((len(data)*0.3), 8, forward=True)
    _path = '../ui/temp/images/'+str(dtNow()) + '_(0)__' + 'backtesting.png'

    plt.savefig(_path, bbox_inches='tight', dpi=100, format='png') # auto-resize bbox_inches='tight'


def backtest2_AnomalyDetection():
    
    portfolio = {}

    interval = 2
    avg_len = 15
    coin = "BTC"
    historymins = 60*24*1
    dtend = datetime.datetime.strptime('2018-03-10 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    inp = getPriceData(coin, interval, historymins, dtend)

    prepare_to_buy = False
    prepare_to_sell = False

    incrementMinutes = 2
    while dtit < dtend:
        print(dtit)
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}
        fts = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
        idx = next((i for i, item in enumerate(inp) if item['label'] == fts), -1)
        if (idx == -1 or idx+1 < avg_len):
            dtit += datetime.timedelta(minutes=incrementMinutes)
            continue
        
        avgs = []
        for j in range(avg_len):
            if inp[idx-j-1]['avg'] != None:
                avgs.append(inp[idx-j-1]['avg'])
        last = inp[idx]['avg']
        if last==None:
            dtit += datetime.timedelta(minutes=incrementMinutes)
            continue
        print(avgs)
        
        avgs = np.array(avgs)
        mean = np.mean(avgs)
        std= np.std(avgs)
        print((mean, std, last))
        
        
        portfolio[dtit_s]["ap"]= last

        dx = abs(last-mean)
        if dx >= 1*std and dx < 2*std:
            print("anomaly of 1 std")
            # if prepare_to_buy:
            #     portfolio[dtit_s]['_buy']=( {'buyprice':last} )    
            #     prepare_to_buy = False
            # if prepare_to_sell:
            #     portfolio[dtit_s]['_sell']=( {'sellprice':last} )    
            #     prepare_to_sell = False

            # if (last > mean):
            #     msg = "The price of " + coin + " is (+)increasing."
            #     prepare_to_sell = True
            # elif (last < mean):
            #     msg = "The price of " + coin + " is (-)decreasing."
            #     prepare_to_buy = True
            # print(msg)

        elif dx >= 2*std and dx < 3*std:
            print("anomaly of +2 std")
            if (last > mean):
                msg = "The price of " + coin + " is (+)increasing."
                prepare_to_sell = True
            elif (last < mean):
                msg = "The price of " + coin + " is (-)decreasing."
                prepare_to_buy = True
            print(msg)
        elif dx >= 3*std:
            print("anomaly of +3 std")
            # if (last > mean):
            #     msg = "The price of " + coin + " is (+)increasing."
            #     prepare_to_sell = True
            # elif (last < mean):
            #     msg = "The price of " + coin + " is (-)decreasing."
            #     prepare_to_buy = True
            # print(msg)
        else:
            print("all good")
            if prepare_to_buy:
                portfolio[dtit_s]['_buy']=( {'buyprice':last} )    
                prepare_to_buy = False
            if prepare_to_sell:
                portfolio[dtit_s]['_sell']=( {'sellprice':last} )    
                prepare_to_sell = False

        dtit += datetime.timedelta(minutes=incrementMinutes)
        print("---")

    #portfolioToImage(portfolio)
    print("\n\n")
    print( json.dumps(processPortfolio(portfolio, 1)) )

def backtest2_AnomalyDetection_binance_exchangeFilter():
    
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

    coin = 'BTCUSDT'
    historymins = 60*24*1
    dtend = datetime.datetime.strptime('2018-03-13 13:40', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    inp = getPriceDataExchange('binance', coin, historymins, dtend)
    
    canBuy = True
    canSell = False

    incrementMinutes = 1

    maA = []
    sizeA = 10
    maB = []
    sizeB = 30
    bucket = []
    while dtit < dtend:
        #print(dtit)
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}
        fts = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
        idx = next((i for i, item in enumerate(inp) if item['label'] == fts), -1)
        if (idx != -1):
            
            lastPrice = (inp[idx]['data']['open']+inp[idx]['data']['close'])/2
            bucket.append(lastPrice)

            if len(bucket) >= sizeA and len(bucket) >= sizeB:
                avgA = sum(bucket[-sizeA:])/sizeA
                avgB = sum(bucket[-sizeB:])/sizeB

                LB = 10
                if len(maA) >= LB and len(maB) >= LB:
                    a = sum(maA[-LB:])/LB
                    b = sum(maB[-LB:])/LB
                    if b > a and avgA > avgB: # short SMA takes the lead
                        buy()
                    elif a > b and avgB > avgA: # long SMA takes the lead
                        sell()


                maA.append(avgA)
                maB.append(avgB)

        dtit += datetime.timedelta(minutes=incrementMinutes)

    print( json.dumps(processPortfolio(portfolio, 0.5, 0.5)['_']) )


def test_hypothesis_A():
    # from statistics based on vol24 and price (14 days, ending in Feb 27, at 2min intervals)
    # we observe that price is lowest at midnight and 10am UTC
    # and price is highest at 23:00 UTC
    
    portfolio = {}

    interval = 2
    avg_len = 15
    coin = "BTC"
    historymins = 60*24*14
    dtend = datetime.datetime.strptime('2018-03-07 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    inp = getPriceData(coin, interval, historymins, dtend)


    incrementMinutes = 2
    while dtit < dtend:
        #print(dtit)
        
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}

        fts = datetime.datetime.strftime(dtit,'%Y-%m-%dT%H:%M')
        idx = next((i for i, item in enumerate(inp) if item['label'] == fts), -1)
        if idx == -1: continue
        ap = inp[idx]["avg"]
        portfolio[dtit_s]["ap"]= ap

        HH = datetime.datetime.strftime(dtit, '%H')


        if HH == "00" or HH=="00":
            portfolio[dtit_s]['_buy']=( {'buyprice':ap} )    
        if HH == "23":
            portfolio[dtit_s]['_sell']=( {'sellprice':ap} )    

        dtit += datetime.timedelta(minutes=incrementMinutes)
        #print("---")

    print("\n\n")
    print( json.dumps(processPortfolio(portfolio, 1)) )

def test_hypothesis_A_exchange():
    # from statistics based on vol24 and price (14 days, ending in Feb 27, at 2min intervals)
    # we observe that price is lowest at midnight and 10am UTC
    # and price is highest at 23:00 UTC
    
    portfolio = {}
    agr = {}

    base = "ETH"
    quote = "USDT"
    historymins = 60*24*30*1
    dtend = datetime.datetime.strptime('2018-04-01 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    interval = 10
    inp = getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    while dtit < dtend:
        

        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
        if dtit_s not in portfolio:
            portfolio[dtit_s] = {}
        idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')

        if idx in inp:
            #print(idx)
            ap = (inp[idx]['open']+inp[idx]['close'])/2
            portfolio[dtit_s]["ap"]= ap
            HH = datetime.datetime.strftime(dtit, '%H')
            if HH == "20":
                portfolio[dtit_s]['_buy']=( {'buyprice':ap*1.001} )    
            if HH == "00":
                portfolio[dtit_s]['_sell']=( {'sellprice':ap} )   
            if not HH in agr:
                agr[HH] = []
            agr[HH].append(ap)

        dtit += datetime.timedelta(minutes=interval)
        #print("---")
    for i, j in agr.items():
        agr[i] = sum(j)/len(j)

    for i, j in sorted(agr.items()):
        print(i + "\t" + str(j))

    print("\n\n")
    #print(json.dumps(portfolio))

    print(str(100/100) + "\t" + str(processPortfolio(portfolio, 1)['_']['ROI%']))
    for x in range(0, 101, 5):
        print(str(x) + "\t" + str(processPortfolio(copy.deepcopy(portfolio), x/100)['_']['ROI%']))
        

def test_hypothesis_A_exchange_randomHH():
    
    import random

    base = "LTC"
    quote = "USDT"
    historymins = 60*24*30*4
    dtend = datetime.datetime.strptime('2018-04-01 00:00', '%Y-%m-%d %H:%M')
    
    interval = 10
    inp = getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    
    def work():
        dtstart = dtend - datetime.timedelta(minutes=historymins)
        dtit = dtstart

        portfolio = {}
        agr = {}
        miHH = str(random.randint(0, 24)).zfill(2)
        maHH = str(random.randint(0, 24)).zfill(2)
        while dtit < dtend:
            
            dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
            if dtit_s not in portfolio:
                portfolio[dtit_s] = {}
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')

            if idx in inp:
                ap = (inp[idx]['open']+inp[idx]['close'])/2
                portfolio[dtit_s]["ap"]= ap
                HH = datetime.datetime.strftime(dtit, '%H')
                if HH == miHH:
                    portfolio[dtit_s]['_buy']=( {'buyprice':ap*1.001} )    
                if HH == maHH:
                    portfolio[dtit_s]['_sell']=( {'sellprice':ap} )   
                # if not HH in agr:
                #     agr[HH] = []
                # agr[HH].append(ap)

            dtit += datetime.timedelta(minutes=interval)
        
        # for i, j in agr.items():
        #     agr[i] = sum(j)/len(j)
        # for i, j in sorted(agr.items()):
        #     print(i + "\t" + str(j))

        out = processPortfolio(copy.deepcopy(portfolio), .5)['_']['%']
        print("%f \t %s %s " % (out, miHH, maHH))
        return out

    arr = []
    for i in range(100):
        arr.append(work())

    print(sum(arr)/len(arr))

def test_hypothesis_A_exchange_slidingWindow():
    # from statistics based on vol24 and price (14 days, ending in Feb 27, at 2min intervals)
    # we observe that price is lowest at midnight and 10am UTC
    # and price is highest at 23:00 UTC
    
    portfolio = {}
    agr = {}
    window = []
    interval = 60
    windowLen = (60/interval)*24*7 # 3 day window

    base = "LTC"
    quote = "USDT"
    historymins = 60*24*30*4
    dtend = datetime.datetime.strptime('2018-04-01 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    
    inp = getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    counter = 0
    while dtit < dtend:
        dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
        if dtit_s not in portfolio: portfolio[dtit_s] = {}
        idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')

        if len(window) < windowLen:
            if idx in inp:
                inp[idx]['dt'] = dtit
                window.append(inp[idx])
        else:

            agr = {}
            for x in window:
                ap = (x['open']+x['close']+x['high']+x['low'])/4
                # print(x['dt'])
                HH = datetime.datetime.strftime(x['dt'], '%H')
                if not HH in agr: agr[HH] = []
                agr[HH].append(ap)

        
            mi = None
            ma = None
            miHH = None
            maHH = None
            for i, j in agr.items():
                agr[i] = sum(j)/len(j)
            for i, j in agr.items():
                if mi == None or j < mi:
                    mi = j
                    miHH = i
                if ma == None or j > ma:
                    ma = j
                    maHH = i



            # print(str(miHH) + " " + str(maHH))
            if miHH and maHH and idx in inp:
                print(miHH + "  " + maHH)
                #print(idx)
                ap = (inp[idx]['open']+inp[idx]['close']+inp[idx]['high']+inp[idx]['low'])/4
                portfolio[dtit_s]["ap"]= ap
                HH = datetime.datetime.strftime(dtit, '%H')
                if HH == miHH:
                    # print("buy: " + HH)
                    portfolio[dtit_s]['_buy']=( {'buyprice':ap*1.001} )    
                if HH == maHH:
                    # print("sell: " + HH)
                    portfolio[dtit_s]['_sell']=( {'sellprice':ap} )
        
            
            window.pop(0)    

            
            if idx in inp:
                inp[idx]['dt'] = dtit
                window.append(inp[idx])

        dtit += datetime.timedelta(minutes=interval)



    print("\n\n")
    #print(json.dumps(portfolio))

    print(processPortfolio(portfolio, .2)['_'])
    #for x in range(0, 101, 5):
    #    print(str(x) + "\t" + str(processPortfolio(copy.deepcopy(portfolio), x/100)['_']['%']))
        #print( json.dumps(processPortfolio(portfolio, x/100)['_']) )
        #print("")

# !!! damn
def test_hypothesis_B():
    # slope |S| of (t-1) -> (t)
    
    portfolio = {}
    agr = {}

    base = "BTC"
    quote = "USDT"
    #historymins = 60*24*30*3
    historymins = 60*24*30
    dtend = datetime.datetime.strptime('2018-04-10 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    dtit = dtstart
    interval = 60
    inp = getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)

    prevPrice = None
    bucket = {'dt': None, 'arr':[]}
    buckets = []
    while dtit < dtend:
        idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
        if idx in inp:
            ohlc = (inp[idx]['open']+inp[idx]['close']+inp[idx]['low']+inp[idx]['high'])/4
            ohc = (inp[idx]['open']+inp[idx]['close']+inp[idx]['high'])/3
            olc = (inp[idx]['open']+inp[idx]['close']+inp[idx]['low'])/3
            ohl = (inp[idx]['open']+inp[idx]['high']+inp[idx]['low'])/3
            oc = (inp[idx]['open']+inp[idx]['close'])/2
            c = (inp[idx]['close'])
            o = (inp[idx]['open'])
            h = (inp[idx]['high'])
            l = (inp[idx]['low'])

            # price = oc
            price = random.randint(int(l), int(h)) if h > l else random.randint(int(h), int(l))
            
            dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
            if dtit_s not in portfolio: portfolio[dtit_s] = {}
            portfolio[dtit_s]["ap"]= price
            

            if prevPrice != None:
                if price >= prevPrice:
                    slope_pct = round((price-prevPrice)/prevPrice*100,2)
                    if bucket['dt'] == None: bucket['dt'] = idx
                    bucket['arr'].append( slope_pct )

                    if slope_pct >= 0.9: #and len(bucket['arr']) >= 2:
                        portfolio[dtit_s]['_buy']=( {'buyprice':price } )
                else:
                    if len(bucket['arr']) > 0:
                        buckets.append(bucket)
                        portfolio[dtit_s]['_sell']=( {'sellprice':price } ) 
                    bucket = {'dt': None, 'arr':[]}

            prevPrice = price

        dtit += datetime.timedelta(minutes=interval)
        

    #print(json.dumps(buckets))
    proc = processPortfolio(portfolio, 1)
    print( json.dumps(proc['_']) )
    #print( json.dumps() )


def test_hypothesis_B_randPrice():

	# let's try including our predictions as additional condition to buy and/or sell 
    
    base = "BTC"
    #base = "ETH"
    #base = "LTC"

    quote = "USDT"
    historymins = 60*24*30 #60*24*30*4
    dtend = datetime.datetime.strptime('2018-04-13 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    interval = 60
    inp = getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    uncertainty_margin = 0.001

    def work(dtstart, dtend):
        portfolio = {}
        prevPrice = None
        slopes = []
        dtit = dtstart
        while dtit < dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']
                ohlc = (o+h+l+c)/4
                ohc = (o+h+c)/3
                olc = (o+l+c)/3
                ohl = (o+h+l)/3
                oc = (o+c)/2

                # price = random.randint(int(o), int(c)) if int(c) > int(o) else random.randint(int(c), int(o)) 
                price = o + (c-o)*random.randint(0,10)/10
                buyprice = price # random.randint(int(l), int(h)) if int(h) > int(l) else random.randint(int(h), int(l))
                sellprice = price # random.randint(int(l), int(h)) if int(h) > int(l) else random.randint(int(h), int(l))

                dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
                if dtit_s not in portfolio: portfolio[dtit_s] = {}
                portfolio[dtit_s]["ap"]= price
                portfolio[dtit_s]["open"]= o
                portfolio[dtit_s]["close"]= c
                portfolio[dtit_s]["low"]= l
                portfolio[dtit_s]["high"]= h

                if prevPrice != None:
                    slope_pct = round((price-prevPrice)/prevPrice*100,2)
                    slopes.append(slope_pct)
                    if price > prevPrice:
                        slopes.append( slope_pct )
                        
                        avgS = sum(slopes)/len(slopes)
                        if avgS > .3 :
                            portfolio[dtit_s]['_buy']=( {'buyprice_':buyprice,'buyprice':buyprice*(1+uncertainty_margin) } )
                    else:
                        if len(slopes) > 0:
                            portfolio[dtit_s]['_sell']=( {'sellprice_':sellprice,'sellprice':sellprice*(1-uncertainty_margin) } ) 
                        slopes = []

                prevPrice = c

            dtit += datetime.timedelta(minutes=interval)
            

        proc = processPortfolio(portfolio, 1)
        portfolioToChart(portfolio)
        return proc['_']['ROI%']

    avgs = []
    for x in range(10):
        out = work(dtstart, dtend)
        print("%s \t %f" % (str(x), out))
        avgs.append(out)
    print("avg:")
    print(sum(avgs)/len(avgs))
    std = np.std(avgs)
    print("std:")
    print(std)

    # price=buyP=sellP=rand(o,c) ; avg(bucket)>.4 ; buyrate=1 ; itrs=1000 ; prevPrice=c ; interval=30
	    # avg: 21.48036059510522
		# std: 8.884097682920208
	# price=buyP=sellP=rand(o,c) ; avg(bucket)>.4 ; buyrate=1 ; itrs=1000 ; prevPrice=c ; interval=60
	    # avg: 24.05144832316877
		# std: 7.929286512881277
	# price=buyP=sellP=(o+(c-o)*rand(0,10)/10) ; avg(bucket)>.4 ; buyrate=1 ; itrs=1000 ; prevPrice=c ; interval=30
		# avg: 11.682762756413297
		# std: 8.42876352596316


import plotly
import plotly.plotly as py
import plotly.graph_objs as go

def portfolioToChart(portfolio):
    
    opens = []
    highs = []
    lows = []
    closes = []
    dates = []

    annons = []
    
    for key, obj in portfolio.items():
        if key == "_": continue
        dt = datetime.datetime.strptime(key, '%Y-%m-%d %H:%M')
        opens.append(obj['open'])
        highs.append(obj['high'])
        lows.append(obj['low'])
        closes.append(obj['close'])
        dates.append( dt )
        if '_buy' in obj:
            annons.append(
                {
                    'x':dt,
                    'y':obj['_buy']['buyprice_'],
                    'text':"B",
                    'arrowcolor': "black",
                }
            )

        if '_sell' in obj:
            annons.append(
                {
                    'x':dt,
                    'y':obj['_sell']['sellprice_'],
                    'text':"S",
                    'arrowcolor': "blue",
                }
            )
        
    
    trace = go.Candlestick(x=dates,
                        open=opens,
                        high=highs,
                        low=lows,
                        close=closes)
    layout = go.Layout(
        xaxis = dict(
            rangeslider = dict(
                visible = False
            )
        ),
        annotations = annons,
        dragmode = "pan"
    )
    data = [trace]
    fig = go.Figure(data=data,layout=layout)
    config = {'scrollZoom': True}
    plotly.offline.plot(fig, config=config, filename='/home/nevolin/public_html/cryptoproto/PWA/server/views/public/test/chart.html')




if __name__ == '__main__':
    #backtest2_AnomalyDetection()
    #backtest1()
    #test_hypothesis_A()
    #backtest2_AnomalyDetection_binance_exchangeFilter()
    
    #test_hypothesis_A_exchange()
    #test_hypothesis_A_exchange_slidingWindow()
    #test_hypothesis_A_exchange_randomHH()
    
    #test_hypothesis_B()
    test_hypothesis_B_randPrice()