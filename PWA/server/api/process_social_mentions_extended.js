

/*

	db.mentionsExtendedSocial.createIndex( { "crypto": 1, "timestamp": 1 } )
	
	this index made us improve speed from 600-3000ms to 125ms
*/


const funcs = require('./functions.js');

module.exports = async function (db, docs, interval, base_cur, currentDateTime) {
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
		var dtStart	= new Date(dtEnd.getTime() - (interval) * 60*1000); 
		dtStart = funcs.roundDateToInterval(dtStart, interval);

		var query =  { 'timestamp'	: { '$gte': dtStart, '$lte': dtEnd, } }
		if (base_cur !== "-1") query['crypto'] = base_cur;
	        
	    //console.log(JSON.stringify(query));

		var cursor =  db.collection('mentionsExtendedSocial').find(query);
		var tempDocs = {};
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var newDoc = {};
				newDoc['body'] = doc['body']
				newDoc['source'] = doc['source']
				newDoc['url'] = doc['url']
				newDoc['timestamp'] = funcs.formatDateToString(new Date(doc['timestamp']))
				docs.push(newDoc)
			}
		}
		

	} catch (error) {
		console.log(error);
	}
}
