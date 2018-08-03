
module.exports = function(io, cryptoDB, auth, payments) {

	var functions = require('../api/functions.js')
	var process_algo_portfolios = require('../api/process_algo_portfolios.js')
	var process_algo_subbed_user = require('../api/process_algo_subbed_user.js')
	var process_algo_singlePortfolio = require('../api/process_algo_singlePortfolio.js')


	var exchange_nsps = io.of('/signals');
	exchange_nsps.on('connection', function(socket) {  
	    console.log('socketIO: Client connected  ('+socket.id+')');
	    var client_room = null;
	    
	    socket.on('join', function(roomObj) {
	    	console.log("socketIO: sesID: "+roomObj.sessionID)
	    	auth.authenticate(roomObj.sessionID, function(user) {
	    		payments.hasExclusiveAccess(user, function() {
	    			joined_fullyAuthenticated(socket, user, roomObj.exchange)
	    		}, function() {
	    			console.log("socketIO: Account limited (not premium)")
	    			socket.emit('message', 'Account limited (not premium)')
	    		})
	    	}, function() {
	    		console.log("socketIO: unable to auth")
	    		socket.emit('message', 'Unable to authenticate, try to logout and then log in again.')
	    	});
		});


		socket.on('chart', function(roomObj) {
	    	console.log("socketIO: sesID: "+roomObj.sessionID)
	    	auth.authenticate(roomObj.sessionID, function(user) {
	    		payments.hasExclusiveAccess(user, function() {
	    			getChart_fullyAuthenticated(socket, roomObj.id, roomObj.chart_id)
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
   		});
	});

	async function joined_fullyAuthenticated(socket, user, exchange) {
		var portfolios = [];
		var subs = [];

		await process_algo_portfolios(cryptoDB, portfolios, {exchange:exchange});
		await process_algo_subbed_user(cryptoDB, subs, user);

		for (var i = 0; i < subs.length; i++) {
			for (var j = 0; j < portfolios.length; j++) {
				if (portfolios[j].name == subs[i].name &&
					portfolios[j].base_cur == subs[i].base_cur &&
					portfolios[j].quote_cur == subs[i].quote_cur &&
					portfolios[j].interval == subs[i].interval &&
					portfolios[j].exchange == subs[i].exchange)
				{
					if (subs[i].type_sub=='email') {
						portfolios[j]['isSub_email'] = true;
					} else if (subs[i].type_sub=='telegram') {
						portfolios[j]['isSub_telegram'] = true;
					}
				}
			}	
		}
    	socket.emit('data', portfolios)
	}


	async function getChart_fullyAuthenticated(socket, id, chart_id) {
		var a = await obtain_Singleportfolio(id);
		a[0]['chart_id'] = chart_id;
    	socket.emit('chart', a)
	}



	var obtain_Singleportfolio = async function(id) {
		var docs = [];
		await process_algo_singlePortfolio(cryptoDB, docs, id);

		/*for (var i in docs) {
			var doc = docs[i]
			
			var keys = Object.keys(doc.portfolio)
			//keys = keys.splice(-120)
			var newfolio = {}
			for (var x in keys) {
				newfolio[keys[x]] = doc.portfolio[keys[x]]
			}
			doc.portfolio = newfolio
		}*/

		return docs;
	}
}