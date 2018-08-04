import datetime
import pprint
import sys
import json
import time
import copy
import collections
import urllib.request
from itertools import chain

import os
os.environ.setdefault('PATH', '') # fix numpy execution from php bug
import sys
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/')
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/presenters/')
from mysettings import dtNow
import DAL

import numpy as np


def init(crypto, INTERVAL, historymins, currentDateTime):
    currentDateTime = datetime.datetime.strftime(currentDateTime, "%Y-%m-%dT%H:%M")
    url = "http://cryptopredicted.com/api.php?type=priceChart&coin="+crypto+"&interval="+str(INTERVAL)+"&historymins="+str(historymins)+"&currentDateTime="+currentDateTime
    print(url)
    out = urllib.request.urlopen(url)
    js = json.loads(out.read().decode(out.info().get_param('charset') or 'utf-8'), object_pairs_hook=collections.OrderedDict)
    return js


def getPriceData(coin, interval, historymins, _dt):
    try:
        currentDateTime = _dt.replace(second=0,microsecond=0) #- timedelta(minutes=interval)
        currentDateTime = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % interval))
        currentDateTime_T = datetime.datetime.strftime(currentDateTime, '%Y-%m-%dT%H:%M')
        print(str(currentDateTime_T))
        import currencyFilter as cm
        curr = cm.main([' ', coin, str(interval), historymins, currentDateTime_T ])
        return curr
    except KeyboardInterrupt:
        raise
    except:
        return None

def getVolumeData(coin, interval, historymins, _dt):
    try:
        currentDateTime = _dt.replace(second=0,microsecond=0) #- timedelta(minutes=interval)
        currentDateTime = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % interval))
        currentDateTime_T = datetime.datetime.strftime(currentDateTime, '%Y-%m-%dT%H:%M')
        print(str(currentDateTime_T))
        import volumeFilter as cm
        curr = cm.main([' ', coin, str(interval), historymins, currentDateTime_T ])
        return curr
    except KeyboardInterrupt:
        raise
    except:
        return None


def priceAggregDayHours():
    interval = 2
    coin = "BTC"
    historymins = 60*24*14
    dtend = datetime.datetime.strptime('2018-02-27 00:00', '%Y-%m-%d %H:%M')
    inp = getPriceData(coin, interval, historymins, dtend)

    buckets = {}
    maxP = 0
    for o in inp:
    	tss = o['label']
    	ts = datetime.datetime.strptime(tss, '%Y-%m-%dT%H:%M')
    	H = datetime.datetime.strftime(ts, '%H')
    	if not H in buckets: buckets[H] = []
    	if o['avg'] != None:
    		buckets[H].append(o['avg'])
    		if o['avg'] > maxP:
    			maxP = o['avg']

    minP = None
    maxP = None
    for k,v in sorted(buckets.items()):
    	v = sum(v)/len(v)
    	buckets[k]=v
    	if minP == None or v < minP: minP=v
    	if maxP == None or v > maxP: maxP=v
    for k,v in sorted(buckets.items()):
    	print(k+"\t"+str( (v-minP)/(maxP-minP) ))

def volumeAggregDayHours():
    interval = 2
    coin = "BTC"
    historymins = 60*24*14
    dtend = datetime.datetime.strptime('2018-02-27 00:00', '%Y-%m-%d %H:%M')
    inp = getVolumeData(coin, interval, historymins, dtend)
    
    buckets_24h = {}
    buckets_delta = {}
    for o in inp:
    	tss = o['label']
    	ts = datetime.datetime.strptime(tss, '%Y-%m-%dT%H:%M')
    	H = datetime.datetime.strftime(ts, '%H')
    	if not H in buckets_24h: buckets_24h[H] = []
    	if not H in buckets_delta: buckets_delta[H] = []
    	if o['avg'] != None:
    		buckets_24h[H].append(o['avg'])
    		buckets_delta[H].append(o['avg_delta'])

    print("24h:")
    minP = None
    maxP = None
    for k,v in sorted(buckets_24h.items()):
    	v = sum(v)/len(v)
    	buckets_24h[k]=v
    	if minP == None or v < minP: minP=v
    	if maxP == None or v > maxP: maxP=v
    for k,v in sorted(buckets_24h.items()):
    	print(k+"\t"+str( (v-minP)/(maxP-minP) ))

    print("")
    print("delta:")
    minP = None
    maxP = None
    for k,v in sorted(buckets_delta.items()):
    	v = sum(v)/len(v)
    	buckets_delta[k]=v
    	if minP == None or v < minP: minP=v
    	if maxP == None or v > maxP: maxP=v
    for k,v in sorted(buckets_delta.items()):
    	print(k+"\t"+str( (v-minP)/(maxP-minP) ))

priceAggregDayHours()
#volumeAggregDayHours()


