

const funcs = require('./functions.js');

module.exports = async function (db, docs, query) {
	try {

	    var cursor =  db.collection('algo_portfolios').find(query);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				
				delete doc.portfolio

				docs.push(doc)
			}
		}

		

	} catch (error) {
		console.log(error);
	}
}