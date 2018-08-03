import os
import multiprocessing as mp
from datetime import datetime, timedelta
import nltk
from facepy import GraphAPI
import pprint
import math
import time
import sys
sys.path.insert(0, '/home/cryptopredicted/')
from mysettings import CRYPTO_facebookPages, CRYPTO_socialKeywords, dtNow, createLogger
import producerMgr
producer = producerMgr.create_kafkaProducer()
import DAL

logErr = createLogger("facebookProducer_error", "facebookProducer_error")
log = createLogger("facebookProducer_info", "facebookProducer_info")

# Facebook Graph API only allows about 600 API calls per 600 seconds (1 call per sec)
# It is also limited to 50 (but this is handled by facepy)
# Every batch's entry counts as one call
# so basically we can make scrape 600 pages and then sleep for 10min
# if we have more than 600 pages then we have to sleep(10*60) between every 600
# however in reality we are not going to have more than 600 pages any time soon since we only analyze big/mainstream pages

# Minimum seconds to wait between each batch wait=len(batch)
# To be on the safe side: wait = ceil(wait*1.30), and wait = 60 if wait < 60  (if we only have one page then we don't want to poll every 3sec, but every minute)


post_arr = []
graph = GraphAPI("637282779976098|Njeav9jewlL9uH-xTWFeodHNAak")
appendix = '/feed/?fields=message,link,created_time,name' # we don't need comments/likes/reactions, because these change over time -- we only care when something is posted
appendix += '&limit=25'
for page in CRYPTO_facebookPages:
	post_arr.append({"method": "GET", "relative_url": page+appendix})

def process():
	X_sleep = len(CRYPTO_facebookPages) * 1.40
	X_sleep = 60 if X_sleep < 60 else X_sleep
	last_check = dtNow() - timedelta(seconds=X_sleep) # give it some slack in case something was posted just recently
	CryptoMapping = list(CRYPTO_socialKeywords.items())
	while True:
		try:
			log.info("\tlast check: " + str(last_check))
			ret = graph.batch(post_arr)
			for entries in ret:
				try:
					log.info(entries)
					for obj in entries['data']:
						body = ''
						link = obj['link'] if 'link' in obj else ''
						created_time = datetime.strptime(obj['created_time'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None) # UTC : OK
						#log.info(created_time)
						if not created_time >= last_check:
							continue # skip non-realtime mentions

						if 'message' in obj:
							body += obj['message']
						if 'name' in obj:
							body += "\n" + obj['name']

						log.info("created: " + obj['created_time'])
						log.info("relative: " + str(created_time))
						log.info("")
						sbody = nltk.wordpunct_tokenize(body.lower())
						for crypto, kws in CryptoMapping:
							for kw in kws:
								if kw in sbody:
									log.info("sending to kafka: " + link)
									producerMgr.producer_send_mentionsSocial(body, 'facebook', link, crypto, producer)
						#pprint.plog.info(o)
						#log.info("")
				except Exception as ex:
					logErr.critical(str(ex), exc_info=True)
			client = DAL.openConnection()
			DAL.liveness_IAmAlive(client, "producer: facebook")
		except Exception as ex:
			logErr.critical(str(ex), exc_info=True)
		
		log.info("\tlast check: " + str(last_check))
		log.info("X_sleep: " + str(X_sleep))
		last_check = dtNow() # new last_check
		time.sleep(X_sleep)

process()