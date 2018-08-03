
/*

	db.predictions_v1.createIndex( { "base_cur": 1, "quote_cur": 1, "interval": 1, "timestamp": 1, "exchange": 1 } )

*/

const funcs = require('./functions.js');

module.exports = async function (db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime, mode) {
	try {
		/*
			We shall include everything until the current datetime.
			We will also not use any caching, so we can view real-time data.
		*/
		
		var dtTime 	= new Date(Date.parse(currentDateTime));
		var dtStart 	= new Date( new Date(Date.parse(currentDateTime)).getTime() - 1000*60*historymins );

		var query = {   'base_cur'	: base_cur,
						'quote_cur'	: quote_cur,
						'interval'	: interval,
						'exchange'	: exchange,
	                	'timestamp'	: dtTime,
	                	'mode'		: mode,
	                	//'timestamp'	: {'$gte':dtStart, '$lte': dtTime}, // --> make sure you are sorting ascending (_id:1), otherwise older values will mess up newest ones ; make sure we don't extend data on the line-chart
	                }
		var cursor =  db.collection('predictions_v1').find(query).sort({_id:1});

		
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var key = doc['stringUID'];
				var val = doc['data'];
				var newVal = {};
				for (var i = 0; i < val.length; i++) {
					var ikey = funcs.formatDateToString(val[i]['timestamp']);
					newVal[ikey] = val[i];
					delete newVal[ikey]['timestamp'];
				}
				funcs.addDocument(docs, key, newVal);
			}
		}
		
	} catch (error) {
		console.log(error);
	}
}
