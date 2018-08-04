import sys
sys.dont_write_bytecode = True

import numpy as np
import datetime
import random
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
    historymins = 60*24*30*3 #60*24*30*4
    dtend = datetime.datetime.strptime('2018-04-18 00:00', '%Y-%m-%d %H:%M')
    dtstart = dtend - datetime.timedelta(minutes=historymins)
    interval = 60
    inp = core.getPriceExchange_v1('binance', interval, base, quote, historymins, dtend)
    uncertainty_margin = 0.001
    slope_pct_threshold = 0.3

    def work(dtstart, dtend):
        portfolio = {}
        prevPrice = None
        slopes = []
        dtit = dtstart
        while dtit < dtend:
            idx = datetime.datetime.strftime(dtit, '%Y-%m-%dT%H:%M')
            if idx in inp:
                c = inp[idx]['close']
                o = inp[idx]['open']
                l = inp[idx]['low']
                h = inp[idx]['high']

                # let price be any random value in range [open, close]
                # price = random.uniform(o, c) if c > o else random.uniform(c, o) 
                # price = random.uniform(l, h)  # much worse than [open, close]
                # let the price be any random value in range [open ; (close-open)*x ] where x is in range [0.0 ; 1.0]
                price = o + (c-o)*random.randint(0,10)/10
                # this strategy seems to stop working when we use range [low, high]
                # however in reality there is a chance the system takes near-low/high values, as a result the ROI will be low or even negative.
                buyprice = price 
                sellprice = price

                core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h)
                if prevPrice != None:
                    slope_pct = round((price-prevPrice)/prevPrice*100,2)
                    slopes.append(slope_pct)
                    if price > prevPrice:
                        slopes.append( slope_pct )
                        avgS = sum(slopes)/len(slopes)
                        if avgS > slope_pct_threshold : # len(slopes) > 1 and
                            # buy
                            core.portfolioBuy(portfolio, dtit, buyprice, uncertainty_margin)
                    else:
                        if len(slopes) > 0:
                            # sell
                            core.portfolioSell(portfolio, dtit, sellprice, uncertainty_margin)
                        slopes = []

                prevPrice = c

            dtit += datetime.timedelta(minutes=interval)
            
        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio)

    if debug == 0:
        avgs = []
        for x in range(100):
            (proc, portfolio) = work(dtstart, dtend)
            print("%s ROI \t %f" % (str(x), proc['_']['ROI%']))
            avgs.append(proc['_']['ROI%'])

        print("avg ROI%: " + str(sum(avgs)/len(avgs)))
        std = np.std(avgs)
        print("std ROI%: " + str(std))
    
    else:
        (proc, portfolio) = work(dtstart, dtend)
        print("ROI: %f" % proc['_']['ROI%'])
        core.portfolioToChart_OHLC(portfolio)

if __name__ == '__main__':
    debug = 0
    run(debug)