
// compute ROI (displayed on the trade signals page)
// the ROI as of now is for the past 60 days

const MongoClient   = require('mongodb').MongoClient;
const dbCfg         = require('../db.js');
const schedule 		= require('node-schedule');

console.log("start ROIs")

MongoClient.connect(dbCfg.url, dbCfg.settings, async (err, database) => {
	if (err) {
		console.log("ici");
		return console.log(err)
	}
	cryptoDB = database.db('crypto');
	const core = require('./core.js')(cryptoDB);


	// for each new crypto pair (symbol) write a new job scheduler:

	schedule.scheduleJob('0 * * * * *', function() {

		var base_cur = 'BTC'
		var quote_cur = 'USDT'
		var exchange = 'binance'

		var currentDatetime = new Date();

		var intervals = [30,60]
		var historymins = 60*24*60 // 30-day ROI

		intervals.forEach(function(interval) {
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.1")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Voltra 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 2.0")
			
			//work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Demo 1.0")
		});
	});

	schedule.scheduleJob('0 * * * * *', function() {

		var base_cur = 'LTC'
		var quote_cur = 'USDT'
		var exchange = 'binance'

		var currentDatetime = new Date();

		var intervals = [30,60]
		var historymins = 60*24*60 // 30-day ROI

		intervals.forEach(function(interval) {
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.1")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Voltra 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 2.0")
			
			//work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Demo 1.0")
		});
	});

	schedule.scheduleJob('0 * * * * *', function() {

		var base_cur = 'ETH'
		var quote_cur = 'USDT'
		var exchange = 'binance'

		var currentDatetime = new Date();

		var intervals = [30,60]
		var historymins = 60*24*60 // 30-day ROI

		intervals.forEach(function(interval) {
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.1")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Voltra 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 2.0")
			
			//work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Demo 1.0")
		});

	});

	schedule.scheduleJob('0 * * * * *', function() {

		var base_cur = 'BCC' // called also BCH on other exchanges
		var quote_cur = 'USDT'
		var exchange = 'binance'

		var currentDatetime = new Date();

		var intervals = [30,60]
		var historymins = 60*24*60 // 30-day ROI

		intervals.forEach(function(interval) {
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.1")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Voltra 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 2.0")
			
			//work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Demo 1.0")
		});

	});


	schedule.scheduleJob('0 * * * * *', function() {

		var base_cur = 'NEO'
		var quote_cur = 'USDT'
		var exchange = 'binance'

		var currentDatetime = new Date();

		var intervals = [30,60]
		var historymins = 60*24*60 // 30-day ROI

		intervals.forEach(function(interval) {
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Pistis 1.1")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Voltra 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 1.0")
			work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Macd 2.0")
			
			//work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, "Demo 1.0")
		});

	});
	
});



async function work(core, cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, algoName) {
	try {
		var docs = await core.obtain_price_with_signals(cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, algoName);
		
		// assign buy & sell signals into portfolio:
		var portfolio = {};
		for (var dt in docs) {
			var price = docs[dt].close; // if the last entry is a buy, sell using its closing price
			core.portfolioPriceEntry(portfolio, dt, price, docs[dt].open, docs[dt].close, docs[dt].low, docs[dt].high)
			if ('signal' in docs[dt]) {
				if (docs[dt].signal.type == 'buy') {
					core.portfolioBuy(portfolio, dt, docs[dt].signal.price, 0.001)
				} else if (docs[dt].signal.type == 'sell') {
					core.portfolioSell(portfolio, dt, docs[dt].signal.price, 0.001)
				}
			}
		}
		// make a deep copy:
		var portfolio2 = JSON.parse(JSON.stringify(portfolio));
		
		// compute ROI of portfolio:
		var proc =  core.processPortfolio(portfolio, 0.001, 1, 1);
		console.log(algoName + " " + base_cur + "" + quote_cur + "  " + interval + "\t" + proc.ROI);

		var query = {
			interval: interval,
			historymins: historymins,
			base_cur: base_cur,
			quote_cur: quote_cur,
			exchange: exchange,
			name: algoName,
		}
		//console.log(query)
		var setter = {
			proc: proc,
			portfolio:portfolio2,
		}
		await cryptoDB.collection('algo_portfolios').update(query, {'$set': setter}, {upsert: true});
	}
	catch (ex) {
		console.log(ex)
	}
}