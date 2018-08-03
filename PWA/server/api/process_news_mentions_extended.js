

/*

	db.mentionsExtendedNews.createIndex( { "crypto": 1, "timestamp": 1 } )
	
	this index made us improve speed from 600-3000ms to 125ms
*/


const funcs = require('./functions.js');

module.exports = async function (db, docs, interval, base_cur, currentDateTime) {
	try {
		/*
			We shall include everything until the current datetime.
			We will also not use any caching, so we can view real-time data.
		*/
		
		var dtStart 	= new Date(Date.parse(currentDateTime));
		if (dtStart > new Date()) {
			dtStart = new Date();
		}
		
		var dtEnd	= new Date(dtStart.getTime() + (interval) * 60*1000); 
		dtEnd = funcs.roundDateToInterval(dtEnd, interval);

		var query = { 'timestamp'	: { '$gte': dtStart, '$lt': dtEnd, } }
		if (base_cur !== "-1") query['crypto'] = base_cur;
	        
	    // console.log(JSON.stringify(query));

		var cursor =  db.collection('mentionsExtendedNews').find(query);
		var tempDocs = {};
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				var newDoc = {};
				newDoc['title'] = doc['title']
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
