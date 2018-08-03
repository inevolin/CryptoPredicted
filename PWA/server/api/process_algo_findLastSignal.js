

const funcs = require('./functions.js');

module.exports = async function (db, docs, interval, base_cur, quote_cur, exchange, algoName) {
	try {

		query = {   'base_cur' 	: 	base_cur,
	                'quote_cur' : 	quote_cur,
	                'exchange'	: 	exchange,
	                'interval'	: 	interval,
	                'name': algoName,
	            }
	    

	    var prevSignal = null;
	    var cursor =  db.collection('algo_signals').find(query).sort({_id:-1}).limit(1);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				docs.push(doc)
			}
		}

	} catch (error) {
		console.log("...")
		console.log(error);
	}
}