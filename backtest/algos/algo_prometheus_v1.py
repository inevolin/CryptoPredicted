
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
    historymins = 60*24*30*1 #60*24*30*4
    interval = 60
    dtend = datetime.datetime.strptime('2018-04-26 15:00', '%Y-%m-%d %H:%M')
   # dtend = datetime.datetime.strptime('2018-05-17 12:00', '%Y-%m-%d %H:%M')
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

    def work(_1, _2, _3):
        portfolio = {}
        dtit = dtstart

        traceD = core.createNewScatterTrace("traceD", "y2")
        
        usage = {
            'canBuy': True,
            'canSell': False,

            'buyPrice': None,
            'sellPrice': None,
            'prevPrice': None,
        }
        bucket=[]
        bucketstd = []
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
                price = random.uniform(l, h)  # reality

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)


                
                def buyF():
                    if len(traceD['y']) < 2:
                        return False
                    if traceD['y'][-2] == 1 and traceD['y'][-1] == -1:
                        return True
                    #if traceD['y'][-1] == 1 and traceD['y'][-2] == -1:
                    #    return True
                def sellF():
                    if price > usage['buyPrice']*_1:
                        return True 
                    if price < usage['buyPrice']*_2:
                        return True
                    
                
                if len(bucket) > 2:    
                    pD = np.average(bucket[-_3:])
                    pD = 1 if pD > 1 else -1
                    core.addToScatterTrace(traceD, dtit, pD)

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
                            usage['countSinceSell'] = 0

                
                if usage['prevPrice'] != None:
                    bucket.append( price/ usage['prevPrice'] )

                usage['prevPrice'] = price

            dtit += datetime.timedelta(minutes=interval)

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceD ])


    if debug == 0: # computing ROI
        A = 1.03
        B = 0.96
        C = 16
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work(A,B,C)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    
    elif debug == 1: # brute-force searching for optimal parameters (A,B,C,D)
        dct = {}
        for A in [1+x/100 for x in range(1, 6)]:
            for B in [0.95+x/100 for x in range(0, 5)]:
                for C in range(1, 20):
                    avgs = []
                    for x in range(20):
                        (proc, portfolio, traces) = work(A,B,C)
                        #print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
                        avgs.append(proc['_']['ROI%'])

                    print("%f %f %f" % (A,B,C))
                    print("avg ROI%: " + str(sum(avgs)/len(avgs)))
                    std = np.std(avgs)
                    print("std ROI%: " + str(std))

                    if not str(sum(avgs)/len(avgs)) in dct:
                        dct [ str(sum(avgs)/len(avgs)) ] = str(A)+"_"+str(B)+"_"+str(C)
        print("--------")
        print(base)
        print("--------")
        print(json.dumps(dct))
        print("--------")
        print(base)
    
    else: # computing and plotting out
        # A = 1.02
        # B = 0.98
        # C = 9
        A = 1.03
        B = 0.97
        C = 16
        (proc, portfolio, traces) = work(A, B, C)
        print("ROI: (%f %f %i) %f" % (A, B, C, proc['_']['ROI%']))
        core.portfolioToChart_OHLC(portfolio, traces)


if __name__ == '__main__':
    debug = 0
    run(debug)