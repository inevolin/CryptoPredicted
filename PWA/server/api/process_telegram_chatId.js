

const funcs = require('./functions.js');

module.exports = async function (db, email) {
	try {
		
		var query = {
			email: email,
			//type_sub: subtype,
		}

	    var cursor =  db.collection('telegramChatIds').find(query);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if ('chatId' in doc) {
				return doc.chatId;
			}
		}

	} catch (error) {
		console.log(error);
	}
	return null;
}