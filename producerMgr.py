
# Common functions used by the various producers, primarily sending messages into Kafka.

import json
from kafka import KafkaProducer
from kafka import KafkaClient
from mysettings import kafkaTopic_mentionsSocial, kafkaTopic_mentionsNews, dtNow, kafkaServerEndPoint, kafkaAuth

def create_kafkaProducer():
	return KafkaProducer(bootstrap_servers=kafkaServerEndPoint, sasl_mechanism=kafkaAuth['sasl_mechanism'], sasl_plain_username=kafkaAuth['sasl_plain_username'], sasl_plain_password=kafkaAuth['sasl_plain_password'] )


def producer_send_mentionsSocial(body, source, url, crypto, producer):
	
	ejs = json.dumps(
			{
				'body': body,
				'source': source,
				'url': url,
				'crypto': crypto,
				'type': 'social',
			}
		)

	producer.send(
		kafkaTopic_mentionsSocial,
		ejs.encode()
	)

	print(str(dtNow().strftime("%Y-%m-%d %H:%M:%S")) + " SENT:\t" + ejs)
	print()

def producer_send_mentionsNews(body, title, source, url, crypto, producer):
	ejs = json.dumps(
			{
				'body': body,
				'title': title,
				'source': source,
				'url': url,
				'crypto': crypto,
				'type': 'news',
			}
		)

	producer.send(
		kafkaTopic_mentionsNews,
		ejs.encode()
	)

	print(str(dtNow().strftime("%Y-%m-%d %H:%M:%S")) + " SENT:\t" + source)
	print()

def producer_send_test(body, producer):
	ejs = json.dumps(
			{
				'body': body,
			}
		)
	print(ejs)

	topic = 'topic_test'
	parts = producer.partitions_for(topic)
	print(parts)

	out = producer.send(
		topic,
		value=ejs.encode(),
		#partition=2
	)

	return out