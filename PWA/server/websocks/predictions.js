
module.exports = function(io, cryptoDB, auth, payments) {


	var predictionsAPI = require('../api/process_predictions_v1.js')
	var functions = require('../api/functions.js')
	var exchangeAPI = require('../api/process_exchange.js')

	function roomObjToString(o) {
		return 	"predic_"
				+"_"+	o.base_cur
				+"_"+ 	o.quote_cur
				+"_"+ 	o.exchange
				+"_"+ 	o.interval
				+"_"+ 	o.mode
	}

	var rooms = {};

	var exchange_nsps = io.of('/predictions');
	exchange_nsps.on('connection', function(socket) {  
	    console.log('socketIO: Client connected  ('+socket.id+')');
	    var client_room = null;
	    
	    socket.on('join', function(roomObj) {
	    	console.log("socketIO: sesID: "+roomObj.sessionID)
	    	auth.authenticate(roomObj.sessionID, function(user) {
	    		payments.hasExclusiveAccess(user, function() {
	    			client_room = roomObjToString(roomObj);
	    			joined_fullyAuthenticated(roomObj, client_room, socket)
	    		}, function() {
	    			console.log("socketIO: Account limited (not premium)")
	    			socket.emit('message', 'Account limited (not premium)')
	    		})
	    	}, function() {
	    		console.log("socketIO: unable to auth")
	    		socket.emit('message', 'Unable to authenticate, try to logout and then log in again.')
	    	});
		});


		socket.on('consult', function(roomObj) {
	    	console.log("socketIO: sesID: "+roomObj.sessionID)
	    	auth.authenticate(roomObj.sessionID, function(user) {
	    		payments.hasExclusiveAccess(user, async function() {
	    			
	    			var docs = await consultData(roomObj, new Date(roomObj.datetime))
	    			socket.emit('consult', docs);

	    		}, function() {
	    			console.log("socketIO: Account limited (not premium)")
	    			socket.emit('message', 'Account limited (not premium)')
	    		})
	    	}, function() {
	    		console.log("socketIO: unable to auth")
	    		socket.emit('message', 'Unable to authenticate, try to logout and then log in again.')
	    	});
		});


   		socket.on('disconnect', function() {
   			console.log("socketIO: discon");
   			if (client_room in rooms && typeof rooms[client_room] !== 'undefined') {
	   			rooms[client_room].clients--;
	   			if (rooms[client_room].clients == 0) {
	   				delete rooms[client_room];
	   			}
   			}
   		});
	});

	function joined_fullyAuthenticated(roomObj, client_room, socket) {
    	console.log("socketIO: room: " + client_room)
        socket.join(client_room);
        if (!(client_room in rooms)) {
        	rooms[client_room] = {roomObj:roomObj, clients: 0, data: null};
        }
        rooms[client_room].clients++;

        if (rooms[client_room].data !== null) {
        	console.log("socketIO: servering from cache");
        	socket.emit('data', rooms[client_room].data);
        } else {
        	console.log("socketIO: empty cache, let's help a brother out");
        	// we don't know what the timer interval is, so if there's no cache obtain data the hard way
	        obtainDataAndCache(client_room, roomObj, function(client_room, data) {
		        socket.emit('data', data);
	        });
        }
	}


	function periodic() {
		for (var room in rooms) {
			var client_room = room;
			var roomObj = rooms[room].roomObj;
			console.log("socketIO: "+client_room+": "+rooms[room].clients)
			obtainDataAndCache(client_room, roomObj, function(client_room, data) {
				console.log("socketIO: periodic: "+client_room);
				exchange_nsps.in(client_room).emit('data', data);
	        });

		}
	}
	setInterval(periodic, 1000*10); // every 1000 * X seconds


	var consultData = async function (roomObj, datetime) {
		var docs_predic = await obtain_predictions(roomObj, functions.roundDateToInterval(datetime, roomObj.interval));

		var predictions = 12
		var datetime_ext = new Date(datetime.getTime() + (1000*60*roomObj.interval)*predictions)
		var docs_price = await obtain_price(roomObj, datetime_ext);

		if (roomObj.mode == "production")
			__anchorPredictionsToPrice(docs_price, docs_predic);

		var docs = {
			predictions: docs_predic,
			price: docs_price,
			base_cur: roomObj.base_cur,
			quote_cur: roomObj.quote_cur,
		}

		return docs
	}
	var obtainDataAndCache = async function (client_room, roomObj, next) {
		console.log(roomObj)
		var docs_predic = await obtain_predictions(roomObj, functions.roundDateToInterval(new Date(), roomObj.interval));
		var docs_price = await obtain_price(roomObj, new Date());

		if (roomObj.mode == "production")
			__anchorPredictionsToPrice(docs_price, docs_predic);


		var docs = {
			predictions:  docs_predic,
			price: docs_price,
			base_cur: roomObj.base_cur,
			quote_cur: roomObj.quote_cur,
		}
		
		if (client_room in rooms)
			rooms[client_room].data = docs;
		next(client_room, docs);
	
	}

	function __anchorPredictionsToPrice(docs_price, docs_predic) {
		try {
			//return docs_predic.avg = new Object();

			var preds_ts = Object.keys(docs_predic[Object.keys(docs_predic)[0]])
			var preds = Object.values(docs_predic[Object.keys(docs_predic)[0]])
			if (!preds.length) return;

			var open_ = preds.slice(0)[0].open
			var close_ = preds.slice(0)[0].close
			var low_ = preds.slice(0)[0].low
			var high_ = preds.slice(0)[0].high


			if (preds_ts[0] in docs_price) {
				var _open = docs_price[preds_ts[0]].open
				var _close = docs_price[preds_ts[0]].close
				var _low = docs_price[preds_ts[0]].low
				var _high = docs_price[preds_ts[0]].high
			} else {
				var _open = Object.values(docs_price).slice(-1)[0].open
				var _close = Object.values(docs_price).slice(-1)[0].close
				var _low = Object.values(docs_price).slice(-1)[0].low
				var _high = Object.values(docs_price).slice(-1)[0].high
			}


			var xopen = _open / open_
			var xclose = _close / close_
			var xlow = _low / low_
			var xhigh = _high / high_

			for (var uid in docs_predic) {
				var obj = docs_predic[uid];
				for (var dt in obj) {
					docs_predic[uid][dt].open *= xopen
					docs_predic[uid][dt].close *= xclose
					docs_predic[uid][dt].low *= xlow
					docs_predic[uid][dt].high *= xhigh
				}
			}

		} catch(err) {
			console.log(err)
		}
	}

	var obtain_price = async function(roomObj, datetime) {
		var docs_price = {};
		await exchangeAPI(cryptoDB,
			docs_price, 				// output
			roomObj.interval,			// interval
			roomObj.interval * 50,		// historymins
			roomObj.base_cur,
			roomObj.quote_cur,
			roomObj.exchange,
			datetime
		)
		return docs_price;
	}

	var obtain_predictions = async function(roomObj, datetime) {
		var docs_predic = {};
		await predictionsAPI(cryptoDB,
			docs_predic, 				// output
			roomObj.interval,			// interval
			roomObj.interval * 50,		// historymins
			roomObj.base_cur,
			roomObj.quote_cur,
			roomObj.exchange,
			datetime,
			roomObj.mode
		)
		
		var new_predic = {"avg" : {}} // { low: [], open: [], high: [], close: []}
		for (var uid in docs_predic) {
			for (var dt in docs_predic[uid]) {
				
				var val = docs_predic[uid][dt]

				if (!(dt in new_predic["avg"]))
					new_predic["avg"][dt] = {}

				if (!('low' in new_predic["avg"][dt]))
					new_predic["avg"][dt]['low'] = []
				if (!('open' in new_predic["avg"][dt]))
					new_predic["avg"][dt]['open'] = []
				if (!('close' in new_predic["avg"][dt]))
					new_predic["avg"][dt]['close'] = []
				if (!('high' in new_predic["avg"][dt]))
					new_predic["avg"][dt]['high'] = []

				new_predic["avg"][dt]['low'].push(val.low)
				new_predic["avg"][dt]['open'].push(val.open)
				new_predic["avg"][dt]['close'].push(val.close)
				new_predic["avg"][dt]['high'].push(val.high)

			}
		}
		for (var dt in new_predic["avg"]) {
			var val = new_predic["avg"][dt]
			new_predic["avg"][dt]['low'] = (val.low.reduce((a, b) => a + b, 0)) / val.low.length
			new_predic["avg"][dt]['open'] = (val.open.reduce((a, b) => a + b, 0)) / val.open.length
			new_predic["avg"][dt]['close'] = (val.close.reduce((a, b) => a + b, 0)) / val.close.length
			new_predic["avg"][dt]['high'] = (val.high.reduce((a, b) => a + b, 0)) / val.high.length
		}
		var sortedKeys=Object.keys(new_predic["avg"]).sort()
		var sortedDict = {};
		for (var x in sortedKeys) {
			var key = sortedKeys[x];
			sortedDict[key] = new_predic['avg'][key]
		}
		new_predic['avg'] = sortedDict;

		return new_predic;
	}


	function standardDeviation(values){
		var avg = average(values);

		var squareDiffs = values.map(function(value){
		var diff = value - avg;
		var sqrDiff = diff * diff;
			return sqrDiff;
		});

		var avgSquareDiff = average(squareDiffs);

		var stdDev = Math.sqrt(avgSquareDiff);
		return stdDev;
	}

	function average(data){
		var sum = data.reduce(function(sum, value){
			return sum + value;
		}, 0);

		var avg = sum / data.length;
		return avg;
	}


	var _eval_productionPredictions = (async() => {
		// we shall not compute pct% accuracy, because it's usually +99% with a low stdv.
		// for BTC the predictions vary on average 0 to $50 from the real price
		// instead we should persuit generating BuySell signals and displaying its 24h ROI
		var interval = 10;
		var dtw = require('dynamic-time-warping');
		var distFunc = function( a, b ) {
			return Math.abs( a - b );
		};
		
		var roomObj = {
			base_cur: 'BTC',
			quote_cur: 'USDT',
			exchange: 'binance',
			interval: interval,
			mode: 'production',
			//mode: 'test',
		}
		var dtStart = new Date(Date.parse('18 Apr 2018 20:00:00 GMT'));
		var dtws = []
		for (var j = 0; j < 144*10; j++) {

			var datetime = new Date(dtStart.getTime() + (1000*60*interval) * j)
			
			var docs = await consultData(roomObj, datetime)
			var prices = []
			var predictions = []
			for (var dt in docs.price) {
				if (dt in docs.predictions.avg) {
					prices.push( (docs.price[dt].low+docs.price[dt].high)/2 )
					predictions.push( (docs.predictions.avg[dt].low+docs.predictions.avg[dt].high)/2 )
				}
			}
			prices.shift()
			predictions.shift()
			
			if (prices.length > 0 && prices.length == predictions.length) {
				/* var out = new dtw.DynamicTimeWarping(prices, predictions, distFunc);
				out = out.getDistance()
				console.log("DTW dist: " + out)
				dtws.push(out) */
				var dxs = []
				for (var i in prices) {
					var dx = ((prices[i] - predictions[i])/prices[i])**2
					dxs.push(dx)
				}
				dtws.push(Math.sqrt(average(dxs)))
			}
		}
		console.log("-----------")
		console.log( average(dtws) )
		console.log( standardDeviation(dtws) )
		console.log("-----------")

		console.log("helloooo")
	});
	// _eval_productionPredictions();

}