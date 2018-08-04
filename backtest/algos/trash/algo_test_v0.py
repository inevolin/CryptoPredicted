
import json
import sys
sys.dont_write_bytecode = True

import numpy as np
import datetime
import random
import math
import core

def run(debug):

    # this strategy works best at 1hr intervals
    # 1. the idea is based on calculating the slope of the current price (which is a random price at interval 't') against the previous close price.
    # 2. it also makes sure a buy occurs when the current price is higher than the previous one
    # 3. 

    base = "BTC"
    #base = "ETH"
    #base = "LTC"

    quote = "USDT"
    historymins = 60*24*30*1 #60*24*30*4
    interval = 60
    dtend = datetime.datetime.strptime('2018-04-23 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    # inp = json.load(open("./LTC_60m.json"))
    uncertainty_margin = 0.001

    def EMAsingle(size, prevY, price):
        if len(prevY) == 0: return price
        multiplier = (2 / float(1 + size))
        v = price*multiplier + prevY[-1]*(1-multiplier)
        return v

    def normalize(arr):
        a = arr[:]
        mi = min(a)
        ma = max(a)
        for i,v in enumerate(a):
            arr[i] = (arr[i]-mi)/(ma-mi)

    def finalizeTrace(trace):
        # beautify (replacing 0's by None )
        for i,v in enumerate(trace['y']):
            if v == 0:
                trace['y'][i]=None


    def sigA(y, z, o,h,l,c):
        z.append(o)
        if len(z) < 2: return 0
        dy = z[-1] - z[-2]
        f = math.log(1+abs(dy)) * (1 if dy > 0 else -1)

        if f < -1:
            return -2
        elif f > 1:
            return 2
        else:
            return 2
        


    def sigB(y, z, o,h,l,c):
        return 0

    def sigC(y, z, o,h,l,c):
        return 0

    
    
    def work():
        portfolio = {}
        dtit = dtstart
        canBuy = True
        canSell = False
        prevBuyPrice = 0

        traceA = core.createNewScatterTrace("traceA" ,"y2")
        traceB = core.createNewScatterTrace("traceB" ,"y2")
        traceC = core.createNewScatterTrace("traceC" ,"y2")

        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                volume = inp[idx]['volume']
                trades = inp[idx]['trades']
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                #price = (o+c)/2   # ok
                # price = c         # ok
                #price = o + (c-o)*random.randint(0,10)/10 # ok
                #price = random.randint(int(o), int(c)) if int(c) > int(o) else random.randint(int(c), int(o)) # ok
                #price = random.randint(int(l), int(h)) if int(h) > int(l) else random.randint(int(h), int(l)) # still "okay" but much worse then [open, close]
                price = o

                buyprice = price
                sellprice = price

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)

                valA = sigA(traceA['y'], traceA['z'], o,h,l,c)
                valB = sigB(traceB['y'], traceB['z'], o,h,l,c)
                valC = sigC(traceC['y'], traceC['z'], o,h,l,c)
                
            
                core.addToScatterTrace(traceA, dtit, valA)
                core.addToScatterTrace(traceB, dtit, valB)
                core.addToScatterTrace(traceC, dtit, valC)

                if len(traceA['y']) > 1:
                    

                    # core.addToScatterTrace(traceC, dtit, abs(traceB['y'][-1]/traceA['y'][-1]))

                    if canBuy and (traceA['y'][-1] > traceA['y'][-2]): # abs(traceB['y'][-1]/traceA['y'][-1]) > 1.0  and np.average(traceA['y'][-2:])<buyprice :
                        core.portfolioBuy(portfolio, dtit, buyprice, uncertainty_margin)
                        prevBuyPrice = buyprice
                        canSell = True
                        canBuy = False
                    elif canSell and (traceA['y'][-1] < traceA['y'][-2] ):
                        core.portfolioSell(portfolio, dtit, sellprice, uncertainty_margin)
                        canSell = False
                        canBuy = True

                
            dtit += datetime.timedelta(minutes=interval)


        finalizeTrace(traceA)
        finalizeTrace(traceB)
        finalizeTrace(traceC)

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceB, traceC])


    if debug == 0:
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work()
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    else:
        (proc, portfolio, traces) = work()
        print("ROI: %f" % proc['_']['ROI%'])
        core.portfolioToChart_OHLC(portfolio, traces)


# notes:
    # unfinished
    # works only in specific regions ; overall performs negatively

if __name__ == '__main__':
    debug = 1
    run(debug)