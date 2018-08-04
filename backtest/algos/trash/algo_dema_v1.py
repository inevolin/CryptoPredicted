
import json
import sys
sys.dont_write_bytecode = True

import numpy as np
import datetime
import random
import math
import core

def run(debug):

    base = "BTC"
    #base = "ETH"
    #base = "LTC"

    quote = "USDT"
    historymins = 60*24*30*1 #60*24*30*4
    interval = 60
    dtend = datetime.datetime.strptime('2018-04-15 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    uncertainty_margin = 0.001
 

    def EMAsingle(price, prev, size):
        multiplier = (2 / float(1 + size))
        v = price*multiplier + prev*(1-multiplier)
        return v

    def sig(prev_len, prevY, prevs, price):
        if len(prevY) == 0: return price
        prev = prevY[-1]
        multiplier = (2 / float(1 + prev_len))
        v = price*multiplier + prev*(1-multiplier)
        v = 2*EMAsingle(price, prev, prev_len) - EMAsingle(EMAsingle(price, prev, prev_len), prev, prev_len)
        return v

    def work(_1, _2):
        portfolio = {}
        dtit = dtstart
        prevs = []
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA", "y")
        traceA['prev_len'] = _1

        traceB = core.createNewScatterTrace("traceB", "y")
        traceB['prev_len'] = _2 

        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                #price = (o+c)/2   # ok
                # price = c         # ok
                price = o + (c-o)*random.randint(0,10)/10 # ok
                #price = random.uniform(o, c) if c > o else random.uniform(c, o) 
                # price = random.uniform(l, h)  # much worse than [open, close]

                buyprice = price
                sellprice = price

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)
            
                core.addToScatterTrace(traceA, dtit, sig(traceA['prev_len'], traceA['y'], prevs, price))
                core.addToScatterTrace(traceB, dtit, sig(traceB['prev_len'], traceB['y'], prevs, price))

                if len(traceA['y']) > 1:
                    if canBuy and (traceA['y'][-2] < traceB['y'][-2] and traceA['y'][-1] > traceB['y'][-1]):
                            core.portfolioBuy(portfolio, dtit, buyprice, uncertainty_margin)
                            canSell = True
                            canBuy = False
                    elif canSell and (traceA['y'][-2] > traceB['y'][-2] and traceA['y'][-1] < traceB['y'][-1]):
                            core.portfolioSell(portfolio, dtit, sellprice, uncertainty_margin)
                            canSell = False
                            canBuy = True

                prevs.append(price)
            dtit += datetime.timedelta(minutes=interval)

        # beautify (replacing 0's by None )
        for i,v in enumerate(traceB['y']):
            if v == 0:
                traceB['y'][i]=None

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceB])


    if debug == 0: # computing ROI
        A = 1
        B = 2
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work(A, B)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    elif debug == 1: # brute-force searching for optimal parameters (A & B)
        arr = []
        for A in range(1, 30):
            for B in range(2, 30):
                if (B <= A): continue
                rois = []
                for x in range(5):
                    (proc, portfolio, traces) = work(A, B)
                    rois.append( proc['_']['ROI%'] )
                arr.append({"ROI": np.average(rois), "A": A, "B": B})
                print("ROI: %i %i %f" % (A, B, np.average(rois)))
        print(sorted(arr, key=lambda x: x['ROI']))
    
    else: # computing and plotting out
        A = 8
        B = 23
        (proc, portfolio, traces) = work(A, B)
        print("ROI: (%i, %i) %f" % (A, B, proc['_']['ROI%']))
        core.portfolioToChart_OHLC(portfolio, traces)


if __name__ == '__main__':
    debug = 1
    run(debug)