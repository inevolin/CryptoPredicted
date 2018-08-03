

const funcs = require('./functions.js');

module.exports = async function (db, docs, query) {
	try {

	    var cursor =  db.collection('algoSubs').find(query);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				docs.push(doc)
			}
		}

	} catch (error) {
		console.log(error);
	}
}