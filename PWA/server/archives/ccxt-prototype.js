

/*
	Using the CCXT open-source project for scraping exchanges
	for more info: https://github.com/ccxt/ccxt/
*/

'use strict';
const ccxt = require ('ccxt');

const MongoClient   = require('mongodb').MongoClient;
const dbCfg         = require('../../../db.js'); // change this to correct path !!!!!!
const schedule 		= require('node-schedule');


MongoClient.connect(dbCfg.url, dbCfg.settings,  async(err, database) => {
	if (err) {
		return console.log(err)
	}
	var cryptoDB = database.db('crypto');



	let coinbasepro = new ccxt.coinbasepro();
	let binance = new ccxt.binance();
	let bitstamp = new ccxt.bitstamp();
	
	let bitfinex = new ccxt.bitfinex2();
	let poloniex = new ccxt.poloniex();
	let bitmex = new ccxt.bitmex();   ////// err
	let kraken = new ccxt.kraken();
	let huobipro = new ccxt.huobipro();

	pull_binance(binance, cryptoDB)
	pull_coinbasepro(coinbasepro, cryptoDB)
	pull_bitfinex(bitfinex, cryptoDB)
	pull_poloniex(poloniex, cryptoDB)
	pull_kraken(kraken, cryptoDB)
	pull_huobipro(huobipro, cryptoDB)

	// pull_bitmex(bitmex, cryptoDB) ////// err
	// pull_bitstamp(bitstamp, cryptoDB) // gives us one hour or one day of data (no history)
	// pull_bittrex(bittrex, cryptoDB) (only about 100 results, not enough)
	

/*	var m = await huobi.load_markets()
	//console.log(m)
	for(var x in m) {
		console.log(x+"\t\t\t"+m[x]['base'] + "/" + m[x]['quote'])
	}*/

	/*Promise.all(promises).then(values => {
		database.close()
	});*/

});


// USD
async function pull_coinbasepro(coinbasepro, cryptoDB) {
	var bases = ['BTC', 'ETH', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(coinbasepro, 	'coinbasepro', 	base,	'USD', '1d', cryptoDB)
		}, 1000*i, base);
	}
}
/*async function pull_bitstamp(bitstamp, cryptoDB) {
	var bases = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(bitstamp, 	'bitstamp', 	base,	'USD', '1d', cryptoDB) // this returns only one candlestick value
		}, 1000*i, base);
	}
}*/
/*async function pull_bitmex(bitmex, cryptoDB) {
	//and it has a problem with timestamps (showing 2015/2016)
	var bases = ['BTC', ] // has only BTC/USD available through API
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(bitmex, 	'bitmex', 	base,	'USD', '1d', cryptoDB) 
		}, 1000*i, base);
	}
}*/
async function pull_kraken(kraken, cryptoDB) {
	var bases = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(kraken, 	'kraken', 	base,	'USD', '1d', cryptoDB) 
		}, 1000*i, base);
	}
}

// USDT
async function pull_binance(binance, cryptoDB) {
	var bases = ['BTC', 'ETH', 'LTC', 'BCH', 'EOS', 'ADA', 'TRX', 'XLM', 'NEO', 'BNB', 'XRP', 'ETC', 'VEN', 'ICX', 'ONT', 'IOTA', 'TUSD', 'QTUM']
	//var bases = ['ADA']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(binance, 	'binance', 	base,	'USDT', '1d', cryptoDB)
		}, 1000*i, base);
	}
}
/*async function pull_bittrex(bittrex, cryptoDB) {
	var bases = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(bittrex, 	'bittrex', 	base,	'USDT', '1d', cryptoDB)
		}, 1000*i, base);
	}
}*/
async function pull_bitfinex(bitfinex, cryptoDB) {
	var bases = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(bitfinex, 	'bitfinex', 	base,	'USDT', '1d', cryptoDB) 
		}, 1000*i, base);
	}
}
async function pull_poloniex(poloniex, cryptoDB) {
	var bases = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(poloniex, 	'poloniex', 	base,	'USDT', '1d', cryptoDB) 
		}, 1000*i, base);
	}
}
async function pull_huobipro(huobipro, cryptoDB) {
	var bases = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']
	for (var i = 0; i < bases.length; i++) {
		var base = bases[i];
		setTimeout(async function(base) {
			getter(huobipro, 	'huobipro', 	base,	'USDT', '1d', cryptoDB) 
		}, 1000*i, base);
	}
}

////////////////////////////////////

async function getter(exchange, exchangename, base, quote, resolution, cryptoDB) {
	if (exchange.has.fetchOHLCV) {
    	try {
    		var start = Date.parse("2018-05-01T00:00:00");
    		var data = await exchange.fetchOHLCV (base+'/'+quote, resolution, start, 300);
	    	// console.log (data)
	    	/*for (var j = 0; j < data.length; j++) {
	    		var d = data[j];
	    		upserter(cryptoDB, exchangename, base, quote, resolution, new Date(d[0]), d[1],d[2],d[3],d[4], d[5])
	    	}*/
	    	if (data.length > 0) {

	    		upserterBatch(cryptoDB, exchangename, base, quote, resolution, data)
	    		console.log(exchangename+' '+base+'/'+quote+': done')

	    	}
	    	

	    } catch(err) {
	    	console.log(err)
	    }
	}
}

async function upserter(cryptoDB, exchange, base, quote, resolution, timestamp, open, high, low, close, volume) {
	try {
		var query = {
			timestamp: timestamp,
			base: base,
			quote: quote,
			exchange: exchange,
			resolution: resolution,
		}
		var setter = {
			open: open,
			high: high,
			low: low,
			close: close,
			volume: volume,
		}
		cryptoDB.collection('tai').update(query, {'$set': setter}, {upsert: true});
	} catch(err) {console.log(err)}
}


async function upserterBatch(cryptoDB, exchange, base, quote, resolution, data) {
	try {
		var bulk = await cryptoDB.collection('tai').initializeUnorderedBulkOp();
		for (var j = 0; j < data.length; j++) {
    		var d = data[j];
    		var timestamp = new Date(d[0]);
    		var open = d[1];
    		var high = d[2];
    		var low = d[3];
    		var close = d[4];
    		var volume = d[5];
			var query = {
				timestamp: timestamp,
				base: base,
				quote: quote,
				exchange: exchange,
				resolution: resolution,
			}
			var setter = {
				open: open,
				high: high,
				low: low,
				close: close,
				volume: volume,
			}
    		await bulk.find(query).upsert().update({'$set': setter});
    	}
		
		await bulk.execute();
		

		
		
		//cryptoDB.collection('tai').update(query, {'$set': setter}, {upsert: true});
	} catch(err) {console.log(err)}
}
