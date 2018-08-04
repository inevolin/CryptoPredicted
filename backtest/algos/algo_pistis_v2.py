
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
    historymins = 60*24*14 #60*24*30*4
    interval = 60
    dtend = datetime.datetime.strptime('2018-05-02 12:00', '%Y-%m-%d %H:%M')
    #dtend = datetime.datetime.strptime('2018-05-26 12:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    # inp = json.load(open("./LTC_60m.json"))
    uncertainty_margin = 0.001


    def EMAsingle(size, prevY, price):
        if len(prevY) == 0: return price
        multiplier = (2 / float(1 + size))
        v = price*multiplier + prevY[-1]*(1-multiplier)
        return v

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
    
    def work(_1, _2):
        portfolio = {}
        dtit = dtstart
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA" ,"y")
        traceC = core.createNewScatterTrace("traceC" ,"y")

        hp_arrL = 35
        hp_arrEL = 4

        usage = {
            'canBuy': True,
            'canSell': False,

            'buyPrice': None,
        }

        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                volume = inp[idx]['volume']
                trades = inp[idx]['trades']
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']


                #price = (o+c+l+h)/4   # ok
                price = (o+c)/2
                #price = c         # ok
                #price = o + (c-o)*random.randint(0,10)/10 # ok
                #price = random.uniform(o, c) if c > o else random.uniform(c, o) 
                price = random.uniform(l, h)  # reality

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)
            
                pA = sigA(traceA['y'], traceA['z'], price, hp_arrL, hp_arrEL)
                pC = sigC(traceC['y'], traceA['z'], price, hp_arrL, hp_arrEL)
                core.addToScatterTrace(traceA, dtit, pA)
                core.addToScatterTrace(traceC, dtit, pC)

                def buyF():
                    #if pC >= o and pC <= c:
                    if pC >= l and pC <= h:
                        return True
                def sellF():
                    if price > usage['buyPrice']*_1: #and not buyF():
                        return True 
                    if price < usage['buyPrice']*_2:
                        return True

                if usage['canBuy'] and buyF():
                        core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                        usage['canSell'] = True
                        usage['canBuy'] = False
                        usage['buyPrice'] = price
                elif usage['canSell'] and sellF():
                        core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                        usage['canSell'] = False
                        usage['canBuy'] = True
                        usage['sellPrice'] = price

                
            dtit += datetime.timedelta(minutes=interval)


        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceC])


    if debug == 0:
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work(1.06, 0.92)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))

    elif debug == 1: # brute-force searching for optimal parameters (A,B,C,D)
        dct = {}

        for A in [1+x/100 for x in range(1, 10)]:
            for B in [0.90+x/100 for x in range(1, 10)]:
                avgs = []
                for x in range(20):
                    (proc, portfolio, traces) = work(A,B)
                    avgs.append(proc['_']['ROI%'])

                print("%f %f" % (A,B))
                print("avg ROI%: " + str(sum(avgs)/len(avgs)))
                std = np.std(avgs)
                print("std ROI%: " + str(std))

                if not str(sum(avgs)/len(avgs)) in dct:
                    dct [ str(sum(avgs)/len(avgs)) ] = str(A)+"_"+str(B)
        print("--------")
        print(base)
        print("--------")
        print(json.dumps(dct))
        print("--------")
        print(base)
    
    else:
        (proc, portfolio, traces) = work(1.02, 0.98)
        print("ROI: %f" % proc['_']['ROI%'])
        core.portfolioToChart_OHLC(portfolio, traces)


# notes:
    # unfinished
    # works only in specific regions ; overall performs negatively

if __name__ == '__main__':
    debug = 2
    run(debug)