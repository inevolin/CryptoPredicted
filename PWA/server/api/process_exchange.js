
/*

	db.exchanges.createIndex( { "base_cur": 1, "quote_cur": 1, "interval": 1, "exchange": 1 } )
	
	this index made us improve speed from 600-3000ms to 125ms
*/

const funcs = require('./functions.js');

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
	            {   'base_cur' 	: 	base_cur,
	                'quote_cur' : 	quote_cur,
	                'exchange'	: 	exchange,
	                'timestamp': { '$gte': dtStart, '$lte': dtEnd, },
	            }
	        },
	        {'$group' : 
	            {   '_id' : {	interval : 	{
	            					$add: [
						        	{ $subtract: [
						            	{ $subtract: [ "$timestamp", new Date(0) ] },
							            	{ $mod: [
							                { $subtract: [ "$timestamp", new Date(0) ] },
						    	           	1000 * 60 * interval
					            			]}
					        		]}
					    			, new Date(0)]},
					    	},
	                'low' : {'$min':'$data.low'},
	                'high' : {'$max':'$data.high'},
	                'open': {'$first':'$$ROOT.data.open'},
	                'close': {'$last':'$$ROOT.data.close'},
	                'volume':{'$sum':'$data.volume'},
	                'trades':{'$sum':'$data.trades'},
	                'count': {'$sum':1},
	            }
	        },
	        {'$sort' : {
	        	'_id' : 1
	        }}
	    ]

		var cursor =  db.collection('exchanges').aggregate(query);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var key = funcs.formatDateToString(new Date(doc._id.interval));
				delete doc['_id'];
				funcs.addDocument(docs, key, doc);
			}
		}
	} catch (error) {
		console.log(error);
	}
}