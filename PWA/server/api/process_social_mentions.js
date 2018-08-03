

const funcs = require('./functions.js');

// db.mentionsSocial.createIndex( { "crypto": 1, "timestamp": 1, } )

module.exports = async function (db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) {
	try {
		/*
			We shall include everything until the current datetime.
			We will also not use any caching, so we can view real-time data.
		*/
		
		var dtEnd 	= new Date(Date.parse(currentDateTime));
		if (dtEnd > new Date()) {
			dtEnd = new Date();
		}
		// don't round dtEnd, because we want real-time data (even if incomplete)
		// make sure the very first interval is complete: round dtStart to a whole interval.
		var dtStart	= new Date(dtEnd.getTime() - (historymins-interval) * 60*1000); 
		dtStart = funcs.roundDateToInterval(dtStart, interval);

		var query = [
	        {'$match' : 
	            {   'crypto'	: base_cur,
	                'timestamp'	: { '$gte': dtStart, '$lte': dtEnd, },
	            }
	        },
	        {'$group' : 
	            {   '_id' : {	interval:{$add: [
						        	{ $subtract: [
						            	{ $subtract: [ "$timestamp", new Date(0) ] },
							           	{ $mod: [
							               	{ $subtract: [ "$timestamp", new Date(0) ] },
						    	           	1000 * 60 * interval
					            		]}
					        		]}
					    		, new Date(0)]},
					    		'source': '$source',
						},
	                'count' : {'$sum' : '$mentions'},
	            }
	        },
	        {'$sort' : {
	        	'_id' : 1
	        }}
	    ]
	    //console.log(JSON.stringify(query));

		var cursor =  db.collection('mentionsSocial').aggregate(query);
		var tempDocs = {};
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var key = funcs.formatDateToString(new Date(doc._id.interval));
				doc['source'] = ("source" in doc['_id'] ? doc['_id']['source'] : "aggregated");
				delete doc['_id'];
				var newDoc = { mentions : { social : { }, 'social_sum' : 0, } };
				newDoc['mentions']['social'][doc['source']] = doc['count'];
				funcs.addDocument(tempDocs, key, newDoc);
			}
		}
		for (var key in tempDocs) {
			for (var source in tempDocs[key]['mentions']['social']) {
				tempDocs[key]['mentions']['social_sum'] += tempDocs[key]['mentions']['social'][source];
			}
		}
		const deepAssign = require('deep-assign');
		deepAssign(docs, tempDocs);
	} catch (error) {
		console.log(error);
	}
}
