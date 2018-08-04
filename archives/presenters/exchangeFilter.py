import datetime
import pprint
import pymongo
import sys
import json
import time
import copy
from pymongo import MongoClient

import sys
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/')
from mysettings import dtNow
import DAL

def main(args = sys.argv):

    # by default, this retrieves all data, it does not aggregate,
    # if you wish to aggregate above 1min, then do it manually.

    client = DAL.openConnection()
    db=client.crypto

    if not len(args) >= 2:
        print("expected exchange parameter, e.g.: binance")
        sys.exit(0)
    exchange = args[1]
    
    if not len(args) >= 3:
        print("expected base currency parameter, e.g.: BTC")
        sys.exit(0)
    base_cur = args[2]

    if not len(args) >= 4:
        print("expected quote currency parameter, e.g.: USDT")
        sys.exit(0)
    quote_cur = args[3]

    if not len(args) >= 5:
        print("expected interval parameter, e.g.: 1 (=1 minute)")
        sys.exit(0)
    INTERVAL = int(args[4])

    if not len(args) >= 6:
        print("expected historymins parameter, e.g.: 60 (=60 minutes)")
        sys.exit(0)
    historymins = int(args[5])

    if not len(args) >= 7:
        print("expected currentDateTime parameter")
        sys.exit(0)
    currentDateTime = datetime.datetime.strptime(args[6], '%Y-%m-%dT%H:%M')
    if currentDateTime > dtNow():
        currentDateTime = dtNow().replace(second=0,microsecond=0)


    # create correct min and max according to total window size and intervals: [min, max[
    maxDateTimeExcluded = currentDateTime
    if INTERVAL > 1: # make sure we only retrieve complete intervals (not still evolving data) -- to prevent caching issues
        maxDateTimeExcluded = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % INTERVAL))
    minDateTimeIncluded = maxDateTimeExcluded - datetime.timedelta(minutes=historymins)


    if INTERVAL < 60:
        def adjust_func(e): e['label'] =    str(e['_id']['year']).zfill(4)  + '-' +\
                                            str(e['_id']['month']).zfill(2)  + '-' +\
                                            str(e['_id']['day']).zfill(2)  + 'T' +\
                                            str(e['_id']['hour']).zfill(2)  + ':' +\
                                            str(e['_id']['interval']).zfill(2) 
        queryinterval = {
            'year': {'$year' : '$timestamp'},
            'month': {'$month' : '$timestamp'},
            'day': {'$dayOfMonth' : '$timestamp'},
            'hour': {'$hour' : '$timestamp'},
            'interval' : { # create 15-minute intervals: [0-15[ ; [15-30[ ; [30-45[ ; [45-60[
                '$subtract' : [ 
                    {'$minute' : '$timestamp'},
                    {'$mod':[{'$minute' : '$timestamp'}, INTERVAL]}
                ]
            }
        }
    elif INTERVAL >= 60 and INTERVAL < 1440: # hour interval
        def adjust_func(e): e['label'] =    str(e['_id']['year']).zfill(4)  + '-' +\
                                            str(e['_id']['month']).zfill(2)  + '-' +\
                                            str(e['_id']['day']).zfill(2)  + 'T' +\
                                            str(e['_id']['interval']).zfill(2)  + ':00'
        queryinterval = {
            'year': {'$year' : '$timestamp'},
            'month': {'$month' : '$timestamp'},
            'day': {'$dayOfMonth' : '$timestamp'},
            'interval' : { 
                '$subtract' : [ 
                    {'$hour' : '$timestamp'},
                    {'$mod':[{'$hour' : '$timestamp'}, int(INTERVAL/60)]}
                ]
            }
        }
    else:
        def adjust_func(e): e['label'] =    str(e['_id']['year']).zfill(4)  + '-' +\
                                            str(e['_id']['month']).zfill(2)  + '-' +\
                                            str(e['_id']['day']).zfill(2)  + 'T00:00'
        queryinterval = {
            'year': {'$year' : '$timestamp'},
            'month': {'$month' : '$timestamp'},
            'day': {'$dayOfMonth' : '$timestamp'},
        }

    pipeline = [
        {'$match' : 
            {   'base_cur' : base_cur,
                'quote_cur' : quote_cur,
                'exchange':     exchange,
                'timestamp': {
                        '$gte': minDateTimeIncluded,
                        '$lt': maxDateTimeExcluded,
                    }
            }
        },
        {'$group' : 
            {   '_id' : {   },
                'low' : {'$min':'$data.low'},
                'high' : {'$max':'$data.high'},
                'open': {'$first':'$$ROOT.data.open'},
                'close': {'$last':'$$ROOT.data.close'},
                'volume':{'$sum':'$data.volume'},
                'trades':{'$sum':'$data.trades'},
                'count': {'$sum':1},
            }
        }
    ]
    pipeline[1]['$group']['_id'] = queryinterval

    cursor = db.get_collection('exchanges').aggregate(pipeline);
    FINAL = []
    for e in cursor:
        if e['count'] < INTERVAL: # make sure candlestick (if aggregated) is complete (if not, probably historymins too short, or missing data)
            continue
        adjust_func(e)
        e['label_dt'] = datetime.datetime.strptime(e['label'], '%Y-%m-%dT%H:%M')
        e['label_to'] = datetime.datetime.strftime(e['label_dt'] + datetime.timedelta(minutes=INTERVAL), '%Y-%m-%dT%H:%M')
        del e['_id']
        FINAL.append(e)


    FINAL =   sorted(FINAL, key=(lambda x:( x['label_dt'] ) ))
    for e in FINAL:
       e.pop('label_dt', None)

    return FINAL


if __name__ == '__main__':
    FINAL = main()
    json_out = json.dumps(FINAL)
    print(json_out)
