import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from mysettings import createLogger, dtNow
import urllib.parse

def openConnection():
	username = urllib.parse.quote_plus('cryptopredicted')
	password = urllib.parse.quote_plus('1561_AEI_qzef26_GRZ_ez65_fezo_fze6')
	return MongoClient('mongodb://%s:%s@159.69.94.65:27017/crypto' % (username, password))

def selectDB(client):
	return client.crypto

# No, you don't need to close PyMongo connections. Leave them open so that PyMongo's connection pooling gives you the most efficient performance
# def closeConnection(client):
# 	client.close()


def store_mentions_social_extended_bulk(client, arr, ts):
	# each obj in arr : {body, crypto, source, url}
	#	 db.mentionsExtendedSocial.createIndex( { crypto: 1, url: 1, body: 1 }, { unique: true } )
	
	try:
		for a in arr:
			a['timestamp'] = ts

		db = selectDB(client)
		db.mentionsExtendedSocial.insert_many(arr, ordered=False) # ordered: If false: when a single write fails, the operation will continue with the remaining writes, if any, and throw an exception.
		print('+ \t '+str(len(arr)) + ' added')
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)
		logErr.critical(arr)
		logErr.critical(ts)

def store_mentions_news_extended_bulk(client, arr, ts):
	# each obj in arr : {title, crypto, source, url}
	
	#	 db.mentionsExtendedNews.createIndex( { crypto: 1, url: 1 , title: 1}, { unique: true } )
	try:
		for a in arr:
			a['timestamp'] = ts
	
		db = selectDB(client)
		db.mentionsExtendedNews.insert_many(arr, ordered=False) # ordered: If false: when a single write fails, the operation will continue with the remaining writes, if any, and throw an exception.
		print('+ \t '+str(len(arr)) + ' added')
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_mentions_social(client, count, ts, crypto, source):
	try:
		db = selectDB(client)
		db.mentionsSocial.insert_one(
			{
				"crypto": crypto, 
				"timestamp": ts, 
				"mentions": count,
				"source": source,
			}
		)
		# print('+')
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def store_mentions_news(client, count, ts, crypto, source):
	try:
		db = selectDB(client)
		db.mentionsNews.insert_one(
			{
				"crypto": crypto, 
				"timestamp": ts, 
				"mentions": count,
				"source": source,
			}
		)
		# print('+')
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def check_when_newsSite_lastBuilt(client, url):
	try:
		db = selectDB(client)
		cursor = db.get_collection('newsbuilds').find({'url':{'$eq':url}})
		result = list(cursor)
		return result
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def insert_newsSite_lastBuilt(client, url):
	try:
		db = selectDB(client)
		db.newsbuilds.insert_one({'url':url,'ts':dtNow()})
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def update_newsSite_lastBuilt(client, id):
	try:
		db = selectDB(client)
		db.newsbuilds.update({'_id':ObjectId(id)}, {'$set':{'ts':dtNow()}})
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def store_currency(client, crypto, USD, ts):
	# do not set index for 'tx' !!! otherwise conflict with different cryptos
	try:
		db = selectDB(client)
		db.currencies.insert_one(
			{
				"crypto": crypto,
				"USD": USD,
				"timestamp":ts
			}
		)
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def upsert_exchangeCurrency(client, base_cur, quote_cur, data, ts, exchange):

	#  db.exchanges.createIndex( { base_cur: 1, quote_cur: 1, timestamp: 1, exchange: 1 }, { unique: true } )
	try:
		db = selectDB(client)
		
		dct_qry = {
			"base_cur": base_cur,
			"quote_cur": quote_cur,
			"timestamp":ts,
			"exchange":exchange,
		}
		
		dct = dct_qry.copy()
		dct['data']=data

		out = db.exchanges.update(dct_qry, dct, upsert=True)

		log = createLogger("exchangeProducer_info", "exchangeProducer_info")
		log.info(str(out))
	except Exception as ex:
		print(ex)
		if not "E11000" in str(ex):
			print("exception: "  + str(ex))
			logErr = createLogger("DAL", "DAL_error")
			logErr.critical(str(ex), exc_info=True)

