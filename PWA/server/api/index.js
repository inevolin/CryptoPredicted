
// the API endpoints :

module.exports = function(app, db) {
	app.get('/api/', (req, res) => {		
		_api_(req, res, db);
	});

	app.get('/api/signals/', (req, res) => {		
		_api_signals_(req, res, db);
	});

	app.get('/api/predictions/v1/', (req, res) => {		
		_api_predictions_v1_(req, res, db);
	});

	app.get('/api/predictions/v1/list/', (req, res) => {		
		_api_predictions_v1_list_(req, res, db);
	});

	app.get('/api/extended/social/', (req, res) => {		
		_api_extended_social_(req, res, db);
	});
	app.get('/api/extended/news/', (req, res) => {		
		_api_extended_news_(req, res, db);
	});

	app.get('/api/status', (req, res) => {		
		_api_status_(req, res, db);
	});
};


function _api_(req, res, db) {
	function validParams(req, res) {
		if(!req.query.type) {
			res.send("Error: missing type parameter");
			return false;
		}
		if (!req.query.exchange) {
	    	res.send("Error: missing exchange parameter");
	    	return false;
	    }
	    if (!req.query.base_cur) {
	    	res.send("Error: missing base_cur parameter");
	    	return false;
	    }
	    if (!req.query.quote_cur) {
	    	res.send("Error: missing quote_cur parameter");
	    	return false;
	    }
	    if (!req.query.interval) {
	    	res.send("Error: missing interval parameter");
	    	return false;
	    }
	    if (!req.query.historymins) {
	    	res.send("Error: missing historymins parameter");
	    	return false;
	    }
	    if (parseInt(req.query.interval) > parseInt(req.query.historymins)) {
	    	res.send("Error: interval must be smaller or equal to historymins");
	    	return false;	
	    }
	    if (!req.query.currentDateTime) {
	    	res.send("Error: missing currentDateTime parameter");
	    	return false;
	    } else if (isNaN(Date.parse(req.query.currentDateTime))) {
	    	res.send("Error: invalid datetime format for currentDateTime");
	    	return false;
	    } else if (new Date(Date.parse(req.query.currentDateTime)) > new Date()) {
	    	res.send("Error: currentDateTime cannot be in the future");
	    	return false;
	    }

	    return true;
	}

	if (!validParams(req, res)) {
		return false;
	}

	var interval 			= parseInt(req.query.interval);
	var historymins 		= parseInt(req.query.historymins);
	var exchange 			= req.query.exchange;
	var base_cur 			= req.query.base_cur;
	var quote_cur 			= req.query.quote_cur;
	var currentDateTime		= req.query.currentDateTime;
	var type 				= req.query.type;

	const process_exchange 				= require('./process_exchange.js');
	const process_social_mentions 		= require('./process_social_mentions.js');
	const process_news_mentions 		= require('./process_news_mentions.js');
	const process_social_sentiments 	= require('./process_social_sentiments.js');
	const process_news_sentiments 		= require('./process_news_sentiments.js');

	var docs = {};
	var promises = [];
	var typesArr = type.split(',');

	for (var i = 0; i < typesArr.length; i++) {
		var type = typesArr[i];
		switch (type) {
			case 'exchange':
				promises.push( process_exchange(db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );
				break;
			case 'socialMentions':
				promises.push( process_social_mentions(db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );
				break;
			case 'newsMentions':
				promises.push( process_news_mentions(db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );
				break;
			case 'socialSentiments':
				promises.push( process_social_sentiments(db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );
				break;
			case 'newsSentiments':
				promises.push( process_news_sentiments(db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );
				break;
			default:
				res.send("Error: unknown type: " + type);
				return false;
		}
	}

	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "X-Requested-With");

	Promise.all(promises).then(() => {
		const ordered = {};
		Object.keys(docs).sort().forEach(function(key) {
		  ordered[key] = docs[key];
		});
		res.send(ordered);
	});
}


function _api_signals_(req, res, db) {
	function validParams(req, res) {
		if (!req.query.algoName) {
	    	res.send("Error: missing algoName parameter");
	    	return false;
	    }
	    if (!req.query.exchange) {
	    	res.send("Error: missing exchange parameter");
	    	return false;
	    }
	    if (!req.query.base_cur) {
	    	res.send("Error: missing base_cur parameter");
	    	return false;
	    }
	    if (!req.query.quote_cur) {
	    	res.send("Error: missing quote_cur parameter");
	    	return false;
	    }
	    if (!req.query.interval) {
	    	res.send("Error: missing interval parameter");
	    	return false;
	    }
	    if (!req.query.historymins) {
	    	res.send("Error: missing historymins parameter");
	    	return false;
	    }
	    if (parseInt(req.query.interval) > parseInt(req.query.historymins)) {
	    	res.send("Error: interval must be smaller or equal to historymins");
	    	return false;	
	    }
	    if (!req.query.currentDateTime) {
	    	res.send("Error: missing currentDateTime parameter");
	    	return false;
	    } else if (isNaN(Date.parse(req.query.currentDateTime))) {
	    	res.send("Error: invalid datetime format for currentDateTime");
	    	return false;
	    } else if (new Date(Date.parse(req.query.currentDateTime)) > new Date()) {
	    	res.send("Error: currentDateTime cannot be in the future");
	    	return false;
	    }

	    return true;
	}

	if (!validParams(req, res)) {
		return false;
	}

	var interval 			= parseInt(req.query.interval);
	var historymins 		= parseInt(req.query.historymins);
	var exchange 			= req.query.exchange;
	var base_cur 			= req.query.base_cur;
	var quote_cur 			= req.query.quote_cur;
	var currentDateTime		= req.query.currentDateTime;
	var algoName 				= req.query.algoName;

	const process_algo_signals 				= require('./process_algo_signals.js');

	var docs = {};
	var promises = [];

	promises.push( process_algo_signals(db, docs, interval, historymins, base_cur, quote_cur, exchange, currentDateTime, algoName) );

	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "X-Requested-With");

	Promise.all(promises).then(() => {
		const ordered = {};
		Object.keys(docs).sort().forEach(function(key) {
		  ordered[key] = docs[key];
		});
		res.send(ordered);
	});
}


function _api_predictions_v1_(req, res, db) {
	function validParams(req, res) {
		if (!req.query.exchange) {
	    	res.send("Error: missing exchange parameter");
	    	return false;
	    }
	    if (!req.query.base_cur) {
	    	res.send("Error: missing base_cur parameter");
	    	return false;
	    }
	    if (!req.query.quote_cur) {
	    	res.send("Error: missing quote_cur parameter");
	    	return false;
	    }
	    if (!req.query.interval) {
	    	res.send("Error: missing interval parameter");
	    	return false;
	    }
	    if (!req.query.historymins) {
	    	res.send("Error: missing historymins parameter");
	    	return false;
	    }
	    if (parseInt(req.query.interval) > parseInt(req.query.historymins)) {
	    	res.send("Error: interval must be smaller or equal to historymins");
	    	return false;	
	    }
	    if (!req.query.currentDateTime) {
	    	res.send("Error: missing currentDateTime parameter");
	    	return false;
	    } else if (isNaN(Date.parse(req.query.currentDateTime))) {
	    	res.send("Error: invalid datetime format for currentDateTime");
	    	return false;
	    } else if (new Date(Date.parse(req.query.currentDateTime)) > new Date()) {
	    	res.send("Error: currentDateTime cannot be in the future");
	    	return false;
	    }

	    if (!req.query.mode) {
	    	res.send("Error: missing mode parameter");
	    	return false;
	    }

	    return true;
	}

	if (!validParams(req, res)) {
		return false;
	}

	var interval 			= parseInt(req.query.interval);
	var historymins 		= parseInt(req.query.historymins);
	var exchange 			= req.query.exchange;
	var base_cur 			= req.query.base_cur;
	var quote_cur 			= req.query.quote_cur;
	var currentDateTime		= req.query.currentDateTime;
	var type 				= req.query.type;
	var mode 				= req.query.mode;

	const funcs 						= require('./functions.js');
	const process_predictions_v1 		= require('./process_predictions_v1.js');
	const process_exchange 				= require('./process_exchange.js');

	var docs_pred = {};
	var docs_history = {};
	var docs_history_ext = {};

	var promises = [];	
	promises.push( process_exchange(db, docs_history, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );
	promises.push( process_predictions_v1(db, docs_pred, interval, historymins, base_cur, quote_cur, exchange, currentDateTime, mode) );

	Promise.all(promises).then(() => {
		if (Object.keys(docs_pred).length == 0) {
			res.send({'error': 188, 'message': 'No prediction(s) yet for the given the parameters.'});
			return;
		}

		var predicL = Object.keys(docs_pred[Object.keys(docs_pred)[0]]).length;
		var promises = [];

		historymins = predicL * interval
		currentDateTime = (new Date(currentDateTime)).getTime() + 60*1000*(predicL * interval)
		currentDateTime = funcs.formatDateToString(new Date(currentDateTime))
		promises.push( process_exchange(db, docs_history_ext, interval, historymins, base_cur, quote_cur, exchange, currentDateTime) );

		Promise.all(promises).then(() => {
			var docs = {
				'history' 		: docs_history,
				'history_ext'	: docs_history_ext,
				'predictions'	: docs_pred,
			};
			res.header("Access-Control-Allow-Origin", "*");
			res.header("Access-Control-Allow-Headers", "X-Requested-With");
			res.send(docs);
		}).catch(function (error) {
	  		console.error(error)
		});


	}).catch(function (error) {
  		console.error(error)
	});
}

function _api_predictions_v1_list_(req, res, db) {
	function validParams(req, res) {
		if (!req.query.exchange) {
	    	res.send("Error: missing exchange parameter");
	    	return false;
	    }
	    if (!req.query.base_cur) {
	    	res.send("Error: missing base_cur parameter");
	    	return false;
	    }
	    if (!req.query.quote_cur) {
	    	res.send("Error: missing quote_cur parameter");
	    	return false;
	    }
	    if (!req.query.interval) {
	    	res.send("Error: missing interval parameter");
	    	return false;
	    }
	    if (!req.query.historymins) {
	    	res.send("Error: missing historymins parameter");
	    	return false;
	    }
	    if (parseInt(req.query.interval) > parseInt(req.query.historymins)) {
	    	res.send("Error: interval must be smaller or equal to historymins");
	    	return false;	
	    }
	    if (!req.query.currentDateTime) {
	    	res.send("Error: missing currentDateTime parameter");
	    	return false;
	    } else if (isNaN(Date.parse(req.query.currentDateTime))) {
	    	res.send("Error: invalid datetime format for currentDateTime");
	    	return false;
	    } else if (new Date(Date.parse(req.query.currentDateTime)) > new Date()) {
	    	res.send("Error: currentDateTime cannot be in the future");
	    	return false;
	    }

	    if (!req.query.mode) {
	    	res.send("Error: missing mode parameter");
	    	return false;
	    }

	    return true;
	}

	if (!validParams(req, res)) {
		return false;
	}

	var interval 			= parseInt(req.query.interval);
	var historymins 		= parseInt(req.query.historymins);
	var exchange 			= req.query.exchange;
	var base_cur 			= req.query.base_cur;
	var quote_cur 			= req.query.quote_cur;
	var currentDateTime		= req.query.currentDateTime;
	var type 				= req.query.type;
	var mode 				= req.query.mode;

	const funcs 						= require('./functions.js');
	const process_predictions_v1_all 		= require('./process_predictions_v1_all.js');

	var docs_pred = {};

	var promises = [];	
	promises.push( process_predictions_v1_all(db, docs_pred, interval, historymins, base_cur, quote_cur, exchange, currentDateTime, mode) );

	Promise.all(promises).then(() => {
		if (Object.keys(docs_pred).length == 0) {
			res.send({'error': 189, 'message': 'No prediction(s) yet for the given the parameters.'});
			return;
		}

		var docs = docs_pred
		res.header("Access-Control-Allow-Origin", "*");
		res.header("Access-Control-Allow-Headers", "X-Requested-With");
		res.send(docs);


	}).catch(function (error) {
  		console.error(error)
	});
}

function _api_extended_social_(req, res, db) {
	function validParams(req, res) {
	    if (!req.query.base_cur) {
	    	res.send("Error: missing base_cur parameter");
	    	return false;
	    }
	    if (!req.query.interval) {
	    	res.send("Error: missing interval parameter");
	    	return false;
	    }
	    if (parseInt(req.query.interval) > parseInt(req.query.historymins)) {
	    	res.send("Error: interval must be smaller or equal to historymins");
	    	return false;	
	    }
	    if (!req.query.currentDateTime) {
	    	res.send("Error: missing currentDateTime parameter");
	    	return false;
	    } else if (isNaN(Date.parse(req.query.currentDateTime))) {
	    	res.send("Error: invalid datetime format for currentDateTime");
	    	return false;
	    } else if (new Date(Date.parse(req.query.currentDateTime)) > new Date()) {
	    	res.send("Error: currentDateTime cannot be in the future");
	    	return false;
	    }

	    return true;
	}

	if (!validParams(req, res)) {
		return false;
	}

	var interval 			= parseInt(req.query.interval);
	var base_cur 			= req.query.base_cur;
	var currentDateTime		= req.query.currentDateTime;

	const process_social_mentions_extended 				= require('./process_social_mentions_extended.js');

	var docs = [];
	var promises = [];

	promises.push( process_social_mentions_extended(db, docs, interval, base_cur, currentDateTime) );

	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "X-Requested-With");

	Promise.all(promises).then(() => {
		res.send(docs);
	});
}

function _api_extended_news_(req, res, db) {
	function validParams(req, res) {
	    if (!req.query.base_cur) {
	    	res.send("Error: missing base_cur parameter");
	    	return false;
	    }
	    if (!req.query.interval) {
	    	res.send("Error: missing interval parameter");
	    	return false;
	    }
	    if (parseInt(req.query.interval) > parseInt(req.query.historymins)) {
	    	res.send("Error: interval must be smaller or equal to historymins");
	    	return false;	
	    }
	    if (!req.query.currentDateTime) {
	    	res.send("Error: missing currentDateTime parameter");
	    	return false;
	    } else if (isNaN(Date.parse(req.query.currentDateTime))) {
	    	res.send("Error: invalid datetime format for currentDateTime");
	    	return false;
	    } else if (new Date(Date.parse(req.query.currentDateTime)) > new Date()) {
	    	res.send("Error: currentDateTime cannot be in the future");
	    	return false;
	    }

	    return true;
	}

	if (!validParams(req, res)) {
		return false;
	}

	var interval 			= parseInt(req.query.interval);
	var base_cur 			= req.query.base_cur;
	var currentDateTime		= req.query.currentDateTime;

	const process_news_mentions_extended 				= require('./process_news_mentions_extended.js');

	var docs = [];
	var promises = [];

	promises.push( process_news_mentions_extended(db, docs, interval, base_cur, currentDateTime) );

	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "X-Requested-With");

	Promise.all(promises).then(() => {
		res.send(docs);
	});
}


async function _api_status_(req, res, db) {
	
	var cursor =  db.collection('liveness').find({});
	var docs = [];
	while(await cursor.hasNext()) {
		const doc = await cursor.next();
		if (doc != null) {
			delete doc._id;

			doc['last_notification_minutes'] = Math.round( (new Date()-doc.timestamp)/1000/60 );

			docs.push(doc);
		}
	}

	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "X-Requested-With");

	res.send(docs);
}