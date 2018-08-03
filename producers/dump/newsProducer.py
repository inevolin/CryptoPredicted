import pprint
import newspaper
from newspaper import Article, ArticleException
from newspaper import news_pool
from urllib.parse import urlparse
import time
import traceback

import sys
import os
sys.path.insert(0, '/home/cryptopredicted/')
import DAL
import producerMgr
from mysettings import INTERVAL_SEC_NEWS, CRYPTO_newsProducer, SITES_newsProducer, dtNow, createLogger
import multiprocessing
import multiprocessing.pool
from multiprocessing.dummy import Pool as ThreadPool
import nltk

# cache stored here: /root/.newspaper_scraper/memoized
# warning: adding a new {crypto} will not have an effect on new articles added since then
#			reason: already seen articles are cached and prevented from scraping

logErr = createLogger("newsProducer_error", "newsProducer_error")
log = createLogger("newsProducer_info", "newsProducer_info")


N_SITES_PARALLEL = 3
N_ARTICLES_PARALLEL = 5

DUP_TITLES = []

def divideWork(ofunc, arr, max_parallel):
	# helper function which splits 'arr' in 'max_parallel' pieces => 'batcharr'€i and then calls ofunc(batcharr) for each piece(i)
	batcharr = []
	for i in range(len(arr)):
		batcharr.append(arr[i])
		if len(batcharr)==max_parallel or i+1==len(arr):
			#log.info(str(batcharr))
			ofunc(batcharr)
			batcharr = []



import threading
class articleProcessor (threading.Thread):
	def __init__(self, article, producer):
		threading.Thread.__init__(self)
		self.article = article
		self.producer = producer

	def getDomainFromString(self, url):
		return urlparse(url).hostname

	def persistMatch(self, body, title, url, crypto, producer):
		source = self.getDomainFromString(url)
		log.info("				 found at source: " + source)
		producerMgr.producer_send_mentionsNews(body, title, source, url, crypto, producer)

	def contains(self, haystack, needles):
		hay = haystack.lower()
		hay = nltk.wordpunct_tokenize(hay)
		for needle in needles:
			if needle in hay:
				return True
		return False

	def processArticle(self, article):
		log.info("				"+"processArticle ...")
		try:
			article.download()
			article.parse()
			if article.title in DUP_TITLES: 
				#log.info("Prevented duplicate title!")
				pass # preventing duplicate entries who have same headline but different url (due to url params etc...)
			else:
				DUP_TITLES.append(article.title)
				for crypto, terms in CRYPTO_newsProducer.items():
					if self.contains(article.title, terms) or self.contains(article.text, terms):
						self.persistMatch(article.text, article.title, article.url, crypto, self.producer)
		except Exception as ex:
			logErr.critical(str(ex), exc_info=True)

	def run(self):
		self.processArticle(self.article)

def processArticles(articles):
	try:
		producer = producerMgr.create_kafkaProducer()
		log.info("			 processArticles start")

		#threadLock = threading.Lock() # https://www.tutorialspoint.com/python3/python_multithreading.htm
		threads = []

		for a in articles:
			th = articleProcessor(a, producer)
			th.start()
			threads.append(th)

		for t in threads:
			try:
   				t.join(timeout=30) # 30 sec per article
			except Exception as ex:
				logErr.critical(str(ex), exc_info=True)   			

	except Exception as ex:
		logErr.critical(str(ex), exc_info=True)
	log.info("			 processArticles end")

def mayProcessArticles(site):
	# make sure the site was built less than an hour ago
	# if not, we should build it first, so second iteration will be considered as real-time data
	# if we don't do this then we may produce data that is old and was not published in current window-time
	client = DAL.openConnection()
	lastb = DAL.check_when_newsSite_lastBuilt(client, site)
	if len(lastb) == 0:
		return [False,0] # new site, has not been built yet
	now = dtNow()
	lastcheck = lastb[0]['ts']
	ds = (now - lastcheck).total_seconds()
	log.info("		 last build: " + str(ds) + " sec ago.")
	if ds > 60*60:
		return [False,lastb[0]['_id']] # more than an hour passed since last check, build now and produce in next iteration
	else:
		return [True,lastb[0]['_id']]

def markSiteAsBuilt(site, mayVal):
	client = DAL.openConnection()
	if mayVal[1] == 0:
		DAL.insert_newsSite_lastBuilt(client, site)
		log.info("		 db:insert")
	else:
		DAL.update_newsSite_lastBuilt(client, mayVal[1])
		log.info("		 db:update")

def processSite(site):
	DUP_TITLES = [] # clean slate every site
	log.info("		 processSite start")
	log.info("		  " +site)
	mayVal = mayProcessArticles(site)
	b = newspaper.build(site, memoize_articles=True) # False to disable cache ; True in production
	markSiteAsBuilt(site, mayVal)
	if mayVal[0]:
		divideWork(processArticles, b.articles, N_ARTICLES_PARALLEL) # how many articles to process in parallel
	else:
		log.info("		 skipping processArticles")
	log.info("		 processSite end")
	client = DAL.openConnection()
	DAL.liveness_IAmAlive(client, "producer: news")

def processSites(sitesarr):
	with multiprocessing.Pool(len(sitesarr)) as pool:
		try:
			log.info("	 processSites start")
			arr = []
			for a in sitesarr:
				arr.append( pool.apply_async(processSite, (a,)) )
			# pool.join() 
			for a in arr:
				try:
					a.get(timeout=600) # give it 10 minutes per site -- otherwise abort/timeout
				except Exception as ex:
					logErr.critical(str(ex), exc_info=True)
		except Exception as ex:
			logErr.critical(str(ex), exc_info=True)
		log.info("	 processSites end")

def processAll():
	log.info(" processAll start")

	divideWork(processSites, SITES_newsProducer, N_SITES_PARALLEL) # how many news sites to process in parallel

	log.info(" processAll end")
	log.info("")

def streamAll():
	while True:
		try:
			processAll()
			log.info("ZZZZzzzz....")
			time.sleep(INTERVAL_SEC_NEWS)
		except KeyboardInterrupt:
			raise
		except Exception as ex:
			logErr.critical(str(ex), exc_info=True)
		#except Exception as ex:
		#	traceback.print_tb(ex.__traceback__)


# find new articles from pre-defined news sites
# parse+nlp each article --> keywords
# check if {crypto} is included in keywords, if not check its text
# store frequency in DB


def testing():
	b = newspaper.build(sys.argv[2], memoize_articles=False)
	for article in b.articles:
		article.download()
		article.parse()
		log.info(article.url)
		log.info(article.title)
		log.info("")


if len(sys.argv) >= 2 and sys.argv[1]=="test":
	log.info("testing mode...")
	testing()
else:
	streamAll() # production mode