def __fix_exchangeCurrency():
	client = openConnection()
	db = selectDB(client)
	cursor = db.exchanges.find()
	result = list(cursor)
	for r in result:
		#print(r)

		dct = {
			"base_cur": 'BTC',
			'quote_cur': 'USDT',
			"timestamp":r['timestamp'],
			"exchange":r['exchange'],
			"data": r['data'],
		}


		import collections
		dct = collections.OrderedDict(sorted(dct.items()))
		uid = int(hashlib.md5(( ''.join((str(x) for key, x in dct.items())) ).encode()).hexdigest()[:8], 16)
		dct['uid']=uid

		output = db.exchanges.update({'_id':ObjectId(r['_id'])}, dct)
		print(output)

		

def store_volume(client, fromSymbol, fromVol24_avg, fromVol24_sum, toSymbol, toVol24_avg, toVol24_sum,  ts):
	try:
		db = selectDB(client)
		db.volumes.insert_one(
			{
				"fromSymbol": fromSymbol,
				"fromVol24_avg": fromVol24_avg,
				"fromVol24_sum": fromVol24_sum,

				"toSymbol": toSymbol,
				"toVol24_avg": toVol24_avg,
				"toVol24_sum": toVol24_sum,
				
				"timestamp":ts,
			}
		)
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_sentiments_social(client, sentiments, ts, crypto):
	# 
	try:
		db = selectDB(client)
		db.sentimentsSocial.insert_one(
			{
				"crypto": crypto, 
				"timestamp": ts, 
				"sentiments": sentiments
			}
		)
		# print('+')
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def store_sentiments_news(client, sentiments, ts, crypto):
	# 
	try:
		db = selectDB(client)
		db.sentimentsNews.insert_one(
			{
				"crypto": crypto, 
				"timestamp": ts, 
				"sentiments": sentiments
			}
		)
		# print('+')
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def liveness_IAmAlive(client, name):
	try:
		db = selectDB(client)
		db.liveness.update({'name': name}, {'name': name, 'timestamp': dtNow()}, upsert=True)
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def liveness_getAll(client):
	try:
		db = selectDB(client)
		cursor = db.liveness.find()
		result = list(cursor)
		return result
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_prediction2(client, crypto, interval, timestamp_predic, timestamp, feature, featuresID, n_batch_size, n_neurons, n_window, n_epoch, data):
	# db.predictions.createIndex( { uid: 1 }, { unique: true } )
	try:
		import collections
		db = selectDB(client)
		dct = { # use dct to construct uid first, then add other data for update
			'crypto':crypto, 
			'interval':interval, 
			'timestamp_predic':timestamp_predic, 
			'timestamp':timestamp, 
			'feature':feature, 
			'featuresID': featuresID, 
			'n_batch_size': n_batch_size,
			'n_neurons': n_neurons,
			'n_window': n_window,
			'n_epoch': n_epoch,
		}
		dct = collections.OrderedDict(sorted(dct.items()))
		# adding new key-values to the dct will yield duplicates because uid will be different

		uid = int(hashlib.md5(( ''.join((str(x) for key, x in dct.items())) ).encode()).hexdigest()[:8], 16)
		dct['uid'] = uid
		dct['data'] = data

		db.predictions.remove({'uid': uid})
		db.predictions.update({'uid': uid}, dct, upsert=True)
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_predictions_completed(client, version, timestamp_predic):
	try:
		db = selectDB(client)
		db.predictions_completed.update({'version': version, 'timestamp_predic': timestamp_predic}, {'version': version, 'timestamp_predic': timestamp_predic}, upsert=True)
	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)

