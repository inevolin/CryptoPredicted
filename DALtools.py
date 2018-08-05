
# This script can be used for misc. operations on the database.
# It's not actively used, unless you need to do some manual maintenance/operations.

from datetime import datetime
import pymongo
import sys
import json
import time
from pymongo import MongoClient

import DAL

client = DAL.openConnection()
db=client.crypto


def remove_all_between(start_incl, end_incl):
	# we can use this function to remove data in gaps, so the graph will close up (interpolate the entire period)
	pipeline =  {	
				'timestamp':
					{	'$gte' : start_incl,
						'$lte' : end_incl,
					},	
			
		}
	
	#print(pipeline)
	cursor = db.get_collection('currencies').remove(pipeline);
	cursor['col'] = 'currencies'
	print(cursor)

	cursor = db.get_collection('mentionsSocial').remove(pipeline);
	cursor['col'] = 'mentionsSocial'
	print(cursor)

	cursor = db.get_collection('mentionsExtendedSocial').remove(pipeline);
	cursor['col'] = 'mentionsExtendedSocial'
	print(cursor)

	cursor = db.get_collection('sentimentsSocial').remove(pipeline);
	cursor['col'] = 'sentimentsSocial'
	print(cursor)

	cursor = db.get_collection('mentionsNews').remove(pipeline);
	cursor['col'] = 'mentionsNews'
	print(cursor)

	cursor = db.get_collection('mentionsExtendedNews').remove(pipeline);
	cursor['col'] = 'mentionsExtendedNews'
	print(cursor)

	cursor = db.get_collection('sentimentsNews').remove(pipeline);
	cursor['col'] = 'sentimentsNews'
	print(cursor)


start = datetime.strptime('2018-01-05 07:00:00', '%Y-%m-%d %H:%M:%S') # must be local EST
end = datetime.strptime('2018-01-05 07:59:00', '%Y-%m-%d %H:%M:%S') # must be local EST
#remove_all_between(start,end)




# import DAL
# client = DAL.openConnection()
# db = DAL.selectDB(client)

# pipeline = [ {"$match": {}},  {"$out": "exchanges_"}, ]
# db.exchanges.aggregate(pipeline)






# import DAL
# client = DAL.openConnection()
# db = DAL.selectDB(client)

# cursor = db.mentionsNewsExtended.find()
# for doc in cursor:
#     try:
#         db.mentionsExtendedNews.insert(doc)
#     except Exception as  ex:
#         print(ex)




# import DAL
# client = DAL.openConnection()
# db = DAL.selectDB(client)

# cursor = db.exchanges_.find()
# buffer = []
# for doc in cursor:
#     if len(buffer) == 10000:
#     	try:
#     		db.exchanges.insert_many(buffer, ordered=False)
#     	except:
#     		pass
#     	buffer = []
#     buffer.append(doc)

# if len(buffer) > 0:
# 	try:
# 		db.exchanges.insert_many(buffer, ordered=False)
# 	except:
# 		pass
