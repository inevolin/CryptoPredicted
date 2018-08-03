


const funcs = require('./functions.js');

// db.sentimentsNews.createIndex( { "crypto": 1, "timestamp": 1, } )

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
	                'positive' : {'$sum' : '$sentiments.positive'},
	        		'negative' : {'$sum' : '$sentiments.negative'},
	            }
	        },
	        {'$sort' : {
	        	'_id' : 1
	        }}
	    ]
	    //console.log(JSON.stringify(query));

		var cursor =  db.collection('sentimentsNews').aggregate(query);
		
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var key = funcs.formatDateToString(new Date(doc._id.interval));
				doc['source'] = ("source" in doc['_id'] ? doc['_id']['source'] : "aggregated");
				delete doc['_id'];
				var newDoc = { sentiments : { news : { }, 'news_delta' : 0, } };
				newDoc['sentiments']['news']['pos'] = doc['positive'];
				newDoc['sentiments']['news']['neg'] = doc['negative'];
				newDoc['sentiments']['news_delta'] = doc['positive']-doc['negative'];
				funcs.addDocument(docs, key, newDoc);
			}
		}
		
	} catch (error) {
		console.log(error);
	}
}
