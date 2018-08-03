



module.exports = async function (db, docs, id) {
	try {
		const {ObjectId} = require('mongodb');

		var query = {  _id: ObjectId(id) }

	    var cursor =  db.collection('algo_portfolios').find(query);
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