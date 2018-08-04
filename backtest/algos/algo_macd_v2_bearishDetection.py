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
    #dtend = datetime.datetime.strptime('2018-05-02 15:00', '%Y-%m-%d %H:%M')
    dtend = datetime.datetime.strptime('2018-05-24 17:00', '%Y-%m-%d %H:%M')

    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    #inp = json.load(open('misc/json_BTCUSDT_60min.json'))
    uncertainty_margin = 0.001

    def sig(prev_len, prevPrice, price):
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
  

    def work(_1, _2, _3, _4, _5, _6):
        portfolio = {}
        dtit = dtstart

        traceA = core.createNewScatterTrace("traceA", "y")
        traceA['prev_len'] = _1
        traceB = core.createNewScatterTrace("traceB", "y")
        traceB['prev_len'] = _2

        traceWL = core.createNewScatterTrace("Wins/Losses", "y2")
        traceC = core.createNewScatterTrace("traceC", "y")
        traceD = core.createNewScatterTrace("traceD", "y")
        
        usage = {
            'canBuy': True,
            'canSell': False,

            'buyPrice': None,
            'sellPrice': None,
            'prevPrice': None,

            'win': 0,
            'loss': 0,
        }
        bucket=[]
        while dtit <= dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                price = (o+c+l+h)/4   # ok
                #price = c         # ok
                #price = o + (c-o)*random.randint(0,10)/10 # ok
                #price = random.uniform(o, c) if c > o else random.uniform(c, o) 
                #price = random.uniform(l, h)  # reality

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)

                pA = sig(traceA['prev_len'], np.average(traceA['y'][-_3:]) if len(traceA['y'])>0 else (o+c)/2, (o+c)/2)
                pB = sig(traceB['prev_len'], np.average(traceB['y'][-_3:]) if len(traceB['y'])>0 else (o+c)/2, (o+c)/2)
                core.addToScatterTrace(traceA, dtit, pA)
                core.addToScatterTrace(traceB, dtit, pB)

                L = 24*4
                core.addToScatterTrace(traceC, dtit, np.average(traceA['y'][-L:])   ) # + np.std(traceA['y'][-24*4:])*0.5
                core.addToScatterTrace(traceD, dtit, np.average(traceA['y'][-L:]) - np.std(traceA['y'][-L:])*2  )


                
                bucket.append(pA) # dummy

                def buyF():
                    if traceB['y'][-1] < traceC['y'][-1]: return False # don't trade downtrend
                    if np.average(traceB['y'][-_4:]) > traceB['y'][-1]:
                        return False
                    if traceB['y'][-2] > traceA['y'][-2] and traceB['y'][-1] < traceA['y'][-1]:
                        return True
                    if traceB['y'][-1] > traceB['y'][-2]:
                        return True
                def sellF():
                    if price > usage['buyPrice']*_5 and not buyF():
                        usage['win'] += 1
                        return True 
                    if price < usage['buyPrice']*_6:
                        usage['loss'] += 1
                        return True
                    
                if len(bucket) > 2:    
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

                    core.addToScatterTrace(traceWL, dtit, 1-1/(1+(usage['win']/(1+usage['loss']))) )

                usage['prevPrice'] = price

            dtit += datetime.timedelta(minutes=interval)

        for i,v in enumerate(traceB['y']):# beautify (replacing 0's by None )
            if v == 0:
                traceB['y'][i]=None

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA, traceB, traceWL, traceC, traceD ])
        #return (proc, portfolio, [])


    if debug == 0: # computing ROI
        A = 2
        B = 15
        C = 5
        D = 10
        E = 1.02
        F = 0.97
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work(A, B, C, D, E, F)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    
    elif debug == 1: # brute-force searching for optimal parameters (A,B,C,D)
        dct = {}
        for A in range(1, 30):
            for B in range(2, 30):
                for C in range(1, 10):
                    for D in range(5, 15):
                        for E in [1+x/100 for x in range(0, 10)]:
                            for F in [0.90+x/100 for x in range(0, 10)]:
                                if (B <= A): continue
                                avgs = []
                                for x in range(20):
                                    (proc, portfolio, traces) = work(A,B,C,D,E,F)
                                    #print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
                                    avgs.append(proc['_']['ROI%'])

                                print("%f %f %f %f %f %f" % (A,B,C,D,E,F))
                                print("avg ROI%: " + str(sum(avgs)/len(avgs)))
                                std = np.std(avgs)
                                print("std ROI%: " + str(std))

                                if not str(sum(avgs)/len(avgs)) in dct:
                                    dct [ str(sum(avgs)/len(avgs)) ] = str(A)+"_"+str(B)+"_"+str(C)+"_"+str(D)+"_"+str(E)+"_"+str(F)
        print("--------")
        print(base)
        print("--------")
        print(json.dumps(dct))
        print("--------")
        print(base)
    
    else: # computing and plotting out
        A = 2
        B = 15
        C = 5
        D = 10
        E = 1.02
        F = 0.97
        (proc, portfolio, traces) = work(A, B, C, D, E, F)
        print("ROI: (%i, %i) %f" % (A, B, proc['_']['ROI%']))
        core.portfolioToChart_OHLC(portfolio, traces)


if __name__ == '__main__':
    debug = 0
    run(debug)
