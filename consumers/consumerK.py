import sys
import os
sys.path.insert(0, '/home/cryptopredicted/')
from mysettings import CRYPTO_socialKeywords, createLogger, kafkaServerEndPoint, kafkaAuth, kafkaTopic_mentionsSocial, kafkaTopic_mentionsNews
import DAL
from WordStatDict import DICT

import traceback
import html
import nltk
from langdetect import detect
import json
import time
import threading
import json
from datetime import datetime
from kafka import KafkaConsumer, TopicPartition

max_window_seconds = 60 # aggregate & update in a one minute window
max_buck_len = 1000 # unless the bucket reaches a threshold then we should flush it prematurely
MAX_MENTIONS_EXTENDED_PER_WINDOW = 500000 # how many mentions to keep within a single buffer/bucket (max_window_seconds || max_buck_len)

try:
    _log = createLogger("consumerK_info", "consumerK_info")
    _logErr = createLogger("consumerK_error", "consumerK_error")
    client = DAL.openConnection()
except Exception as ex:
    log("exception")
    logErr(str(ex), traceback.format_exc())
    exit()

def log(*params):
    for p in params:
        print(p)
        _log.info(p)

def logErr(*params):
    for p in params:
        print(p)
        _logErr.critical(p)

def main():
    topics = (kafkaTopic_mentionsSocial, kafkaTopic_mentionsNews)
    consumer = KafkaConsumer(*topics, group_id='consumerK_GRP', bootstrap_servers=kafkaServerEndPoint, sasl_mechanism=kafkaAuth['sasl_mechanism'], sasl_plain_username=kafkaAuth['sasl_plain_username'], sasl_plain_password=kafkaAuth['sasl_plain_password'] )

    prev_ts = None
    bucket_social = []
    bucket_news = []
    threads = []
    for msg in consumer:
        # log("partition: " + str(msg.partition))
        try:
            ts = msg.timestamp/1000
            ts -= ts%(max_window_seconds) 

            val = json.loads(msg.value.decode('utf8'))

            if prev_ts != None:
                if (ts != prev_ts and len(bucket_social) > 0) or len(bucket_social) >= max_buck_len:
                    log("bucket_social: " + str(len(bucket_social)))
                    th = processor_social(prev_ts, bucket_social, threads)
                    threads.append(th)
                    th.start()
                    bucket_social = []

                if (ts != prev_ts and len(bucket_news) > 0) or len(bucket_news) >= max_buck_len:
                    log("bucket_news: " + str(len(bucket_news)))
                    th = processor_news(prev_ts, bucket_news, threads)
                    threads.append(th)
                    th.start()
                    bucket_news = []

            if val['type'] == 'social':
                bucket_social.append(val)
            elif val['type'] == 'news':
                bucket_news.append(val)

            prev_ts = ts
        except Exception as ex:
            log("exception")
            logErr(str(ex), traceback.format_exc())
        
# {
#     "url": "https://twit", 
#     "source": "twitter", 
#     "body": "body", 
#     "type": "social", 
#     "crypto": "BTC"
# }


class processor_social (threading.Thread):
    def __init__(self, timestamp, arr, threads):
        threading.Thread.__init__(self)
        self.timestamp = timestamp
        self.arr = arr
        self.threads = threads

    def run(self):
        try:
            print(str(datetime.fromtimestamp(self.timestamp)) + ": ("+str(len(self.threads))+") " + str(len(self.arr)))
            process_rdd_social(self.timestamp, self.arr)
            process_rdd_sentimentAnalysis_social(self.timestamp, self.arr)
        except Exception as ex:
            log("exception")
            logErr(str(ex), traceback.format_exc())
        self.threads.pop(0)
        
class processor_news (threading.Thread):
    def __init__(self, timestamp, arr, threads):
        threading.Thread.__init__(self)
        self.timestamp = timestamp
        self.arr = arr
        self.threads = threads

    def run(self):
        try:
            print(str(datetime.fromtimestamp(self.timestamp)) + ": ("+str(len(self.threads))+") " + str(len(self.arr)))
            process_rdd_news(self.timestamp, self.arr)
            process_rdd_sentimentAnalysis_news(self.timestamp, self.arr)
        except Exception as ex:
            log("exception")
            logErr(str(ex), traceback.format_exc())
        self.threads.pop(0)
        


