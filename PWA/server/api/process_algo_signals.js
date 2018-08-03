

const funcs = require('./functions.js');

module.exports = async function (db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime, algoName) {
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
		//console.log(docs)

		query = {   'base_cur' 	: 	base_cur,
	                'quote_cur' : 	quote_cur,
	                'exchange'	: 	exchange,
	                'interval'	: 	interval,
	                'ts_interval': { '$gte': dtStart, '$lte': dtEnd, },
	                'name': algoName,
	            }
	    

	    var prevSignal = null;
	    var cursor =  db.collection('algo_signals').find(query);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var key = funcs.formatDateToString(new Date(doc.ts_interval));
				// keep only very first signal:
				
				if (key in docs) {
					if (!('signal' in docs[key])) {
						if (prevSignal == null || prevSignal != doc.signal.type) // only unique consecutive types
							// you may want to comment this 'if' when you want to show all generated signals
						{
							docs[key]['signal'] = doc.signal
							prevSignal = doc.signal.type;
						}
					}
				}


			}
		}

		

	} catch (error) {
		console.log("...")
		console.log(error);
	}
}