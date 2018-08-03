import pprint
import newspaper
from newspaper import Article, ArticleException
from newspaper import news_pool
import nltk
from urllib.parse import urlparse
import time
import traceback
# nltk.download('punkt')
import re
import sys
import os
sys.path.insert(0, '/home/cryptopredicted/')
import DAL
import producerMgr
producer = producerMgr.create_kafkaProducer() # this is thread-safe
from mysettings import INTERVAL_SEC_FORUMS, CRYPTO_socialKeywords, SITES_forumProducer, logException, dtNow
from multiprocessing.dummy import Pool as ThreadPool 

# cache stored here: /root/.newspaper_scraper/memoized
# warning: adding a new {crypto} will not have an effect on new articles added since then
#			reason: already seen articles are cached and prevented from scraping

N_SITES_PARALLEL = 3
N_ARTICLES_PARALLEL = 3

DUP_TITLES = []
client = DAL.openConnection()

def divideWork(ofunc, arr, max_parallel):
	# helper function which splits 'arr' in 'max_parallel' pieces => 'batcharr'€i and then calls ofunc(batcharr) for each piece(i)
	batcharr = []
	for i in range(len(arr)):
		batcharr.append(arr[i])
		if len(batcharr)==max_parallel or i+1==len(arr):
			#print(str(batcharr))
			ofunc(batcharr)
			batcharr = []

def getDomainFromString(url): return urlparse(url).hostname

def persistMatch(body, title, url, crypto):
	source = getDomainFromString(url)
	print(str(dtNow()) + "				" + " found at source: " + source)
	print(url)
	print(title)
	print(body)
	print()
	print()
	#producerMgr.producer_send_mentionsNews(body, title, source, url, crypto, producer)

def contains(haystack, needles):
	hay = haystack.lower()
	for needle in needles:
		if needle in hay: # potential false positives: 'apple' returns true for 'appletree' (simplified matching)
			return True
	return False

def processArticle(article):
	try:

		article.download()
		article.parse()

		if article.title in DUP_TITLES: 
			pass # preventing duplicate entries who have same headline but different url (due to url params etc...)
		else:
			DUP_TITLES.append(article.title)
			for crypto, terms in CRYPTO_socialKeywords.items():
				if contains(article.title, terms) or contains(article.text, terms):
					persistMatch(article.text, article.title, article.url, crypto)
	except:
		print(str(dtNow())+"				"+"error processingArticle")

def processArticles(articles):
	print(str(dtNow()) + "			" + " processArticles start")
	pool = ThreadPool(len(articles)) # pool of X threads to process articles in parallel
	pool.map(processArticle, articles)
	pool.close()
	pool.join()
	print(str(dtNow()) + "			" + " processArticles end")

def mayProcessArticles(site):
	# make sure the site was built less than an hour ago
	# if not, we should build it first, so second iteration will be considered as real-time data
	# if we don't do this then we may produce data that is old and was not published in current window-time
	lastb = DAL.check_when_newsSite_lastBuilt(client, site)
	if len(lastb) == 0:
		return [False,0] # new site, has not been built yet
	now = dtNow()
	lastcheck = lastb[0]['ts']
	ds = (now - lastcheck).total_seconds()
	print(str(dtNow()) + "		" + " last build: " + str(ds) + " sec ago.")
	if ds > 60*60:
		return [False,lastb[0]['_id']] # more than an hour passed since last check, build now and produce in next iteration
	else:
		return [True,lastb[0]['_id']]

def markSiteAsBuilt(site, mayVal):
	if mayVal[1] == 0:
		DAL.insert_newsSite_lastBuilt(client, site)
		print(str(dtNow()) + "		" + " db:insert")
	else:
		DAL.update_newsSite_lastBuilt(client, mayVal[1])
		print(str(dtNow()) + "		" + " db:update")

def processSite(site):
	DUP_TITLES = [] # clean slate every site
	print(str(dtNow()) + "		" + " processSite start")
	print(str(dtNow()) + "		  " +site)
	mayVal = mayProcessArticles(site)
	b = newspaper.build(site, memoize_articles=True) # False to disable cache ; True in production
	markSiteAsBuilt(site, mayVal)
	if mayVal[0]:
		divideWork(processArticles, b.articles, N_ARTICLES_PARALLEL) # how many articles to process in parallel
	else:
		print(str(dtNow()) + "		" + " skipping processArticles")
	print(str(dtNow()) + "		" + " processSite end")

def processSites(sitesarr):
	print(str(dtNow()) + "	" + " processSites start")
	pool = ThreadPool(len(sitesarr)) # pool of X threads to process sites in parallel
	pool.map(processSite, sitesarr)
	pool.close()
	pool.join()
	print(str(dtNow()) + "	" + " processSites end")

def processAll():
	print(str(dtNow()) + " processAll start")

	divideWork(processSites, SITES_forumProducer, N_SITES_PARALLEL) # how many news sites to process in parallel

	print(str(dtNow()) + " processAll end")
	print()

def streamAll():
	while True:
		try:
			processAll()
			print("ZZZZzzzz....")
			time.sleep(INTERVAL_SEC_FORUMS)
		except KeyboardInterrupt:
			raise
		except:
			logException(locals())
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
		print(article.url)
		print(article.title)
		print()


if len(sys.argv) >= 2 and sys.argv[1]=="test":
	print("testing mode...")
	testing()
else:
	#streamAll() # production mode
	pat = re.compile(r".*somi.*")
	print(True if re.match(pat, "this is quite some haystack") else False)