def process_rdd_social(time, part_iterator):
    try:
        log("----------- %s :  SOCIAL --" % str(datetime.fromtimestamp(time)))
        buckets = {}
        for part in part_iterator:
            crypto = part['crypto']
            source = part['source']
            key = crypto+"|"+source
            if not key in buckets:
                buckets[key] = {'crypto':crypto, 'source': source, 'nums': 0}
            buckets[key]['nums'] += 1

        for key, b in buckets.items():
            crypto = b['crypto']
            source = b['source']
            nums = b['nums']
            log(crypto+" ("+source+"): "+str(nums))
            DAL.store_mentions_social(client, nums, datetime.fromtimestamp(time), crypto, source)
        
        DAL.liveness_IAmAlive(client, "worker: social")
    except Exception as ex:
        log("exception")
        logErr(str(ex), traceback.format_exc())

def process_rdd_news(time, part_iterator):
    try:
        log("----------- %s :  NEWS --" % str(datetime.fromtimestamp(time)))
        buckets = {}
        for part in part_iterator:
            crypto = part['crypto']
            source = part['source']
            key = crypto+"|"+source
            if not key in buckets:
                buckets[key] = {'crypto':crypto, 'source': source, 'nums': 0}
            buckets[key]['nums'] += 1

        for key, b in buckets.items():
            crypto = b['crypto']
            source = b['source']
            nums = b['nums']
            log(crypto+" ("+source+"): "+str(nums))
            DAL.store_mentions_news(client, nums, datetime.fromtimestamp(time), crypto, source)

        DAL.liveness_IAmAlive(client, "worker: news")
    except Exception as ex:
        log("exception")
        logErr(str(ex), traceback.format_exc())



def process_rdd_sentimentAnalysis_social(time, part_iterator):
    try:

        log("----------- %s :  Social Sentiment --" % str(datetime.fromtimestamp(time)))
    
        keepers = [] # elements from 'out' which we should keep and display to users (batch insert)
        crypto_sentiments = {}
        
        count = 0;
        for part in part_iterator:
            count+=1
            try:
                crypto = part["crypto"]
                body = part["body"]
                result = processAndValidateSocialMention(body, crypto)
                if not crypto in crypto_sentiments:
                    crypto_sentiments[crypto] = {}
                for cat in result['cats']:
                    if not cat in crypto_sentiments[crypto]:
                        crypto_sentiments[crypto][cat] = 0 
                    crypto_sentiments[crypto][cat] += result['cats'][cat]
                if result['keeper'] == 1:
                    part["body"] = result['mention'] # the text has changed due to NLP
                    part["social_score"] = result['score']
                    keepers.append(part)
            except Exception as ex:
                log("exception")
                logErr(str(ex), traceback.format_exc())
        if len(keepers) > 0:
            buckets = {}
            for keeper in keepers:
                if not keeper['crypto'] in buckets:
                    buckets[keeper['crypto']] = []
                buckets[keeper['crypto']].append( keeper )

            # for key, val in buckets.items():
            #     log(key + " keepers: " + str(len(val)))
            #     val = sorted(val, key=lambda k: k['social_score'], reverse=True)    
            #     val = val[:MAX_MENTIONS_EXTENDED_PER_WINDOW] if len(val) > MAX_MENTIONS_EXTENDED_PER_WINDOW else val
            #     log(key + " keepers: " + str(len(val)))
            #     log("--")
            #     DAL.store_mentions_social_extended_bulk(client, val, datetime.fromtimestamp(time));
                
        if len(crypto_sentiments) > 0:
            for crypto, sentiments in crypto_sentiments.items():
                if len(sentiments) > 0:
                    log(crypto + str(sentiments))
                    DAL.store_sentiments_social(client, sentiments, datetime.fromtimestamp(time), crypto);
        
        DAL.liveness_IAmAlive(client, "worker: sentiments social")
    except Exception as ex:
        log("exception")
        logErr(str(ex), traceback.format_exc())

