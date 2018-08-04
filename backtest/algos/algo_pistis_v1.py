
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
    base = "ETH"
    #base = "LTC"

    quote = "USDT"
    historymins = 60*24*30*2 #60*24*30*4
    interval = 30
    dtend = datetime.datetime.strptime('2018-05-28 23:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    # inp = json.load(open("./LTC_60m.json"))
    uncertainty_margin = 0.001


    def EMAsingle(size, prevY, price):
        if len(prevY) == 0: return price
        multiplier = (2 / float(1 + size))
        v = price*multiplier + prevY[-1]*(1-multiplier)
        return v

    def finalizeTrace(trace):
        # beautify (replacing 0's by None )
        for i,v in enumerate(trace['y']):
            if v == 0:
                trace['y'][i]=None


    def sigA(y, z, price, hp_arrL, hp_arrEL):
        z.append(price)
        L = hp_arrL
        avg = np.average(z[-L:])
        std = np.std(z[-L:]) * 2
        out = avg + std
        out = EMAsingle(hp_arrEL, y, out)
        return out

    def sigC(y, z, price, hp_arrL, hp_arrEL):
        z.append(price)
        L = hp_arrL
        avg = np.average(z[-L:])
        std = np.std(z[-L:]) * 2
        out = avg - std
        out = EMAsingle(hp_arrEL, y, out)
        return out
    
    def work():
        portfolio = {}
        dtit = dtstart
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA" ,"y")
        traceC = core.createNewScatterTrace("traceC" ,"y")

        hp_arrL = 35
        hp_arrEL = 4

        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                volume = inp[idx]['volume']
                trades = inp[idx]['trades']
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                price = random.randint(int(l), int(h)) if int(h) > int(l) else random.randint(int(h), int(l)) # still "okay" but much worse than [open, close]

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)
            
                pA = sigA(traceA['y'], traceA['z'], price, hp_arrL, hp_arrEL)
                pC = sigC(traceC['y'], traceA['z'], price, hp_arrL, hp_arrEL)
                core.addToScatterTrace(traceA, dtit, pA)
                core.addToScatterTrace(traceC, dtit, pC)

                #if canBuy and (pC >= o and pC <= c):
                if canBuy and (pC >= l and pC <= h):
                    core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                    canSell = True
                    canBuy = False
                #elif canSell and (pA >= c and pA <= o):
                elif canSell and (pA >= l and pA <= h):
                    core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                    canSell = False
                    canBuy = True

                
            dtit += datetime.timedelta(minutes=interval)


        finalizeTrace(traceA)
        finalizeTrace(traceC)

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceC])


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