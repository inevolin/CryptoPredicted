process.env.NTBA_FIX_319 = 1;

module.exports = function() {

    var module = {};

    module.init_telegram_bot_1 = function(params) {
    	const TelegramBot = require('node-telegram-bot-api');
		const token = '523693659:AAH_JjJxbt1hrtrMYui80bLurfwonhnVRHQ';
		const bot = new TelegramBot(token, params);

		return bot;
    }

    return module;
};