def processAndValidateSocialMention(mention, crypto):
    retobj = { 'cats':{}, 'mention':mention,  'keeper':0, 'score':0 }
    try:
        editedMention=html.unescape(mention)
        words = nltk.wordpunct_tokenize(mention)
        # sentiment analysis:
        catMatrix = {}
        for cat in DICT.keys():
            count = len(DICT[cat].intersection([w.lower() for w in words]))
            if count > 0:
                catMatrix[cat] = count
        retobj['cats'] = catMatrix # categories matched (if any), eg.: {positivity: 1, uncertainty: 2}
        retobj['mention'] = editedMention # edited (nonASCII removed)
        if len(set(CRYPTO_socialKeywords[crypto]).intersection([w.lower() for w in words])) <= 0: # make sure the text contains any of the terms
            retobj['keeper']=0 # don't keep it
        elif detect(editedMention) != 'en':
            retobj['keeper']=0 
        else:
            score = socialMentionScore(editedMention)
            # if score < 0.90:
            #     retobj['keeper']=0 # don't keep it
            # else:
            #     retobj['score'] = score
            #     retobj['keeper']=1
            retobj['score'] = score
            retobj['keeper']=1

    except Exception as ex:
        log("exception")
        logErr(str(ex), traceback.format_exc())
    return retobj

def socialMentionScore(cleantxt):
    numbers = sum(c.isdigit() for c in cleantxt)
    lowercases = sum(c.islower() for c in cleantxt)
    uppercases = sum(c.isupper() for c in cleantxt)
    nonAlphaNum = sum(c not in [' ','.',',','?'] and not c.isalnum() for c in cleantxt)
    AlphaNum = sum(c.isalnum() for c in cleantxt)

    tokens = len(nltk.wordpunct_tokenize(cleantxt))
    divider = (tokens + numbers + uppercases + lowercases + nonAlphaNum + AlphaNum)
    good = (tokens + lowercases + AlphaNum) / (1 if divider == 0 else divider)
    return good #float : [0.0 ; 1.0]


def process_rdd_sentimentAnalysis_news(time, part_iterator):
    try:
        log("----------- %s :  News Sentiment --" % str(datetime.fromtimestamp(time)))
        keepers = [] # elements from 'out' which we should keep and display to users (batch insert)
        crypto_sentiments = {}

        count=0
        for part in part_iterator:
            count+=1
            try:
                crypto = part["crypto"]
                body = part["body"]
                title = part["title"]
                result = processAndValidateNewsMention(title, body, crypto) # sentiment analysis on title+body and decide whether to keep title or not
                if not crypto in crypto_sentiments:
                    crypto_sentiments[crypto] = {}
                for cat in result['cats']:
                    if not cat in crypto_sentiments[crypto]:
                        crypto_sentiments[crypto][cat] = 0 
                    crypto_sentiments[crypto][cat] += result['cats'][cat]
                if result['keeper'] == 1:
                    del part['body'] # we don't want body
                    keepers.append(part)
            except Exception as ex:
                log("exception")
                logErr(str(ex), traceback.format_exc())
                    
        # if len(keepers) > 0:
        #     DAL.store_mentions_news_extended_bulk(client, keepers, datetime.fromtimestamp(time));
            
        if len(crypto_sentiments) > 0:
            for crypto, sentiments in crypto_sentiments.items():
                if len(sentiments) > 0:
                    log(crypto + str(sentiments))
                    DAL.store_sentiments_news(client, sentiments, datetime.fromtimestamp(time), crypto);

        DAL.liveness_IAmAlive(client, "worker: sentiments news")
    except Exception as ex:
        log("exception")
        logErr(str(ex), traceback.format_exc())


def processAndValidateNewsMention(title, mention, crypto):
    retobj = { 'cats':{},  'keeper':0, }
    try:
        # the body of news is already pre-processed with nltk in newsProducer
        mention = title + "\n" + mention # let's prepend the title and analyze it in one shot
        body_words = nltk.wordpunct_tokenize(mention)
        title_words = nltk.wordpunct_tokenize(title)
        # sentiment analysis:
        catMatrix = {}
        for cat in DICT.keys():
            count = len(DICT[cat].intersection([w.lower() for w in body_words]))
            if count > 0:
                catMatrix[cat] = count
        
        retobj['cats'] = catMatrix # categories matched (if any), eg.: {positivity: 1, uncertainty: 2}
        if detect(mention) != 'en': # english only
           retobj['keeper']=0 # don't keep it
        else:
            retobj['keeper']=1
    except Exception as ex:
        log("exception")
        logErr(str(ex), traceback.format_exc())
    return retobj



if __name__=="__main__":
   main()

