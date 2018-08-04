import datetime
import pprint
import pymongo
import pprint
import json
import random
import time
from pymongo import MongoClient

import sys
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/')

import DAL

client = DAL.openConnection()
db=client.crypto

if not len(sys.argv) == 4:
	print("parameters: crypto 'datetime' GraphInterval")
	sys.exit(0)


INTERVAL_GRAPH_mentionsBasic = int(sys.argv[3])
datetimeClicked = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M') # in future the user may send datetime from another tz, use dtLocal()
GRAPH_DATA_SHOW_PAST_INTERVAL_min = datetimeClicked
GRAPH_DATA_SHOW_PAST_INTERVAL_max = GRAPH_DATA_SHOW_PAST_INTERVAL_min + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic)

#print(GRAPH_DATA_SHOW_PAST_INTERVAL_min)
#print(GRAPH_DATA_SHOW_PAST_INTERVAL_max)
#sys.exit(0)

pipeline =  [
				{'$project': { # everything used in match should be projected!
					'url':1,
					'source':1,
					'body':1,
					'crypto': 1,
					'timestamp': 1,
				}},
				{'$match': {
					'crypto' : {
						'$eq' : sys.argv[1]
					},
					'timestamp': {
						'$gte': GRAPH_DATA_SHOW_PAST_INTERVAL_min,
						'$lte': GRAPH_DATA_SHOW_PAST_INTERVAL_max,
					},
				}},
				{'$group': { '_id' : {
					'url': '$url', 
					'source': '$source', 
					'body': '$body', 
					'crypto': '$crypto', 
					#'timestamp': '$timestamp'
				}}},
				{'$sort': { 'timestamp': -1 }}, # sort descending (newest first)
				{'$limit': 100}, # limit to 100
			]

cursor = db.get_collection('mentionsExtendedSocial').aggregate(pipeline);
result = list(cursor)
#print(len(result))
#pprint.pprint((result))
#sys.exit(0)

FINAL = []
for key, val in enumerate(result):
	for k in val['_id']:
		val[k] = val['_id'][k]
	#val['timestamp'] = datetime.datetime.strftime(val['timestamp'], '%Y-%m-%dT%H:%M')
	del val['_id']
	FINAL.append(val)

#sys.exit(0)s

#pp.pprint(sorted_list)
#print("### mentions ### most recent:")
#pprint.pprint(FINAL)

print(json.dumps(FINAL))