def init_predictions_completed(client):
	# temporary function to fill this new collection based on already generated data
	try:
		db = selectDB(client)
		cursor = db.predictions.find()
		#result = list(cursor)
		for e in cursor:
			
			if 'feature' in e:
				v = None
				if e['feature'] == 'price':
					v = 1
				elif e['feature'] == 'price2':
					v = 2
				elif e['feature'] == 'price3':
					v = 3
				if v != None:
					print( db.predictions_completed.update({'version': v, 'timestamp_predic': e['timestamp_predic']}, {'version': v, 'timestamp_predic': e['timestamp_predic']}, upsert=True) )

	except Exception as ex:
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_prediction3(client, sendobj):
	# db.predictions3.createIndex( { uid: 1 }, { unique: true } )
	try:
		import collections
		db = selectDB(client)
		dct = { # use dct to construct uid first, then add other data for update
			'crypto': 				sendobj['crypto'], 
			'interval': 			sendobj['interval'], 
			'timestamp':			sendobj['timestamp'], 
			'feature':				sendobj['feature'], 
			'featuresID': 			sendobj['featuresID'], 
			'n_batch_size': 		sendobj['n_batch_size'],
			'n_neurons': 			sendobj['n_neuron'],
			'n_window': 			sendobj['n_window'],
			'n_epoch': 				sendobj['n_epoch'],
			'predict_n_intervals':	sendobj['predict_n_intervals'],
			'n_hiddenlayers':		sendobj['n_hiddenlay'],
		}
		dct = collections.OrderedDict(sorted(dct.items()))
		# adding new key-values to the dct will yield duplicates because uid will be different

		uid = int(hashlib.md5(( ''.join((str(x) for key, x in dct.items())) ).encode()).hexdigest()[:8], 16)
		dct['uid'] = uid
		dct['data'] = sendobj['data']
		# beware that upsert will update even deep nested objects. --> solution: remove first

		db.predictions3.remove({'uid': uid})
		db.predictions3.update({'uid': uid}, dct, upsert=True)
	except Exception as ex:
		print(ex)
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_prediction4(client, sendobj):
	# db.predictions3.createIndex( { uid: 1 }, { unique: true } )
	try:
		import collections
		db = selectDB(client)
		dct = { # use dct to construct uid first, then add other data for update
			'symbol': 				sendobj['symbol'], 
			'interval': 			sendobj['interval'], 
			'timestamp':			sendobj['timestamp'], 
			'feature':				sendobj['feature'], 
			'featuresID': 			sendobj['featuresID'], 
			'n_batch_size': 		sendobj['n_batch_size'],
			'n_neurons': 			sendobj['n_neuron'],
			'n_window': 			sendobj['n_window'],
			'n_epoch': 				sendobj['n_epoch'],
			'predict_n_intervals':	sendobj['predict_n_intervals'],
			'n_hiddenlayers':		sendobj['n_hiddenlay'],
		}
		dct = collections.OrderedDict(sorted(dct.items()))
		# adding new key-values to the dct will yield duplicates because uid will be different

		uid = int(hashlib.md5(( ''.join((str(x) for key, x in dct.items())) ).encode()).hexdigest()[:8], 16)
		dct['uid'] = uid
		dct['data'] = sendobj['data']
		# beware that upsert will update even deep nested objects. --> solution: remove first

		db.predictions4.remove({'uid': uid})
		db.predictions4.update({'uid': uid}, dct, upsert=True)
	except Exception as ex:
		print(ex)
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


def store_predictions_v1(client, sendobj):
	# db.predictions_v1.createIndex( { uid: 1 }, { unique: true } )
	try:
		import collections
		db = selectDB(client)
		dct = { # use dct to construct uid first, then add other data for update
			'base_cur': 			sendobj['base_cur'], 
			'quote_cur': 			sendobj['quote_cur'], 
			'interval': 			sendobj['interval'], 
			'timestamp':			sendobj['timestamp'], 
			'exchange':				sendobj['exchange'], 

			'n_fid': 				sendobj['n_fid'], 
			'n_batch_size': 		sendobj['n_batch_size'],
			'n_neurons': 			sendobj['n_neuron'],
			'n_window': 			sendobj['n_window'],
			'n_epoch': 				sendobj['n_epoch'],
			'n_predict_intervals':	sendobj['n_predict_intervals'],
			'n_hiddenlayers':		sendobj['n_hiddenlay'],

			'mode':					sendobj['mode'],
		}
		dct = collections.OrderedDict(sorted(dct.items()))

		# adding new key-values to the dct will yield duplicates because uid will be different
		stringUID = '_'.join((str(x) for key, x in dct.items()))
		uid = int(hashlib.md5(( stringUID ).encode()).hexdigest()[:8], 16)
		dct['stringUID'] = stringUID
		dct['uid'] = uid
		dct['data'] = sendobj['data']
		# beware that upsert will update even deep nested objects. --> solution: remove first

		db.predictions_v1.remove({'uid': uid})
		db.predictions_v1.update({'uid': uid}, dct, upsert=True)
	except Exception as ex:
		print("error DAL: " + str(ex))
		logErr = createLogger("DAL", "DAL_error")
		logErr.critical(str(ex), exc_info=True)


