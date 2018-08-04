
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
    historymins = 60*24*30 #60*24*30*4
    interval = 30
    dtend = datetime.datetime.strptime('2018-04-29 20:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    # inp = json.load(open("./LTC_60m.json"))
    uncertainty_margin = 0.001

    def finalizeTrace(trace):
        # beautify (replacing 0's by None )
        for i,v in enumerate(trace['y']):
            if v == 0:
                trace['y'][i]=None
    
    def work(hp_A=0.02, hp_B=0.1, hp_C=1.03, hp_D=0.97):
        portfolio = {}
        dtit = dtstart
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA" ,"y2")
        traceC = core.createNewScatterTrace("traceC" ,"y2")

        buyPrice = None
        prevPrice = None
        prevVolume = None

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
                #price = (o+l+h+c)/4

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)            
                if (prevPrice):
                    pA = 1/abs(volume-prevVolume)
                    core.addToScatterTrace(traceA, dtit, pA)
                    if canBuy and pA > hp_A and pA < hp_B:
                        core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                        canSell = True
                        canBuy = False
                        buyPrice = price
                    elif canSell and (price > buyPrice*hp_C or price < buyPrice*hp_D):
                        core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                        canSell = False
                        canBuy = True

                prevPrice = price
                prevVolume = volume
                
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

    elif debug == 2: # hyper-param optimization

        dct = {}
        for A in [x/100 for x in range(1, 10)]:
            for B in [x/10 for x in range(1, 10)]:
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

    
    else:
        # (proc, portfolio, traces) = work(0.07, .5, 1.08, .94)
        (proc, portfolio, traces) = work(0.06, .6, 1.07, .93)

        # (proc, portfolio, traces) = work(0.02, .1, 1.09, .92)
        # (proc, portfolio, traces) = work(0.01, .2, 1.06, .9)

        print("ROI: %f" % proc['_']['ROI%'])
        core.portfolioToChart_OHLC(portfolio, traces)


# notes:
    # unfinished
    # works only in specific regions ; overall performs negatively

if __name__ == '__main__':
    debug = 1
    run(debug)