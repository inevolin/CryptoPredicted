
# Settings/configurations and common functions used by various Python scripts.
# *) Kafka endpoint URI, authentication and topics
# *) Keywords used by twitter producer, reddit; facebook pages; and news urls.

import sys
import os
import traceback
import datetime
import json
import time
from bson import json_util
import pytz
import logging
import logging.handlers
    
def dtNow():
	return datetime.datetime.now().replace(microsecond=0)

def createLogger(name, filename, maxBytes=13107200, backupCount=3):
    log = logging.getLogger(name+"_my")
    if len(log.handlers) == 0:
        handler = logging.handlers.RotatingFileHandler("/home/cryptopredicted/logs/"+filename+".log", maxBytes=maxBytes, backupCount=backupCount)
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
    return log

INTERVAL_SEC_CURRENCY = 20 # currency update interval
INTERVAL_SEC_NEWS = 1200 # delay of X seconds between re-checks : 20 minutes (news sites are not updated every single minute)
INTERVAL_SEC_FORUMS = 20

kafkaServerEndPoint = "95.216.22.99:9092" # kafka server
kafkaTopic_mentionsSocial = 'mentionsSocial'
kafkaTopic_mentionsNews = 'mentionsNews'
kafkaAuth = {'sasl_mechanism':'SASL_PLAINTEXT', 'sasl_plain_username':'jFEZf9z5f4ze', 'sasl_plain_password':'__feqzfqze---qefF__'}

CRYPTO_socialKeywords = {
	# used to detect crypto-related mentions: used by twitter, reddit, NLP
	# all lower case 

    'BTC':['bitcoin', 'btc', '#btc', '$btc', '#bitcoin', ], 
    'ETH':['ethereum', 'eth', '#eth', '$eth', '#ethereum', ],

    'LTC':['litecoin', 'ltc', '#ltc', '$ltc', '#litecoin', ],
    'DASH':['digitalcash', '#dash', '$dash', 'dash', '#digitalcash', ],
    'XMR':['monero', '#xmr', '$xmr', 'xmr', '#monero', ],
    'NXT':['#nxt', '$nxt', 'nxt', ],
    'ZEC':['zcash', 'zec', '#zec', '$zec', '#zcash', ],
    'DGB':['digibyte', 'dgb', '#dgb', '$dgb', '#digibyte', ],
    'XRP':['ripple', 'xrp', '#xrp', '$xrp', '#ripple', ],
    'EOS':['#eos', '$eos', 'eos', ],

    'BCH':['bitcoin cash', 'bitcoincash', '#bitcoincash', '$bitcoincash', 'bch', '#bch', '$bch', ],
    'ETC':['ethereum classic', 'ethereumclassic', '#ethereumclassic', '$ethereumclassic', 'etc', '$etc', '#etc',],
    'IOT':['iota', '#iota', '$iota',],
    'XLM':['stellar', '#stellar', '$stellar', 'xlm', '$xlm', '#xlm', ],
    'NEO':['neo', '#neo', '$neo', ],
    'DOGE':['doge', '#doge', '$doge', ],
    'TRX':['tronix', '#tronix', '$tronix', 'trx', '$trx', '#trx', 'tron', '#tron', '$tron' ],
    'ADA':['cardano', '$cardano', '#cardano', 'ada', '#ada', '$ada', ],
    'OMG':['omisego', '$omisego', '#omisego', 'omg', '$omg', '#omg', ],
    #'SC':['siacoin', '$siacoin', '#siacoin', 'sc', '$sc', '#sc', ],
    # ...
}

