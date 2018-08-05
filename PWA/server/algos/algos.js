
const MongoClient   = require('mongodb').MongoClient;
const dbCfg         = require('../db.js');
const schedule 		= require('node-schedule');
//const notifiers         = require('../notifiers/')(cryptoDB);


//reference to working algorithms:
const algo_pistis_1 = require('./algo_pistis_1.js')
const algo_pistis_1_1 = require('./algo_pistis_1_1.js')
const algo_voltra_1 = require('./algo_voltra_1.js')
const algo_macd_1 = require('./algo_macd_1.js')
const algo_macd_2 = require('./algo_macd_2.js')

const algo_demo_1 = require('./algo_demo_1.js')


// included algorithms:
async function work(cryptoDB, base_cur, quote_cur, exchange, interval, historymins, FIRST_RUN) {
	
	var currentDatetime = new Date();

	const core = require('./core.js')(cryptoDB);
	var inp = await core.obtain_price(cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime)
	algo_pistis_1(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN)
	algo_pistis_1_1(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN)
	algo_voltra_1(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN)
	algo_macd_1(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN)
	algo_macd_2(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN)

	//algo_demo_1(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN)
}

console.log("start algos")

// here we check for and generate signals in an almost real-time fashion

MongoClient.connect(dbCfg.url, dbCfg.settings, async (err, database) => {
	if (err) {
		console.log("ici");
		return console.log(err)
	}
	cryptoDB = database.db('crypto');

	// for each Crypto pair (symbol) write a new job scheduler:
	
	schedule.scheduleJob('*/10 * * * * *', function() {
		var base_cur = 'BTC'
		var quote_cur = 'USDT'
		var exchange = 'binance'
		var intervals = [30,60]
		var historymins = 60*24*30
		var FIRST_RUN = false;

		intervals.forEach(function(interval) {
			work(cryptoDB, base_cur, quote_cur, exchange, interval, historymins, FIRST_RUN)
		});
	});

	schedule.scheduleJob('*/10 * * * * *', function() {
		var base_cur = 'LTC'
		var quote_cur = 'USDT'
		var exchange = 'binance'
		var intervals = [30,60]
		var historymins = 60*24*30
		var FIRST_RUN = false;

		intervals.forEach(function(interval) {
			work(cryptoDB, base_cur, quote_cur, exchange, interval, historymins, FIRST_RUN)
		});
	});

	schedule.scheduleJob('*/10 * * * * *', function() {
		var base_cur = 'ETH'
		var quote_cur = 'USDT'
		var exchange = 'binance'
		var intervals = [30,60]
		var historymins = 60*24*30;
		var FIRST_RUN = false;

		intervals.forEach(function(interval) {
			work(cryptoDB, base_cur, quote_cur, exchange, interval, historymins, FIRST_RUN)
		});
	});

	schedule.scheduleJob('*/10 * * * * *', function() {
		var base_cur = 'BCC' // called also BCH on other exchanges
		var quote_cur = 'USDT'
		var exchange = 'binance'
		var intervals = [30,60]
		var historymins = 60*24*30
		var FIRST_RUN = false;

		intervals.forEach(function(interval) {
			work(cryptoDB, base_cur, quote_cur, exchange, interval, historymins, FIRST_RUN)
		});
	});

	schedule.scheduleJob('*/10 * * * * *', function() {
		var base_cur = 'NEO' 
		var quote_cur = 'USDT'
		var exchange = 'binance'
		var intervals = [30,60]
		var historymins = 60*24*30
		var FIRST_RUN = false; // if true, adjust history mins accordingly

		intervals.forEach(function(interval) {
			work(cryptoDB, base_cur, quote_cur, exchange, interval, historymins, FIRST_RUN)
		});
	});

});

