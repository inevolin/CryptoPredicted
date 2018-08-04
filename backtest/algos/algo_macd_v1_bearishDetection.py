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
    base = "ETH"
    base = "LTC"

    quote = "USDT"
    historymins = 60*24*30*3 #60*24*30*4
    interval = 60
    dtend = datetime.datetime.strptime('2018-05-02 15:00', '%Y-%m-%d %H:%M')
    dtend = datetime.datetime.strptime('2018-05-17 12:00', '%Y-%m-%d %H:%M')

    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)

    uncertainty_margin = 0.001

    def sig(prev_len, prevY, price):
        if len(prevY) == 0: return price
        multiplier = (2 / float(1 + prev_len))
        v = price*multiplier + prevY[-1]*(1-multiplier)
        return v

    def sig_bear(prev_len, prevPrice, price):
        multiplier = (2 / float(1 + prev_len))
        v = price*multiplier + prevPrice*(1-multiplier)
        return v

    def normalize(arr):
        a = arr[:]
        mi = min(a)
        ma = max(a)
        if (ma-mi) == 0: return [0.0]
        for i,v in enumerate(a):
            a[i] = (a[i]-mi)/(ma-mi)
        return a
  

    def work(_1, _2, _3, _4):
        portfolio = {}
        dtit = dtstart
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA", "y")
        traceA['prev_len'] = _1

        traceB = core.createNewScatterTrace("traceB", "y")
        traceB['prev_len'] = _2 

        traceC = core.createNewScatterTrace("traceC", "y2")
        traceD = core.createNewScatterTrace("traceD", "y2")

        trace_bear_A = core.createNewScatterTrace("trace_bear_A", "y2")
        trace_bear_B = core.createNewScatterTrace("trace_bear_B", "y2")
        trace_bear_C = core.createNewScatterTrace("trace_bear_C", "y2")
        
        buyPrice = None
        prevC = None
        prevCavg = None
        bucket=[]
        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                #price = (o+c+l+h)/4   # ok
                #price = (o+c)/2   # ok
                #price = c         # ok
                #price = o + (c-o)*random.randint(0,10)/10 # ok
                #price = random.uniform(o, c) if c > o else random.uniform(c, o) 
                price = random.uniform(l, h)  # reality

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)
                
                pA = sig(traceA['prev_len'], traceA['y'], o)
                pB = sig(traceB['prev_len'], traceB['y'], c)
                pC = pA-pB
                pC = sig(3, [prevC if prevC != None else pC], pC)
                bucket.append(pC)
                pCavg = np.average(bucket[-10:])


                core.addToScatterTrace(traceA, dtit, pA)
                core.addToScatterTrace(traceB, dtit, pB)
                core.addToScatterTrace(traceC, dtit, pC)
                core.addToScatterTrace(traceD, dtit, pCavg)

                BL= 5
                core.addToScatterTrace(trace_bear_A, dtit, sig_bear(2, np.average(trace_bear_A['y'][-BL:]) if len(trace_bear_A['y'])>0 else (o+c)/2, (o+c)/2))
                core.addToScatterTrace(trace_bear_B, dtit, sig_bear(15, np.average(trace_bear_B['y'][-BL:]) if len(trace_bear_B['y'])>0 else (o+c)/2, (o+c)/2))
                CL = 24*4
                core.addToScatterTrace(trace_bear_C, dtit, np.average(trace_bear_A['y'][-CL:])   )

                if len(bucket) > 2:

                    if canBuy and (prevCavg < 0 and pCavg > 0):
                        if trace_bear_B['y'][-1] > trace_bear_C['y'][-1]: # don't trade downtrend
                            core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                            canSell = True
                            canBuy = False
                            buyPrice = price
                    elif canSell and (price > buyPrice*_3 or price < buyPrice*_4):
                            core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                            canSell = False
                            canBuy = True
                prevC = pC
                prevCavg = pCavg

            dtit += datetime.timedelta(minutes=interval)

        for i,v in enumerate(traceB['y']):# beautify (replacing 0's by None )
            if v == 0:
                traceB['y'][i]=None

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceB, traceC, traceD, trace_bear_B, trace_bear_C])


    if debug == 0: # computing ROI
        A = 2
        B = 15
        C = 1.03
        D = 0.97
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work(A, B, C, D)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    elif debug == 1: # brute-force searching for optimal parameters (A,B,C,D)
        dct = {}
        for A in range(1, 30):
            for B in range(2, 30):
                if (B <= A): continue
                for C in [1+x/100 for x in range(0, 10)]:
                    for D in [0.90+x/100 for x in range(0, 10)]:
                        avgs = []
                        for x in range(20):
                            (proc, portfolio, traces) = work(A,B,C,D)
                            #print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
                            avgs.append(proc['_']['ROI%'])

                        print("%f %f %f %f" % (A,B,C,D))
                        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
                        std = np.std(avgs)
                        print("std ROI%: " + str(std))

                        if not str(sum(avgs)/len(avgs)) in dct:
                            dct [ str(sum(avgs)/len(avgs)) ] = str(A)+"_"+str(B)+"_"+str(C)+"_"+str(D)
        print("--------")
        print(base)
        print("--------")
        print(json.dumps(dct))
        print("--------")
        print(base)
    
    else: # computing and plotting out
        A = 2
        B = 15
        C = 1.03
        D = 0.97
        (proc, portfolio, traces) = work(A, B, C, D)
        print("ROI: (%i, %i %f %f) %f" % (A,B,C,D, proc['_']['ROI%']))
        core.portfolioToChart_OHLC(portfolio, traces)


if __name__ == '__main__':
    debug = 0
    run(debug)

