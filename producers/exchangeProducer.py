
# exchange producer: getting data from exchanges (OHLC and Volume)
# until now only Binance exchange was scraped.
# if you are going to expand to more exchanges, then instead use a public library like:
# https://github.com/ccxt/ccxt
# the  CCXT project has dozens (if not hundreds) of exchange APIs all idone for you (and free).
# I would also advise you to get rid of Python and use NodeJS workers instead.

import datetime
import pprint
import json
import time
import collections
import urllib.request

import threading
import sys
sys.path.insert(0, '/home/cryptopredicted/')
from mysettings import dtNow, createLogger
import DAL

log = createLogger("exchangeProducer_info", "exchangeProducer_info")
logErr = createLogger("exchangeProducer_err", "exchangeProducer_err")


fillFromHistory = False

class upserter (threading.Thread):
    def __init__(self, client, newData, ts, exchange, base_cur, quote_cur):
        threading.Thread.__init__(self)
        self.client = client
        self.newData = newData
        self.ts = ts
        self.exchange = exchange
        self.base_cur = base_cur
        self.quote_cur = quote_cur
    def run(self):
        try:
            DAL.upsert_exchangeCurrency(self.client, self.base_cur, self.quote_cur, self.newData, self.ts, self.exchange)
            print("upserted: " + str(self.ts))
            log.info("upserted: " + str(self.ts))
        except Exception as ex:
            logErr.info(ex)
            print(ex)

class binance (threading.Thread):
    def __init__(self, dtnow, dbclient, base_cur, quote_cur):
        threading.Thread.__init__(self)
        self.dtnow = dtnow
        self.client=dbclient
        self.base_cur = base_cur
        self.quote_cur = quote_cur

    def init(self, base_cur, quote_cur, interval, fromTS, toTS):    
        symbol = base_cur + quote_cur
        url = "https://api.binance.com/api/v1/klines?symbol="+symbol+"&interval="+interval
        if fromTS != None:
            fromTS = int(fromTS.timestamp())*1000
            url += "&startTime="+str(fromTS)
        if toTS != None:
            toTS = int(toTS.timestamp())*1000
            #url += "&endTime="+str(toTS)
        print(url)
        log.info(url)
        out = urllib.request.urlopen(url)
        js = json.loads(out.read().decode(out.info().get_param('charset') or 'utf-8'), object_pairs_hook=collections.OrderedDict)
        return js

    def run(self):
        try:
            base_cur = self.base_cur
            quote_cur = self.quote_cur

            stickInterval="1m"
            currentTS=self.dtnow
            out = self.init(base_cur, quote_cur, stickInterval, currentTS, currentTS)
            
            if not fillFromHistory:
                out = out[len(out)-5:] # only keep the latest X (last X) -- reason: the most recent one will need to be updated once a new interval has started, because it will have changed due to timing.

            threads = []
            for data in out:
                ts = datetime.datetime.utcfromtimestamp(data[0]/1000)
                newData = {
                    'open': float(data[1]),
                    'close': float(data[4]),
                    'high': float(data[2]),
                    'low': float(data[3]),
                    'volume': float(data[5]),
                    'trades': int(data[8]),
                }
                #DAL.upsert_exchangeCurrency(self.client, base_cur, quote_cur, newData, ts, "binance")
                th = upserter(self.client, newData, ts, "binance", base_cur, quote_cur)
                th.start()
                threads.append(th)

            for t in threads:
                try:
                    t.join(timeout=30) # 30 sec per article
                except Exception as ex:
                    print(ex)

            DAL.liveness_IAmAlive(client, "producer: exchange")
        except Exception as ex:
            logErr.info(ex)
            print(ex)


client = DAL.openConnection()

mapping = [
    {'base':'BTC','quote':'USDT'},
    {'base':'ETH','quote':'USDT'},
    {'base':'LTC','quote':'USDT'},

    {'base':'BCC','quote':'USDT'},
    {'base':'NEO','quote':'USDT'},
]

def run():
    while(True):
        try:
            for x in range(len(mapping)):
                y = mapping[x]
                th = binance(None, client, y['base'], y['quote'])
                th.start()
        except Exception as ex2:
            print(ex2)
            logErr.info(ex2)
        time.sleep(20)

def fillUpFromHistory():

    threads = []
    dtit = datetime.datetime.strptime('2018-01-01 00:00', '%Y-%m-%d %H:%M')
    dtnow=dtNow()
    #dtnow=datetime.datetime.strptime('2018-02-09 13:00', '%Y-%m-%d %H:%M')

    while dtit <= dtnow:
        print("")
        dtnow=dtNow()
        print("dtit: " + str(dtit))
        #print("dtnow: " + str(dtnow))
        
        for x in range(len(mapping)):
            y = mapping[x]

            th = binance(dtit, client,  y['base'], y['quote'])
            th.start()
            threads.append(th)
            if len(threads) == 1:
                for t in threads:
                    try:
                        t.join(timeout=30000) # 30 sec per article
                    except Exception as ex:
                        print(ex)
                threads=[]
                time.sleep(1)

        #dtit += datetime.timedelta(seconds=20)
        dtit += datetime.timedelta(minutes=1000)

if len(sys.argv) == 2:
    if sys.argv[1] == "history":
        fillFromHistory = True
        fillUpFromHistory()
    else:
        print("error: invalid argument (use 'history')")
else:
    run()