CRYPTO_twitterProducer = {
	## in twitter "#btc" and "$btc" are included in "btc"
	## however "dash" could give results unrelated to crypto

    'BTC':['bitcoin', 'btc',], 
    'ETH':['ethereum', 'eth',],

    'LTC':['litecoin', 'ltc', ],
    'DASH':['digitalcash', '#dash', '$dash',],
    'XMR':['monero', '#xmr', '$xmr',],
    'NXT':['#nxt', '$nxt',],
    'ZEC':['zcash', 'zec',],
    'DGB':['digibyte', 'dgb',],
    'XRP':['ripple', 'xrp',],
    'EOS':['#eos', '$eos',],

    'BCH':['bitcoincash', 'bch', ],
    'ETC':['ethereumclassic', '$etc', ],
    'IOT':['iota', ],
    'XLM':['#stellar', 'xlm', ],
    'NEO':['#neo', '$neo', ],
    'DOGE':['#doge', '$doge', ],
    'TRX':['tronix', 'trx', ],
    'ADA':['cardano', '$ada', ],
    'OMG':['omisego', '$omg', ],
    #'SC':['siacoin', '$sc', ],

    # ...
}

CRYPTO_newsProducer = { 
	# we use these terms to look in title/body of an article to determine if it's about a specific crypto

	'BTC' : ['bitcoin', 'btc',], 
	'ETH' : ['ethereum', 'eth',],

    'LTC':['litecoin', 'ltc', ],
    'DASH':['digitalcash', '#dash', '$dash',],
    'XMR':['monero', 'xmr', '#xmr', '$xmr',],
    'NXT':['nxt', '#nxt', '$nxt',],
    'ZEC':['zcash', 'zec',],
    'DGB':['digibyte', 'dgb',],
    'XRP':['ripple', 'xrp',],
    'EOS':['eos', '#eos', '$eos',],


    'BCH':['bitcoincash', 'bch', '#bch', '$bch' ],
    'ETC':['ethereumclassic', '$etc', '#etc' ],
    'IOT':['iota', '#iota', '$iota', ],
    'XLM':['#stellar', 'xlm', '$stellar', '$xlm', '#xlm', ],
    'NEO':['#neo', '$neo', ],
    'DOGE':['#doge', '$doge', 'doge', ],
    'TRX':['tronix', 'trx', '#trx', '$trx', 'tron', '#tron', '$tron', ],
    'ADA':['cardano', '$ada', '#ada', ],
    'OMG':['omisego', '$omg', '#ada', ],
    #'SC':['siacoin', '$sc', '#sc', ],
}


# listen for comments on subreddits; subreddit names are separated by + sign
CRYPTO_redditProducer_subreddits = { 
	'general': ['CoinBase','CryptoMarkets',],

	'BTC': ['Bitcoin','bitcoin_uncensored','btc','Bitcoin_News','BitcoinMarkets','bitcoin_cash','BitcoinBeginners',],
	'ETH': ['ethereum','ethereumnoobies','ethtrader','EthAnalysis','ethtraderpro','ETHInsider',],

    'LTC':['litecoin', 'ltc', ],
    'DASH':['dashpay',],
    'XMR':['Monero', 'xmrtrader',],
    'NXT':['NXT', ],
    'ZEC':['zec', ],
    'DGB':['Digibyte', ],
    'XRP':['Ripple', 'XRP',],
    'EOS':['eos', 'EOSDev',],

    'BCH':['Bitcoincash', 'bitcoin_cash', 'BitcoinCashLol' ],
    'ETC':['EthereumClassic', 'EtcTrader', ],
    'IOT':['Iota', 'IOTAmarkets', ],
    'XLM':['Stellar', ],
    'NEO':['NEO', 'Neotrader', ],
    'DOGE':['dogecoin', 'dogemarket', ],
    'TRX':['Tronix', 'TronixTrader', ],
    'ADA':['cardano', 'CardanoCoin', ],
    'OMG':['OMG', 'OMGtrader', 'OMGtraders', ],
    #'SC':['siacoin', 'siatrader', ],
}

