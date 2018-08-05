
// telegram bot related functions and used on trade signals page (for enabled/disabling telegram notifications for specific strategies)

module.exports = function(cryptoDB) {

    var module = {};

    const request = require('request');

    const process_telegram_chatId = require('../api/process_telegram_chatId.js');
    const telegram_bot_funcs = require('../notifiers/functions.js')();
    const telegram_bot = telegram_bot_funcs.init_telegram_bot_1({});

    module.algoParamsToTopicName = function(name, base_cur, quote_cur, interval, exchange) {
        return (name + "_" + base_cur + "_" + quote_cur + "_" + interval + "_" + exchange).replace(' ', '_');
    }

    module.subUserToAlgo = async function(user, name, base_cur, quote_cur, interval, exchange, type_sub) {
        try {
            var query = {
                email: user.email,
                name: name,
                base_cur: base_cur,
                quote_cur: quote_cur,
                interval: interval,
                exchange: exchange,
                type_sub: type_sub,
            }
            var cursor = await cryptoDB.collection('algoSubs').update(query, query, {upsert:true});
            return ({ok:(cursor.result.ok && cursor.result.n)});
        } catch (err) {
            console.log(err)
            return ({ok:0});
        }
    }
    module.unsubUserFromAlgo = async function(user, name, base_cur, quote_cur, interval, exchange, type_sub) {
        try {
            var query = {
                email: user.email,
                name: name,
                base_cur: base_cur,
                quote_cur: quote_cur,
                interval: interval,
                exchange: exchange,
                type_sub: type_sub,
            }
            console.log(query)
            var cursor = await cryptoDB.collection('algoSubs').remove(query);
            return ({ok:1});
        } catch (err) {
            console.log(err)
            return ({ok:0});
        }
    }

    module.telegram_bot_sendMessage = async function(email, message) {
        var chatId = (await process_telegram_chatId(cryptoDB, email));
        if (chatId != null) {
            try {
                console.log("sending TELEGRAM message to: " + email)
                telegram_bot.sendMessage(chatId, message);
            } catch (err) {
                console.log(err)
            }
            return 1;
        } else {
            console.log('missing chatId for user: ' + email)
        }
        return 0;
    }

    return module;
};