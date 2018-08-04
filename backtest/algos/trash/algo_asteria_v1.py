
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
    historymins = 60*24*30*4 #60*24*30*4
    interval = 120
    dtend = datetime.datetime.strptime('2018-04-15 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    uncertainty_margin = 0.001

    def EMA(_arr, size, iterations=2): # simplified version
        multiplier = (2 / float(1 + size))

        arr = _arr[:] # slice/copy it
        for j in range(iterations):
            ema = [ arr[0] ]
            for i in range(1, len(arr)):
                v = (arr[i]*multiplier) + (ema[i-1]*(1-multiplier))
                ema.append( v )
            arr = ema[:]

        return arr

    def sig(prev_len, prevs, price, num):
        x = price-np.average(prevs[ -prev_len: ])
        u = EMA(prevs[ -prev_len: ], prev_len, 1)
        z = np.average(u)
        x = (-1 if x < 0 else 1) * math.log(abs(z/prev_len))
        x = (-num if x < 0 else num)
        return x

    def sig2(prev_len, prevs, price):
        u = EMA(prevs, prev_len, 1)
        z = u[-1]
        return z

    def isDownTrend(arr):
        if len(arr) < 10: return True
        arr = arr[:]
        j = int(len(arr)/3)
        first = np.average(arr[:j])
        mid = np.average(arr[j:j*2])
        last = np.average(arr[-j:])
        
        
        if first > mid or mid > last:
            return True
        return False

    def work():
        portfolio = {}
        dtit = dtstart
        prevs = []
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA", "y2")
        traceA['prev_len'] = 10

        traceB = core.createNewScatterTrace("traceB", "y")
        traceB['prev_len'] = 12 # make sure it's large enough ( >= 12) for isDownTrend formula

        upduration_A = 0
        downduration_A = 0
   
        prevBuyPrice = 0

        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                price = (o+c)/2   # ok
                # price = c         # ok
                #price = o + (c-o)*random.randint(0,10)/10 # ok
                # price = random.uniform(o, c) if c > o else random.uniform(c, o) 
                # price = random.uniform(l, h)  # much worse than [open, close]

                buyprice = price
                sellprice = price

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)
                if len(prevs) > 0:
                    core.addToScatterTrace(traceA, dtit, sig(traceA['prev_len'], prevs, price, 1))
                    core.addToScatterTrace(traceB, dtit, sig2(traceB['prev_len'], prevs, price))

                    if len(traceA['y']) > 1:
                        if traceA['y'][-1] > 0 and traceA['y'][-2] > 0: # A up -> up
                            upduration_A += 1
                        if traceA['y'][-1] < 0 and traceA['y'][-2] > 0: # A up -> down
                            upduration_A = 0
                        if traceA['y'][-1] < 0 and traceA['y'][-2] < 0: # A down -> down
                            downduration_A += 1
                        if traceA['y'][-1] > 0 and traceA['y'][-2] < 0: # A down -> up
                            downduration_A = 0

                        if canBuy and isDownTrend(traceB['y'][-traceB['prev_len']:])==False:
                            if traceA['y'][-1] > 0 and traceA['y'][-2] < 0: # B down -> up

                                core.portfolioBuy(portfolio, dtit, buyprice, uncertainty_margin)
                                prevBuyPrice = buyprice
                                canSell = True
                                canBuy = False
                        elif canSell:
                            if traceA['y'][-1] < 0 and traceA['y'][-2] > 0: # B up -> down
                                core.portfolioSell(portfolio, dtit, sellprice, uncertainty_margin)
                                canSell = False
                                canBuy = True


                else:
                    core.addToScatterTrace(traceA, dtit, 0) # use 0 instead of None
                    core.addToScatterTrace(traceB, dtit, 0) # use 0 instead of None

                prevs.append(price)

            # else:
            #     print("missing: " + str(idx))

            dtit += datetime.timedelta(minutes=interval)

        # beautify (replacing 0's by None )
        for i,v in enumerate(traceB['y']):
            if v == 0:
                traceB['y'][i]=None

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceB])


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
    # 60min interval over 100 days:
    	# BTC: 11%
    	# ETH: 47%
    	# LTC: -4%
    # 120min interval over 100 days:
    	# BTC: 36%
    	# ETH: 31%
    	# LTC: 56%

if __name__ == '__main__':
    debug = 1
    run(debug)