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

	client = DAL.openConnection()
	db=client.crypto

	if not len(args) >= 2:
		print("expected crypto parameter, e.g. BTC [interval mins]")
		sys.exit(0)

	INTERVAL_GRAPH_mentionsBasic = 60 # 60 minutes default
	if len(args) >= 3:
	    INTERVAL_GRAPH_mentionsBasic = int(args[2])

	currentDateTime = dtNow().replace(second=0,microsecond=0)
	if len(args) >= 5:
		currentDateTime = datetime.datetime.strptime(args[4], '%Y-%m-%dT%H:%M') # in future the user may send datetime from another tz, use dtLocal()
		if currentDateTime > dtNow():
			currentDateTime = dtNow().replace(second=0,microsecond=0)

	# create correct min and max according to total window size and intervals: [min, max[
	maxDateTimeExcluded = currentDateTime
	if INTERVAL_GRAPH_mentionsBasic > 1:
		maxDateTimeExcluded = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % INTERVAL_GRAPH_mentionsBasic))

	WINDOW = 1440
	if len(args) >= 4: # value in minutes
		WINDOW = int(args[3])
	minDateTimeIncluded = maxDateTimeExcluded - datetime.timedelta(minutes=WINDOW)


	if INTERVAL_GRAPH_mentionsBasic < 60:
		def adjust_func(e): e['label'] = 	str(e['_id']['year']).zfill(4)  + '-' +\
											str(e['_id']['month']).zfill(2)  + '-' +\
											str(e['_id']['day']).zfill(2)  + 'T' +\
											str(e['_id']['hour']).zfill(2)  + ':' +\
											str(e['_id']['interval']).zfill(2) 
		interval = {
			'year': {'$year' : '$timestamp'},
			'month': {'$month' : '$timestamp'},
			'day': {'$dayOfMonth' : '$timestamp'},
			'hour': {'$hour' : '$timestamp'},
			'interval' : { # create 15-minute intervals: [0-15[ ; [15-30[ ; [30-45[ ; [45-60[
				'$subtract' : [ 
					{'$minute' : '$timestamp'},
					{'$mod':[{'$minute' : '$timestamp'}, INTERVAL_GRAPH_mentionsBasic]}
				]
			}
		}
	elif INTERVAL_GRAPH_mentionsBasic >= 60 and INTERVAL_GRAPH_mentionsBasic < 1440: # hour interval
		def adjust_func(e): e['label'] = 	str(e['_id']['year']).zfill(4)  + '-' +\
											str(e['_id']['month']).zfill(2)  + '-' +\
											str(e['_id']['day']).zfill(2)  + 'T' +\
											str(e['_id']['interval']).zfill(2)  + ':00'
		interval = {
			'year': {'$year' : '$timestamp'},
			'month': {'$month' : '$timestamp'},
			'day': {'$dayOfMonth' : '$timestamp'},
			'interval' : { 
				'$subtract' : [ 
					{'$hour' : '$timestamp'},
					{'$mod':[{'$hour' : '$timestamp'}, int(INTERVAL_GRAPH_mentionsBasic/60)]}
				]
			}
		}
	else:
		def adjust_func(e): e['label'] = 	str(e['_id']['year']).zfill(4)  + '-' +\
											str(e['_id']['month']).zfill(2)  + '-' +\
											str(e['_id']['day']).zfill(2)  + 'T00:00'
		interval = {
			'year': {'$year' : '$timestamp'},
			'month': {'$month' : '$timestamp'},
			'day': {'$dayOfMonth' : '$timestamp'},
		}

	pipeline = [
			{'$match' : 
				{	'fromSymbol' :
						{	'$eq' : args[1] },
					'timestamp': {
							'$gte': minDateTimeIncluded,
							'$lt': maxDateTimeExcluded,
						}
				}
			},
			{'$group' : 
				{	'_id' : {	},
		        	'avg' : {'$avg':'$fromVol24_sum'},
	 			}
	    	}
	    ]
	pipeline[1]['$group']['_id'] = interval
	#print(pipeline)


	cursor = db.get_collection('volumes').aggregate(pipeline);
	result = list(cursor)
	FINAL = []

	# pre-process:
	for e in result:
		adjust_func(e)
		e['label_dt'] = datetime.datetime.strptime(e['label'], '%Y-%m-%dT%H:%M')

		if e['label_dt']< minDateTimeIncluded or (e['label_dt'] + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic)) > maxDateTimeExcluded:
			continue

		e['start'] = str(e['label_dt'])
		e['end'] = str(e['label_dt'] + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic))
		e['label'] = str(datetime.datetime.strftime(e['label_dt'], '%Y-%m-%dT%H:%M')) # + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic)
		e.pop('_id', None)
		FINAL.append(e)


	# add missing intervals
	tmp_datetime = min( [x['label_dt'] for x in FINAL] ) # we need smallest interval, not just minDateTimeIncluded
	while(tmp_datetime+ datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic) < maxDateTimeExcluded):
		contains = False
		for e in FINAL:
			if e['label_dt'] == tmp_datetime:
				contains = True
				break
		if not contains:
			e_tmp = copy.copy(FINAL[0])
			e_tmp['label_dt'] = tmp_datetime
			e_tmp['start'] = str(e_tmp['label_dt'])
			e_tmp['end'] = str(e_tmp['label_dt'] + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic))
			e_tmp['label'] = str(datetime.datetime.strftime(tmp_datetime, '%Y-%m-%dT%H:%M')) # + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic)
			e_tmp['avg'] = None
			e_tmp['avg_delta'] = None
			FINAL.append(e_tmp)
		tmp_datetime = tmp_datetime + datetime.timedelta(minutes=INTERVAL_GRAPH_mentionsBasic)


	# sort list :
	sorted_list = 	sorted(FINAL, key=(lambda x:( x['label_dt'] ) ))
	FINAL = []

	# post-process:
	prev_avg = None
	for e in sorted_list:
		if e['avg'] != None:
			e['avg'] = round(e['avg'],2)
			if prev_avg == None:
				e['avg_delta'] = 0
			else:
				e['avg_delta'] = round(e['avg']-prev_avg,2)
			prev_avg = e['avg']
		
		del e['label_dt']
		FINAL.append(e)



	return FINAL


if __name__ == '__main__':
	FINAL = main()
	json_out = json.dumps(FINAL)
	print(json_out)