CRYPTO_currencyProducer = {
    'BTCUSD':['BTC', 'USD'],
    'ETHUSD':['ETH', 'USD'],

    'LTCUSD':['LTC', 'USD'],
    'DASHUSD':['DASH', 'USD'],
    'XMRUSD':['XMR', 'USD'],
    'NXTUSD':['NXT', 'USD'],
    'ZECUSD':['ZEC', 'USD'],
    'DGBUSD':['DGB', 'USD'],
    'XRPUSD':['XRP', 'USD'],
    'EOSUSD':['EOS', 'USD'],

    'BCH':['BCH', 'USD'],
    'ETC':['ETC', 'USD'],
    'IOT':['IOT', 'USD'],
    'XLM':['XLM', 'USD'],
    'NEO':['NEO', 'USD'],
    'DOGE':['DOGE', 'USD'],
    'TRX':['TRX', 'USD'],
    'ADA':['ADA', 'USD'],
    'OMG':['OMG', 'USD'],
    #'SC':['SC', 'USD'],
    # ...
}

CRYPTO_facebookPages = [
	# pages (by name):
	'cnbccrypto',
	'CryptoEverything',
	'Cryptolyse',
	'CryptoTradersNews',
	'cryptotradingsignal',
	'all.things.cryptocurrency.daily',
	'bitcoinandcrypto',
	'cryptohubcentral',
	'cryptomkt',
	'HotCrypto',
	'LHCrypto',
	'MasterTheCryptoWorld',
	'cryptopricetoday',
	'inflowcrypto',
	'badcrypto',
	'Bitcoin.News.Cryptocurrency.Trade',
	'cryptostache',

	# public groups (by id):
	'1922566931292037', # /groups/bkcryptotrader/
	'256406324441664', # /groups/TheBitcoin/
	'300065276761228', # /groups/bitcoinlitecoin/
	'144961585575245', # /groups/bitcoinitalia/
	'637562649639902', # /groups/bitcoinvalencia/
	'246479302178538',
	'504768593237915', # cryptomasteryvip
	'1728595424029593', # learncrypto
	'140037853273290', # CryptoCousins
	'1316333775145056',
	'664873586880402', # cryptoinvestingclub
	'885160248326266', # CryptoWatchDogGroup
	'124844464777346', # blockchainnation
	'1709457722715586',
	'381376835597450', # cryptoaus
	'127641828007836', # blackcryptoinvesting
]

SITES_forumProducer = [
	'https://www.blackhatworld.com',
	'https://www.blackhatworld.com/forums/cryptocurrency.218/',
]

SITES_newsProducer = [
	'http://www.telegraph.co.uk/news/',
	'https://www.coindesk.com/',
	'https://economictimes.indiatimes.com/news/economy',
	'https://www.rt.com/business/',
	'https://news.bitcoin.com/',
	'https://www.express.co.uk/',
	'https://cointelegraph.com/',
	'https://www.ccn.com/',
	'http://www.independent.co.uk/',
	'https://www.bloomberg.com/',
	'https://www.cnbc.com/finance/',
	'http://www.aljazeera.com/topics/categories/business.html',
	'https://finance.yahoo.com/news/',
	'http://www.itpro.co.uk/strategy/news',
	'https://www.theguardian.com/uk/technology',
	'http://money.cnn.com/',
	'http://www.foxnews.com/',
	'http://www.bbc.com/news/business',
	'http://www.businessinsider.com/clusterstock',
	'https://www.ft.com/markets',
	'https://seekingalpha.com/',
	'https://news.crunchbase.com/news/',
	'https://www.theverge.com/',
	'http://fortune.com/',
	'https://www.investors.com/news/',
	'http://www.newsbtc.com/',
	'http://time.com/money/',
	'https://www.fool.com/',
	'http://www.valuewalk.com/',
	'https://theusacommerce.com/',
	'http://www.digitaljournal.com/business',
	'https://www.reuters.com/',
	'http://bitcoinist.com/',
	'http://normanobserver.com/',
	'https://bravenewcoin.com/news',
	
	# 'https://www.forbes.com/', # has annoying pre-loader with redirect :: not working
]
