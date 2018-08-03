
# email: cryptopredicted@gmail.com
# user: crypto_predicted
# pass: fqe5r89f49esrqg8-*ser5g+serg
# url: https://www.reddit.com/prefs/apps
# client id: EzcegP77YYq7dg
# client secret:	CwTogkSNVPGIJFiQdWyZF_Gqqr4

import praw
import json
import nltk
import sys
import os
import time
sys.path.insert(0, '/home/cryptopredicted/')
import producerMgr
from mysettings import CRYPTO_redditProducer_subreddits, CRYPTO_socialKeywords, dtNow, createLogger
import DAL

logErr = createLogger("redditProducer_error", "redditProducer_error")
log = createLogger("redditProducer_info", "redditProducer_info")


def streamAll():
	producer = producerMgr.create_kafkaProducer()
	subreddits = list(CRYPTO_redditProducer_subreddits.values()) # get values
	subreddits = [item for items in subreddits for item in items] # flatten
	querystring="+".join(subreddits)
	log.info(querystring)
	
	CryptoMapping = list(CRYPTO_socialKeywords.items())
	while True:
		try:
			client = DAL.openConnection()
			alive_counter = dtNow()
			reddit = praw.Reddit(client_id='EzcegP77YYq7dg',client_secret="CwTogkSNVPGIJFiQdWyZF_Gqqr4",user_agent='USERAGENT')
			for comment in reddit.subreddit(querystring).stream.comments():
				if comment.body.find('Your submission has been flagged') == -1:
					body = comment.link_title + " | " + comment.body # let's construct a new 'body' since comments don't always tell which crypto is discussed
					sbody = nltk.wordpunct_tokenize(body.lower())
					for crypto, kws in CryptoMapping:
						for kw in kws:
							if kw in sbody:
								log.info("sending to kafka: " + comment.link_url)
								producerMgr.producer_send_mentionsSocial(comment.body, 'reddit', comment.link_url, crypto, producer )
								if (dtNow()-alive_counter).total_seconds() >= 15:
									DAL.liveness_IAmAlive(client, "producer: reddit")
									alive_counter = dtNow()
								break # one signal per crypto only
		except Exception as ex:
			logErr.critical(str(ex), exc_info=True)
		time.sleep(20)

streamAll()
