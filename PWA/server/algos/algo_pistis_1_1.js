

module.exports = async function(cryptoDB, inp, core, interval, historymins, base_cur, quote_cur, exchange, currentDatetime, FIRST_RUN) {

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

    function EMAsingle(size, prevPrice, price) {
        if (prevPrice == null) return price;

        var k = (2 / (1+size));
        var v = price * k + prevPrice*(1-k)
        return v;
    }
    

    var name = "Pistis 1.1";
	var portfolio = {};


	var keys = Object.keys(inp);
	var dtStart = core.parseDateTime_dt(keys[0]);
	var dtEnd = core.parseDateTime_dt(keys[keys.length -1]);
	var dtit = dtStart;

	var uncertainty_margin = 0.001

    var arrA = [];
    var arrC = [];
    var arrL = 35;
    var arrEL = 4;
    var pA=null, prevA=null;
    var pC=null, prevC=null;

    var canSell = false, canBuy = true;

	while (dtit <= dtEnd) {
		var idx = core.dateTime_ToString(dtit);
		if (idx in inp) {
			var c = inp[idx]['close'];
            var o = inp[idx]['open'];
            var l = inp[idx]['low'];
            var h = inp[idx]['high'];

            var price = c;
            if (FIRST_RUN) price = (o+c)/2;  // when running algo for the first time to generate historical signals

            arrA.push(price);
            var avg = average(arrA.slice(-arrL))
            var std = standardDeviation(arrA.slice(-arrL))
            pA = avg + std
            pA = EMAsingle(arrEL, prevA, pA)
            prevA = pA

            arrC.push(price)
            avg = average(arrC.slice(-arrL))
            std = standardDeviation(arrC.slice(-arrL))
            pC = avg - std
            pC = EMAsingle(arrEL, prevC, pC)
            prevC = pC

        	core.portfolioPriceEntry(portfolio, dtit, price, o, c, l, h);
            if (canBuy && (pC >= o && pC <= c)) {
                core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                canSell = true;
                canBuy = false;    
            } else if (canSell && (pA >= c && pA <= o)) {
                core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                canSell = false;
                canBuy = true;    
            }

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


