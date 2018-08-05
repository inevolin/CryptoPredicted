
# this script connects to your Telegram account and listens for new messages sent to all your chats (groups, private chats, channels, bots, ...).
# make sure you're not using your Telegram account for sensitive conversations, because it may be recorded by this scirpt.
# you can however add filters in this script, to only listen to specific groups/channels.

# On the other hand, only one API connection can be established at any time (if I'm not mistaken).

# Finally, if you want to scrape messages regarding crypto currencies, make sure you join public (super) groups and channels on your Telegram app, where people talk about crypto currencies --.

# Telegram sessions.... ###
# The first time you start this script it will prompt you for your phone number (e.g. +14984984949)
# once you gave it your phone number, you will receive a Telegram notification on your app with a code,
# so you will prompted for this code.
# once you have entered that code this script creates a session file.
# so the next time it won't prompt you again.
# this is done only the first time you run it, unless a session file already exists.


from pyrogram import Client, MessageHandler
from pyrogram.api import types

import praw
import json
import nltk
import sys
import os
import time
sys.path.insert(0, '/home/cryptopredicted/')
import producerMgr
from mysettings import CRYPTO_socialKeywords, dtNow, createLogger
import DAL

logErr = createLogger("telegramProducer_error", "telegramProducer_error")
log = createLogger("telegramProducer_info", "telegramProducer_info")

dalclient = DAL.openConnection()
producer = producerMgr.create_kafkaProducer()
CryptoMapping = list(CRYPTO_socialKeywords.items())



def update_handler(client, message):
	print(message)
	print(type(message)) # pyrogram message type/class
	log.info(message)
	try:
		DAL.liveness_IAmAlive(dalclient, "producer: telegram")
		if message['text'] is not None:
			msg = (message['text'].encode('utf-8')).decode('utf-8')
			channelName = message['chat']['title']
			print() # channel's name
			print( msg ) # message
			print( " ")
			# print(update.message.date) # UTC timestamp of message
			
			sbody = nltk.wordpunct_tokenize(msg.lower())
			for crypto, kws in CryptoMapping:
				for kw in kws:
					if kw in sbody:
						print("sending to kafka <"+crypto+">: " + msg)
						log.info("sending to kafka <"+crypto+">: " + msg)
						producerMgr.producer_send_mentionsSocial(msg, 'telegram', channelName, crypto, producer )
		else:
			print("non-text message (sticker or image)")
			log.info("non-text message (sticker or image)")
							

	except Exception as ex:
		print(ex)
		pass # not every update is a message, some are misc. notifications
		logErr.critical(str(ex), exc_info=True)


def phone_code_callback():
    code = "85257"  # Get your code programmatically
    return code  # Must be string, e.g., "12345"

log.info("trying to connect...")
client = Client(
	 session_name="/home/cryptopredicted/producers/cryptopredicted",
     api_id=224334,
     api_hash="820e1291cb0d8ef7455b3da30a4f3438",

     #session_name="/home/cryptopredicted/producers/cryptopredicted_vanja",
     #api_id=317029,
     #api_hash="88e30a2ddffd981c5ff7a58aa8871ca2",
)
log.info("logged in")
print("logged in")

#client.set_update_handler(update_handler)
client.add_handler(MessageHandler(update_handler))
client.start()
client.idle()


# https://docs.pyrogram.ml/resources/UpdateHandling
# https://github.com/pyrogram/pyrogram/blob/master/examples/advanced_echo2.
