

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

    var name = "Macd 2.0";
	var portfolio = {};

	var keys = Object.keys(inp);
	var dtStart = core.parseDateTime_dt(keys[0]);
	var dtEnd = core.parseDateTime_dt(keys[keys.length -1]);
	var dtit = dtStart;

	var uncertainty_margin = 0.001

    var usage= {
        canBuy: true,
        canSell: false,

        buyPrice: null,
        prevPrice: null,

        arrA: [],
        arrB: [],
    }

    function buyF() {
        if (average(usage.arrB.slice(-10)) > usage.arrB[usage.arrB.length-1]) return false;
        if (usage.arrB[usage.arrB.length-2] > usage.arrA[usage.arrA.length-2] && usage.arrB[usage.arrB.length-1] < usage.arrA[usage.arrA.length-1]) return true;
        if (usage.arrB[usage.arrB.length-1] > usage.arrB[usage.arrB.length-2]) return true;
    }
    function sellF() {
        if (price > usage.buyPrice*1.02 && !buyF()) return true;
        if (price < usage.buyPrice*.97) return true;
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

            var pA = EMAsingle(2, usage.arrA.length > 0 ? average(usage.arrA.slice(-5)) : (o+c)/2, (o+c)/2 );
            usage.arrA.push(pA);
            var pB = EMAsingle(15, usage.arrB.length > 0 ? average(usage.arrB.slice(-5)) : (o+c)/2, (o+c)/2 );
            usage.arrB.push(pB);

            if (usage.arrB.length > 2) {
                if (usage.canBuy && buyF()) {
                    core.portfolioBuy(portfolio, dtit, price, uncertainty_margin)
                    usage.canSell = true;
                    usage.canBuy = false;    
                    usage.buyPrice = price;
                } else if (usage.canSell && sellF()) {
                    core.portfolioSell(portfolio, dtit, price, uncertainty_margin)
                    usage.canSell = false;
                    usage.canBuy = true;    
                }
            }
            usage.prevPrice = price;
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


