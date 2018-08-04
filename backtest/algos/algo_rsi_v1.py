import json
import sys
sys.dont_write_bytecode = True

import numpy as np
import datetime
import random
import math
import core

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

def work(dtstart, dtend, inp, interval, uncertainty_margin, _1, _2, _3):
    portfolio = {}
    dtit = dtstart

    traceA = core.createNewScatterTrace("traceA", "y2")
    traceB = core.createNewScatterTrace("traceB", "y2")
    traceC = core.createNewScatterTrace("traceC", "y2")
    traceD = core.createNewScatterTrace("traceD", "y2")
    
    usage = {
        'canBuy': True,
        'canSell': False,

        'buyPrice': None,
        'sellPrice': None,
        'prevPrice': None,
        
        'prevClose': None,
    }
    bucket_gain=[]
    bucket_loss=[]
    counter = 0
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

            if usage['prevClose']:
                dx = price-usage['prevClose']
                if (dx > 0):
                    bucket_gain.append(abs(dx)) # dummy
                    core.addToScatterTrace(traceA, dtit, 1)
                else:
                    bucket_loss.append(abs(dx))
                    core.addToScatterTrace(traceA, dtit, -1)
                
                counter+=1
                if counter > _1:
                    # print(bucket_gain)
                    # print(bucket_loss)
                    aGain = np.average(bucket_gain[-_1:]) if len(bucket_gain[-_1:])>0 else 0
                    aLoss = np.average(bucket_loss[-_1:]) if len(bucket_loss[-_1:])>0 else 0
                    #aGain = sig(_1, np.average(bucket_gain[-_1:-1]), bucket_gain[-1])  if len(bucket_gain[-_1:])>0 else 0
                    #aLoss = sig(_1, np.average(bucket_loss[-_1:-1]), bucket_loss[-1])  if len(bucket_loss[-_1:])>0 else 0
                    if (aLoss != 0):

                        RSI = (100-(100/(1+(aGain/aLoss))))
                        #if (abs(RSI) > 100): print(aGain, aLoss)
                        core.addToScatterTrace(traceB, dtit, RSI)

                    if len(traceB['y']) > 0:
                        p = 10 if np.average(traceB['y'][-10:]) > traceB['y'][-1] else 0
                        core.addToScatterTrace(traceC, dtit, p)
                        

            def buyF():
                if len(traceC['y']) <= 1: return False
                # if traceC['y'][-1] < 35: return False
                # if traceC['y'][-1] > 60: return False

                # if np.average(traceC['y'][-5:]) > traceC['y'][-1]: return False

                # #if traceC['y'][-2] > traceD['y'][-2] and traceC['y'][-1] < traceD['y'][-1]:
                # if traceC['y'][-2] < traceD['y'][-2] and traceC['y'][-1] > traceD['y'][-1]:
                #     return True
                #return False
                if np.average(traceC['y'][-5:]) > 6:
                    return True

            def sellF():
                if price > usage['buyPrice']*_2 and not buyF() :
                    return True 
                if price < usage['buyPrice']*_3:
                    return True
                
            if counter > _1:    
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

            usage['prevPrice'] = price
            usage['prevClose'] = c

        dtit += datetime.timedelta(minutes=interval)

    proc = core.processPortfolio(portfolio, 1)
    return (proc, portfolio, [traceA, traceB, traceC, traceD ])

def run(debug):

    base = "BTC"
    base = "ETH"
    base = "LTC"

    quote = "USDT"
    historymins = 60*6#60*24*1 #60*24*30*1 #60*24*30*4
    interval = 1 #60
    #dtend = datetime.datetime.strptime('2018-05-02 15:00', '%Y-%m-%d %H:%M')
    dtend = datetime.datetime.strptime('2018-05-24 12:30', '%Y-%m-%d %H:%M')

    dtstart = dtend - datetime.timedelta(minutes=historymins)
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    #inp = json.load(open('misc/json_BTCUSDT_60min.json'))
    #uncertainty_margin = 0.001
    uncertainty_margin = 0.0005 # slippage

    if debug == 0: # computing ROI
        A = 2
        B = 1.007
        C = 0.993
        avgs = []
        for x in range(100):
            (proc, portfolio, traces) = work(dtstart, dtend, inp, interval, uncertainty_margin, A, B, C)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    elif debug == 1: # brute-force searching for optimal parameters (A,B,C,D)
        dct = {}
        for A in range(2, 10):
            for B in [1+x/1000 for x in range(3, 10)]:
                for C in [0.99+x/1000 for x in range(3, 10)]:
                    #if (B <= A): continue
                    avgs = []
                    for x in range(1):
                        (proc, portfolio, traces) = work(dtstart, dtend, inp, interval, uncertainty_margin, A, B, C)
                        #print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
                        avgs.append(proc['_']['ROI%'])

                    if sum(avgs)/len(avgs) < 0: continue # skip negatives

                    print("%f %f %f %f %f %f" % (A,B,C,D,E,F))
                    print("avg ROI%: " + str(sum(avgs)/len(avgs)))
                    std = np.std(avgs)
                    #print("std ROI%: " + str(std))

                    if not str(sum(avgs)/len(avgs)) in dct:
                        dct [ str(sum(avgs)/len(avgs)) ] = str(A)+"_"+str(B)+"_"+str(C)

                                
        print("--------")
        print(base)
        print("--------")
        print(json.dumps(dct))
        print("--------")
        print(base)
    
    else: # computing and plotting out
        shapes = [
            {
                'type': 'line',
                'xref': 'x',
                'yref': 'y2',
                'x0': datetime.datetime.strftime(dtstart, '%Y-%m-%dT%H:%M'),
                'x1': datetime.datetime.strftime(dtend, '%Y-%m-%dT%H:%M'),
                'y0': 50,
                'y1': 50,
                'line': {
                    'color': 'gray',
                    'width': 3,
                    'dash': 'dash'
                },
            },
            {
                'type': 'line',
                'xref': 'x',
                'yref': 'y2',
                'x0': datetime.datetime.strftime(dtstart, '%Y-%m-%dT%H:%M'),
                'x1': datetime.datetime.strftime(dtend, '%Y-%m-%dT%H:%M'),
                'y0': 70,
                'y1': 70,
                'line': {
                    'color': 'gray',
                    'width': 2,
                },
            },
            {
                'type': 'line',
                'xref': 'x',
                'yref': 'y2',
                'x0': datetime.datetime.strftime(dtstart, '%Y-%m-%dT%H:%M'),
                'x1': datetime.datetime.strftime(dtend, '%Y-%m-%dT%H:%M'),
                'y0': 30,
                'y1': 30,
                'line': {
                    'color': 'gray',
                    'width': 2,
                },
            },
        ]
        A = 7
        B = 1.002
        C = 0.991
        (proc, portfolio, traces) = work(dtstart, dtend, inp, interval, uncertainty_margin, A, B, C)
        print("ROI: (%i, %i) %f" % (A, B, proc['_']['ROI%']))
        core.portfolioToChart_OHLC(portfolio, traces, shapes=shapes)


if __name__ == '__main__':
    debug = 2
    run(debug)
