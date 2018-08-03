

module.exports = async function(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN) {

    var name = "Demo 1.0";
	var portfolio = {};

	var keys = Object.keys(inp);
	var dtStart = core.parseDateTime_dt(keys[0]);
	var dtEnd = core.parseDateTime_dt(keys[keys.length -1]);
	var dtit = dtStart;

	var uncertainty_margin = 0.001

    var buyPrice = null;
    var prevPrice = null;
    var canSell = false, canBuy = true;

    function getRandomInt(max) {
        return Math.floor(Math.random() * Math.floor(max));
    }


	while (dtit <= dtEnd) {
		var idx = core.dateTime_ToString(dtit);
		if (idx in inp) {
			var c = inp[idx]['close'];
            var o = inp[idx]['open'];
            var l = inp[idx]['low'];
            var h = inp[idx]['high'];

            var price = c;
            if (FIRST_RUN) price = (o+c)/2;  // when running algo for the first time to generate historical signals

        	core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h);

            if (prevPrice != null) {
                if (getRandomInt(100) <= 50)
                {
                    core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                    canSell = true;
                    canBuy = false;    
                    buyPrice = price;
                } else
                {
                    core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                    canSell = false;
                    canBuy = true;    
                }
            }

            prevPrice = price;

		}
		//console.log(dtit)
		dtit = dtit.add(interval, 'minutes');
	}
	// var proc = core.processPortfolio(portfolio, 0.001, 1, 1);
	
    //console.log(name + " " + base_cur + " " + quote_cur)
    if (FIRST_RUN)
        core.processSignals_all(cryptoDB, portfolio, interval, base_cur, quote_cur, exchange, name);  // when running algo for the first time to generate historical signals
    else
        core.processSignals(cryptoDB, portfolio, interval, base_cur, quote_cur, exchange, name);
}


