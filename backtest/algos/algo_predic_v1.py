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
    #base = "LTC"

    quote = "USDT"
    historymins = 60*24*30*2 #60*24*30*4
    interval = 60
    dtend = datetime.datetime.strptime('2018-05-02 15:00', '%Y-%m-%d %H:%M')
    #dtend = datetime.datetime.strptime('2018-05-17 12:00', '%Y-%m-%d %H:%M')
    #dtend = datetime.datetime.strptime('2018-06-02 12:00', '%Y-%m-%d %H:%M')
    dtend = datetime.datetime.strptime('2018-07-26 10:00', '%Y-%m-%d %H:%M')

    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    preds = core.getPredictions_v1('binance', interval, base, quote, historymins, dtend)
    #preds = json.load(open('misc/preds1.json'))

    uncertainty_margin = 0.001

    def work(_1, _2, _3, _4):
        portfolio = {}
        dtit = dtstart
        canBuy = True
        canSell = False

        traceA = core.createNewScatterTrace("traceA", "y")
        traceB = core.createNewScatterTrace("traceB", "y")
        
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
                
                shouldBuy=False
                if idx in preds:
                    x1,y1=list(preds[idx].items())[0]
                    x2,y2=list(preds[idx].items())[1]
                    _2 = 1.002
                    if ((y2['open']+y2['high']+y2['low']+y2['close'])/4) > ((y1['open']+y1['high']+y1['low']+y1['close'])/4)*_2:
                    	shouldBuy=True


                #if canBuy and (prevCavg < 0 and pCavg > 0) and pE > 0:
                if canBuy and shouldBuy :
                        core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                        canSell = True
                        canBuy = False
                        buyPrice = price
                elif canSell and (price > buyPrice*_3 or price < buyPrice*_4):
                        core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                        canSell = False
                        canBuy = True

            dtit += datetime.timedelta(minutes=interval)

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [ traceA,  traceB ])


    if debug == 0: # computing ROI
        A = 2
        B = 15
        C = 1.03
        D = 0.95
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
        D = 0.95
        (proc, portfolio, traces) = work(A, B, C, D)
        print("ROI: (%i, %i %f %f) %f" % (A,B,C,D, proc['_']['ROI%']))
        core.portfolioToChart_OHLC(portfolio, traces)


if __name__ == '__main__':
    debug = 2
    run(debug)