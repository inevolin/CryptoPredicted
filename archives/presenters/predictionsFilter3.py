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

if not len(sys.argv) >= 2:
    print("expected crypto parameter, e.g. BTC [interval mins]")
    sys.exit(0)

INTERVAL = 30
if len(sys.argv) >= 3:
    INTERVAL = int(sys.argv[2])

currentDateTime = dtNow().replace(second=0,microsecond=0)
if len(sys.argv) >= 5:
    currentDateTime = datetime.datetime.strptime(sys.argv[4], '%Y-%m-%dT%H:%M') # in future the user may send datetime from another tz, use dtLocal()
    if currentDateTime > dtNow():
        currentDateTime = dtNow().replace(second=0,microsecond=0)

maxDateTimeExcluded = currentDateTime
if INTERVAL > 1: #  and INTERVAL <= 60
    maxDateTimeExcluded = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % INTERVAL))

WINDOW = 1440
if len(sys.argv) >= 4: # value in minutes
    WINDOW = int(sys.argv[3])
minDateTimeIncluded = maxDateTimeExcluded - datetime.timedelta(minutes=WINDOW)

featuresID = None
if len(sys.argv) >= 6:
    featuresID = sys.argv[5]
else:
    print("missing featuresID")
    exit()

batchsize = None
if len(sys.argv) >= 7:
    batchsize = int(sys.argv[6])
else:
    print("missing batchsize")
    exit()

neurons = None
if len(sys.argv) >= 8:
    neurons = int(sys.argv[7])
else:
    print("missing neurons")
    exit()

windowsize = None
if len(sys.argv) >= 9:
    windowsize = int(sys.argv[8])
else:
    print("missing windowsize")
    exit()

n_epoch = None
if len(sys.argv) >= 10:
    n_epoch = int(sys.argv[9])
else:
    print("missing n_epoch")
    exit()

predicted_feature = None
if len(sys.argv) >= 11:
    predicted_feature = sys.argv[10]
else:
    print("missing predicted_feature")
    exit()


n_hiddenlay = None
if len(sys.argv) >= 12:
    n_hiddenlay = int(sys.argv[11])
else:
    print("missing n_hiddenlay")
    exit()


FINAL_predic = {}
FINAL_predic_traindata = {}


#### PREDICTIONS

pipeline = [
        {'$match' : 
            {   'crypto':       { '$eq' : sys.argv[1] },
                'timestamp':    { '$eq': maxDateTimeExcluded },
                'interval':     { '$eq': INTERVAL },
                '$or':          [{'feature': predicted_feature}, {'feature': predicted_feature+'_traindata'}],     
            }
        },
    ]
if (featuresID != "-1"):
    pipeline[0]['$match']['featuresID'] = { '$eq': featuresID }
if (batchsize != -1):
    pipeline[0]['$match']['n_batch_size'] = { '$eq': batchsize }
if (neurons != -1):
    pipeline[0]['$match']['n_neurons'] = { '$eq': neurons }
if (windowsize != -1):
    pipeline[0]['$match']['n_window'] = { '$eq': windowsize }
if (n_epoch != -1):
    pipeline[0]['$match']['n_epoch'] = { '$eq': n_epoch }
if (n_hiddenlay != -1):
    pipeline[0]['$match']['n_hiddenlayers'] = { '$eq': n_hiddenlay }

cursor = db.get_collection('predictions3').aggregate(pipeline);
res_predic = list(cursor)
# pre-process:
for obj in res_predic:
    for e in obj['data']:

        e['price'] = None # predicted data
        e['label_dt'] = e['timestamp']-datetime.timedelta(minutes=INTERVAL) 
        del e['timestamp']
        e['start'] = str(e['label_dt'])
        e['end'] = str(e['label_dt'] + datetime.timedelta(minutes=INTERVAL))
        e['label'] = str(datetime.datetime.strftime(e['label_dt'], '%Y-%m-%dT%H:%M'))


        uid = obj['featuresID']+' '+str(obj['n_epoch'])+' '+str(obj['n_window'])+' '+str(obj['n_neurons'])+' '+str(obj['n_batch_size'])+' '+str(obj['n_hiddenlayers'])

        if obj['feature'] == predicted_feature:
            if not uid in FINAL_predic:
                FINAL_predic[uid] = []
            FINAL_predic[uid].append(e)
        else:
            if not uid in FINAL_predic_traindata:
                FINAL_predic_traindata[uid] = []
            FINAL_predic_traindata[uid].append(e)

for key in FINAL_predic.keys():
     FINAL_predic[key] = sorted(FINAL_predic[key], key=(lambda x:( x['label_dt'] ) ))

for key in FINAL_predic_traindata.keys():
     FINAL_predic_traindata[key] =     sorted(FINAL_predic_traindata[key], key=(lambda x:( x['label_dt'] ) ))


# post-process:
for e, arr in FINAL_predic.items():
    for ee in arr:
        del ee['label_dt']
for e, arr in FINAL_predic_traindata.items():
    for ee in arr:
        del ee['label_dt']



json_out = json.dumps( {'predictions': FINAL_predic, 'predictions_traindata': FINAL_predic_traindata} )
print(json_out)

