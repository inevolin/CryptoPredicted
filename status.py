from datetime import datetime
import json
import DAL
import pprint
from mysettings import dtNow
from math import floor
import sys
from smtp import send_email_server

mailer = False
def whoIsAlive():
	#print(dtNow())
	client = DAL.openConnection()
	cursor = DAL.liveness_getAll(client)
	results = list(cursor)
	for d in results:
		d['last_notif_min'] = floor((dtNow() - d["timestamp"]).total_seconds()/60) # how many seconds ago last received
		d['last_notif_sec'] = floor((dtNow() - d["timestamp"]).total_seconds()) # how many seconds ago last received
		if d['name'] == "producer: news":
			d['status'] = True if d['last_notif_min'] < 25 else False
		elif d['name'] == "producer: predictions":
			d['status'] = True if d['last_notif_min'] < 61 else False
		elif d['name'] == "producer: telegram":
			d['status'] = True if d['last_notif_min'] < 60 else False

		elif d['name'] == "worker: news":
			d['status'] = True if d['last_notif_min'] < 120 else False
		elif d['name'] == "worker: sentiments news":
			d['status'] = True if d['last_notif_min'] < 120 else False

		else:
			d['status'] = True if d['last_notif_min'] < 3 else False
		del d['timestamp']
		del d['_id']

		if mailer and not d['status']:
			send_email_server("Module ("+d['name']+") is offline", "last notif minutes: " + str(d['last_notif_min']))

	results = sorted(results, key=lambda x: x['name'])
	return results

def databaseCounts():
	client = DAL.openConnection()
	db = DAL.selectDB(client)
	counts = []
	for i,name in enumerate(db.collection_names()):
		counts.append( {'name': name, 'count': db[name].find().count() } ) 
	counts = sorted(counts, key=lambda x: x['name'])
	return counts

if len(sys.argv) < 2:
	print("error: missing argument(s) [liveness, database]")
	exit()

out = {}
if 'mailer' in sys.argv:
	mailer = True
if 'liveness' in sys.argv:
	out['liveness'] = whoIsAlive()
if 'database' in sys.argv:
	out['database'] = databaseCounts()


print(json.dumps(out))
