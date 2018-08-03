

module.exports = async function(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN) {

    function EMAsingle(size, prevPrice, price) {
        if (prevPrice == null) return price;

        var k = (2 / (1+size));
        var v = price * k + prevPrice*(1-k)
        return v;
    }

    function average(data){
        var sum = data.reduce(function(sum, value){
            return sum + value;
        }, 0);

        var avg = sum / data.length;
        return avg;
    }

    var name = "Macd 1.0";
	var portfolio = {};

	var keys = Object.keys(inp);
	var dtStart = core.parseDateTime_dt(keys[0]);
	var dtEnd = core.parseDateTime_dt(keys[keys.length -1]);
	var dtit = dtStart;

	var uncertainty_margin = 0.001

    var buyPrice = null;
    var bucket = [];
    var prevPrice = null;
    var canSell = false, canBuy = true;
    var pA=null, prevA=null;
    var pB=null, prevB=null;
    var pC=null, prevC=null;
    var pCavg=null, prevCavg=null;

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

            pA = EMAsingle(2, prevA, o);
            pB = EMAsingle(15, prevB, c);
            pC = pA-pB
            pC = EMAsingle(3, prevC, pC)
            bucket.push(pC)
            pCavg = average(bucket.slice(-10))

            if (bucket.length > 2) {
                if (canBuy && (prevCavg < 0 && pCavg > 0)) {
                    core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                    canSell = true;
                    canBuy = false;    
                    buyPrice = price;
                } else if (canSell && (price > buyPrice*1.03 || price < buyPrice*.98)) {
                    core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                    canSell = false;
                    canBuy = true;    
                }
            }

            prevPrice = price;
            prevA = pA;
            prevB = pB;
            prevC = pC;
            prevCavg = pCavg;

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


