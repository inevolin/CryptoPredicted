
const moment        = require('moment');
const mailer         = require('../mail')();
const process_algo_subbed_users = require('../api/process_algo_subbed_users.js');
const process_algo_findLastSignal = require('../api/process_algo_findLastSignal.js');

module.exports = function(cryptoDB) {
    const payments = require('../payments.js')(cryptoDB);
    const auth = require('../auth.js')(cryptoDB, mailer);
    const notifiers = require('../notifiers/index.js')(cryptoDB);

    var module = {};

    module.obtain_price = async function(cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime) {
        var process_exchange = require('../api/process_exchange.js')
        var docs_price = {};
        await process_exchange(cryptoDB,
            docs_price,
            interval,
            historymins,
            base_cur,
            quote_cur,
            exchange,
            currentDatetime
        )
        return docs_price;
    }

    module.obtain_price_with_signals = async function(cryptoDB, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, algoName) {
        var process_algo_signals = require('../api/process_algo_signals.js')
        var docs_price = {};
        await process_algo_signals(cryptoDB,
            docs_price,
            interval,
            historymins,
            base_cur,
            quote_cur,
            exchange,
            currentDatetime,
            algoName
        )
        return docs_price;
    }

    module.parseDateTime_dt = function(str, format) {
        if (typeof format == "undefined" || format == null) {
            format="YYYY-MM-DDTHH:mm";
        }
        return moment.utc(str, format); 
    }

    module.parseDateTime_string = function(str, format) {
        if (typeof format == "undefined" || format == null) {
            format="YYYY-MM-DDTHH:mm";
        }
        return parseDateTime_dt(str).format(format);
    }

    module.dateTime_ToString = function(dt, format) {
        if (typeof format == "undefined" || format == null) {
            format="YYYY-MM-DDTHH:mm";
        }
        return moment(dt).format(format)
    }

    module.processPortfolio = function(portfolio, fee, buyRate, sellRate) {

        var cashStart = 10000;
        var cash = cashStart;
        var crypto = 0;

        var buys = 0;
        var sells = 0;

        var ignore_last_key = null;
        var keys = Object.keys(portfolio).reverse();
        for (var i in keys) {
            var dt = keys[i];
            if ('buy' in portfolio[dt]) {
                //delete portfolio[dt].buy
                ignore_last_key = dt;
            } else if ('sell' in portfolio[dt]) {
                break;
            }
        }

        Object.keys(portfolio).forEach(function (idx) {
            var obj = portfolio[idx];
            if (ignore_last_key != null && idx == ignore_last_key) return;
            if ('buy' in obj) {
                if (cash > 0) {
                    crypto_x = cash * buyRate / obj.buy.buyprice;
                    crypto += crypto_x * (1-fee);
                    cash -= cash * buyRate;
                    buys++;
                }

            } else if ('sell' in obj) {
                if (crypto > 0) {
                    cash_x = crypto * sellRate * obj.sell.sellprice;
                    cash += cash_x * (1-fee);
                    crypto -= crypto * sellRate;
                    sells++;
                }
            }
        });
        
        if (crypto > 0) { // sell what's left using last available price
            //console.log("!!!!!! crypto not empty")
            //console.log(crypto)
            var i = Object.keys(portfolio).slice(-1)[0];
            var obj = portfolio[i];
            cash_x = crypto * 1 * obj.price
            cash += cash_x * (1-fee)
            crypto -= crypto * 1
        }

        return {
            'cash': cash,
            'crypto': crypto,
            'ROI': (cash - cashStart)/cash * 100,
            'buys': buys,
            'sells': sells
        }
    }


    module.average = function(arr) {
        var sum = 0;
        if (arr.length == 0) return sum;

        for (var i in arr) {
            if (!isNaN(arr[i])) {
                sum += arr[i]
            }
        }
        return sum/arr.length;
    }



    module.portfolioPriceEntry = function(portfolio, dtit, price, open, close, low, high) {
        var dtit_s = module.dateTime_ToString(dtit)
        if (!(dtit_s in portfolio))
            portfolio[dtit_s] = {};

        portfolio[dtit_s]["price"]= price // ap = actual price
        portfolio[dtit_s]["open"]= open
        portfolio[dtit_s]["close"]= close
        portfolio[dtit_s]["low"]= low
        portfolio[dtit_s]["high"]= high
    }

    module.portfolioBuy = function(portfolio, dtit, buyprice, uncertainty_margin) {
        var dtit_s = module.dateTime_ToString(dtit)
        portfolio[dtit_s]['buy'] = {
            'buyprice_default':buyprice,
            'buyprice':buyprice*(1+uncertainty_margin)
        }
    }

    module.portfolioSell = function(portfolio, dtit, sellprice, uncertainty_margin) {
        var dtit_s = module.dateTime_ToString(dtit)
        portfolio[dtit_s]['sell'] = {
            'sellprice_default':sellprice,
            'sellprice':sellprice*(1-uncertainty_margin)
        }
    }


    module.processSignals = async function (cryptoDB, portfolio, interval, base_cur, quote_cur, exchange, name) {
        // take the last item from portfolio (~ realtime), if it has buy/sell signal then process it.

        // db.algo_signals.createIndex( { interval: 1, ts_interval: 1, base_cur: 1, quote_cur: 1, exchange: 1, name: 1}, { unique: true } )
        // right now the unique index is removed; this way we allow all signals to be saved, not only one per interval

        try {
            var keys = Object.keys(portfolio);
            var lastKey = keys[keys.length-1];
            var lastEntry = portfolio[lastKey];

            if (lastEntry && 'buy' in lastEntry) {
                //console.log('buy in entry')
                var type = 'buy';
                var ts = module.parseDateTime_dt(lastKey);
                var price = lastEntry.buy.buyprice_default;

                process(type, ts, price);
            }
            else if (lastEntry && 'sell' in lastEntry) {
                //console.log('sell in entry')
                var type = 'sell';
                var ts = module.parseDateTime_dt(lastKey);
                var price = lastEntry.sell.sellprice_default;

                process(type, ts, price);
            }

            async function process(type, ts, price) {
                try {
                    var query = {
                        interval: interval,
                        base_cur: base_cur,
                        quote_cur: quote_cur,
                        exchange: exchange,
                        name: name,
                        ts_interval: ts.toDate(), // datetime rounded given the interval:    [A, B[

                        signal: {
                            type:type,
                            ts: new Date(), // signal was detected & generated right now:        [A, now, B[
                            price:price},
                    }
                    // first check if signal is same as previous one; then insert current signal
                    // otherwise we would check against current signal and email would never be sent
                    if (!(await isSameTypeSignal(cryptoDB, interval, base_cur, quote_cur, exchange, name))) {
                        await cryptoDB.collection('algo_signals').insert(query);
                        doNotify(cryptoDB, name, base_cur, quote_cur, interval, exchange, type);
                    }
                } catch(ex) {
                    //console.log("dup")
                    if (name.includes('Demo')) {
                    //if (!(await isSameTypeSignal(cryptoDB, interval, base_cur, quote_cur, exchange, name)))
                    {
                    //doNotify(cryptoDB, name, base_cur, quote_cur, interval, exchange, type); // remove in production
                    }
                    }
                }
            }

            async function isSameTypeSignal(cryptoDB, interval, base_cur, quote_cur, exchange, name) {
                // previous signal could of the same type ; in that case check what the previous signal's type was ...
                var docs = [];
                await process_algo_findLastSignal(cryptoDB, docs, interval, base_cur, quote_cur, exchange, name);
                if (docs.length == 1) {
                    var doc = docs[0];
                    //console.log(doc)
                    //console.log("type now: " + type)
                    if (doc.signal.type == type) {
                        //console.log("identical signal type detected")
                        return true; // don't notify of same consecutive types
                    }
                }
                return false;
            }

            async function doNotify(cryptoDB, name, base_cur, quote_cur, interval, exchange, type) {
                
                var title= type + ": " + name + " ("+base_cur+"-"+quote_cur+") " + "["+interval+"m]";
                var body = "Algo " + name + " indicated a '"+type+"' signal "+ " ("+base_cur+"-"+quote_cur+") "  + "["+interval+"m]";
                console.log(title)

                try {
                    doNotify_email(cryptoDB, name, base_cur, quote_cur, interval, exchange, type, title, body)
                } catch (err) {console.log(err)}
                try {
                    doNotify_telegram(cryptoDB, name, base_cur, quote_cur, interval, exchange, type, title, body)
                } catch (err) {console.log(err)}
            }

            async function doNotify_email(cryptoDB, name, base_cur, quote_cur, interval, exchange, type, title, body) {
                console.log("doNotify: email -- " + name)
                // find all users subbed to this specific algo: 
                var subs = [];
                await process_algo_subbed_users(cryptoDB, subs, {name:name, base_cur:base_cur, quote_cur:quote_cur, interval:interval, exchange:exchange, type_sub: 'email'});
                for (var i = 0; i < subs.length; i++) {
                    try {
                        var email = subs[i].email;
                        if (await canNotifyUser(email)) {
                            console.log("sending signal to: " + email)
                            mailer.send_trade_signal(email, title, body); // send mail
                        }
                    } catch (err) {
                        console.log(err)
                    }
                }
            }

            async function doNotify_telegram(cryptoDB, name, base_cur, quote_cur, interval, exchange, type, title, body) {
                console.log("doNotify: telegram -- " + name)
                // find all users subbed to this specific algo: 
                var subs = [];
                await process_algo_subbed_users(cryptoDB, subs, {name:name, base_cur:base_cur, quote_cur:quote_cur, interval:interval, exchange:exchange, type_sub: 'telegram'});
                for (var i = 0; i < subs.length; i++) {
                    try {
                        var email = subs[i].email;
                        if (await canNotifyUser(email)) {
                            notifiers.telegram_bot_sendMessage(email, body);
                        }
                    } catch (err) {
                        console.log(err)
                    }
                }
            }


            async function canNotifyUser(email) {
                var user = await auth.findUser(email);
                if (!user) {
                    console.log("core: " + email + " user not found");
                    return false;
                }
                else if (!auth.isEmailVerified(user)) {
                    console.log("core: " + email + " not verified");
                    return false;   
                }
                return await payments.hasExclusiveAccess(user, function() {
                    console.log("core: " + email + " ok!");
                    return true;
                }, function() {
                    console.log("core: " + email + " has no exclusive access");
                    return false;
                });

            }
            
        } catch (ex) {
            console.log(ex)
        }
    };

    



    module.processSignals_all = async function (cryptoDB, portfolio, interval, base_cur, quote_cur, exchange, name) {
        // if we have a new algo, we'd like to add many signals to it (let's take price=random[O,C])

        // db.algo_signals.createIndex( { interval: 1, ts_interval: 1, base_cur: 1, quote_cur: 1, exchange: 1, name: 1}, { unique: true } )
        // right now the unique index is removed; this way we allow all signals to be saved, not only one per interval

        try {
            var keys = Object.keys(portfolio);
            for (var i in keys) {
                var lastKey = keys[i];
                var lastEntry = portfolio[lastKey];

                if (lastEntry && 'buy' in lastEntry) {
                    //console.log('buy in entry')
                    var type = 'buy';
                    var ts = module.parseDateTime_dt(lastKey);
                    var price = lastEntry.buy.buyprice_default;

                    process(type, ts, price);
                }
                else if (lastEntry && 'sell' in lastEntry) {
                    //console.log('sell in entry')
                    var type = 'sell';
                    var ts = module.parseDateTime_dt(lastKey);
                    var price = lastEntry.sell.sellprice_default;

                    process(type, ts, price);
                }

                async function process(type, ts, price) {
                    try {
                        var query = {
                            interval: interval,
                            base_cur: base_cur,
                            quote_cur: quote_cur,
                            exchange: exchange,
                            name: name,
                            ts_interval: ts.toDate(), // datetime rounded given the interval:    [A, B[

                            signal: {
                                type:type,
                                ts: new Date(), // signal was detected & generated right now:        [A, now, B[
                                price:price},
                        }
                       // console.log(query)
                        await cryptoDB.collection('algo_signals').insert(query);
                        // push notif if no exception ... (if unique index exists that is) -- otherwise use a different strategy
                    } catch(ex) {
                        //console.log("dup")
                    }
                }
            }
            
        } catch (ex) {
            console.log(ex)
        }
    }





    return module;
}