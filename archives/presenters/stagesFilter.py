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

client = DAL.openConnection()
db=client.crypto

currentDateTime = dtNow().replace(second=0,microsecond=0)
if len(sys.argv) >= 3:
	currentDateTime = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M') # in future the user may send datetime from another tz, use dtLocal()
	if currentDateTime > dtNow():
		currentDateTime = dtNow().replace(second=0,microsecond=0)

# create correct min and max according to total window size and intervals: [min, max[
maxDateTimeExcluded = currentDateTime

WINDOW = 1440
if len(sys.argv) >= 2: # value in minutes
	WINDOW = int(sys.argv[1])
minDateTimeIncluded = maxDateTimeExcluded - datetime.timedelta(minutes=WINDOW)


FINAL = {}

pipeline = [
		{'$match' : 
			{
				'timestamp': {
						'$gte': minDateTimeIncluded,
						'$lt': maxDateTimeExcluded,
					}
			}
		},
		{'$group' : 
			{	'_id': {'crypto': '$crypto'},
	        	'avg' : {'$avg':'$USD'},
 			}
    	}
    ]
cursor = db.get_collection('currencies').aggregate(pipeline);
res_currencies = list(cursor)
FINAL['currencies']=res_currencies



pipeline = [
		{'$match' : 
			{
				'timestamp': {
						'$gte': minDateTimeIncluded,
						'$lt': maxDateTimeExcluded,
					}
			}
		},
		{'$group' : 
			{	'_id': {'crypto': '$fromSymbol'},
	        	'avg' : {'$avg':'$fromVol24_sum'},
 			}
    	}
    ]
cursor = db.get_collection('volumes').aggregate(pipeline);
res_currencies = list(cursor)
FINAL['volumes']=res_currencies



pipeline = [
		{'$match' : 
			{
				'timestamp': {
						'$gte': minDateTimeIncluded,
						'$lt': maxDateTimeExcluded,
					}
			}
		},
		{'$group' : 
			{	'_id': {'crypto': '$crypto'},
	        	'sum' : {'$sum':'$mentions'},
 			}
    	}
    ]
cursor = db.get_collection('mentionsSocial').aggregate(pipeline);
res_socialHype = list(cursor)
FINAL['socialHype']=res_socialHype


pipeline = [
		{'$match' : 
			{
				'timestamp': {
						'$gte': minDateTimeIncluded,
						'$lt': maxDateTimeExcluded,
					}
			}
		},
		{'$group' : 
			{	'_id': {'crypto': '$crypto'},
	        	'sum' : {'$sum':'$mentions'},
 			}
    	}
    ]
cursor = db.get_collection('mentionsNews').aggregate(pipeline);
res_newsHype = list(cursor)
FINAL['newsHype']=res_newsHype



json_out = json.dumps(FINAL)
print(json_out)

