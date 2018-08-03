import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import nltk
import sys
import os
sys.path.insert(0, '/home/cryptopredicted/')
import producerMgr
producer = producerMgr.create_kafkaProducer()
from mysettings import CRYPTO_socialKeywords, dtNow, CRYPTO_twitterProducer, createLogger
import DAL

logErr = createLogger("twitterProducer_error", "twitterProducer_error")
log = createLogger("twitterProducer_info", "twitterProducer_info")


class StdOutListener(StreamListener):
    def __init__(self):
        self.CryptoMapping = list(CRYPTO_socialKeywords.items())
        self.client = DAL.openConnection()
        self.alive_counter = dtNow()

    def on_data(self, data):
        try:
            data = json.loads(data)
            if 'user' in data:
                body, url = '', ''
                if 'user' in data and not 'retweeted_status' in data:
                    body = data['text']
                    url = 'https://twitter.com/' + data['user']['screen_name'] + '/status/' + data['id_str']
                else: # this is a re-tweet, so let us extract the original tweet
                    url = 'https://twitter.com/' + data['retweeted_status']['user']['screen_name'] + '/status/' + data['retweeted_status']['id_str']
                    body = (data['retweeted_status']['extended_tweet']['full_text'] if data['retweeted_status']['truncated'] else data['retweeted_status']['text'])
                
                sbody = nltk.wordpunct_tokenize(body.lower())
                for crypto, kws in self.CryptoMapping:
                    for kw in kws:
                        if kw in sbody:
                            log.info("sending to kafka: " + url)
                            producerMgr.producer_send_mentionsSocial(body, 'twitter', url, crypto, producer)
                            if (dtNow()-self.alive_counter).total_seconds() >= 15:
                                DAL.liveness_IAmAlive(self.client, "producer: twitter")
                                self.alive_counter = dtNow()
                            break # one signal per crypto only
            else:
                log.info(data)
        except Exception as ex:
            logErr.critical(str(ex), exc_info=True)
        return True
    def on_error(self, status):
        log.info("error at #34: "+str(status))

def streamAll():
    kws = list(CRYPTO_twitterProducer.values()) # get values
    kws = [item for items in kws for item in items] # flatten array
    log.info(str(kws))

    while True:
        try:
            access_token = "5855....7-tv........Pz4PZ8jJYRX"
            access_token_secret = "UiYiMDScAF9Nn.......X3kEpEzEyrBdJ"
            consumer_key = "qK7Qg43I........712M"
            consumer_secret = "GKqbr3Bs2y5EMqIT71.........jHlLio4B0hjOfVo"
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            stream.filter(track=kws)
        except Exception as ex:
            logErr.critical(str(ex), exc_info=True)
        time.sleep(30)# ! important so we don't get connection banned in case smthn goes wrong


def ____streamAll___():
    while True:
        try:
            url = 'daadada'
            body = 'laekfjoerjgiosrejgisoerjgsoijgroisejrgson  noerig g seiorgj serg serog serg seorig oseg,esorig ser'
            producerMgr.producer_send_mentionsSocial(body, 'twitter', url, crypto, producer)
            log.info("+")
        except Exception as ex:
            logErr.critical(str(ex), exc_info=True)
        time.sleep(.1)


streamAll()



