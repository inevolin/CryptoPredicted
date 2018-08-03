import sys
import os
sys.path.insert(0, '/home/cryptopredicted/')
import producerMgr
producer = producerMgr.create_kafkaProducer_secure()
import time

i = 0
while True:	

	promise= producerMgr.producer_send_test("body " + str(i), producer)
	i+=1
	time.sleep(0.2)


producer.flush()
