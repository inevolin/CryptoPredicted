
// payment processing (paypal & stripe)

module.exports = function(app, mailer, payments) {

	function notify(email, email2, affiliate) {
		// notify buyer
		mailer.send_new_payment(email)
		if (email !== email2) {
			mailer.send_new_payment(email2)
		}

		// notify affiliate
		console.log('affiliate: '+affiliate)
		if (affiliate && affiliate['email']!=null) { // check 1
			var coupon = payments.getCouponFromEmail(affiliate['email'])
			console.log(coupon)
			if (coupon !== null) { // check 2 
				var text= "Congratz! You have a new referral. Visit the 'Partners' page on our dashboard for more info."
				mailer.send_custom(affiliate['email'], 'Payment received', text, text)
			}
		}
		
		// notify admin
		var text = "New payment from " + email2 + " ("+email+")"
		mailer.send_to_admin('Payment received', text, text)
		
	}

	app.post('/webhook-stripe', async (req, res) => {
		try {
	    	var wh = JSON.parse(req.body);
	    	var a = await payments.recordMetaData("stripe", "webhook", wh) // we do want to record/log all IPN calls
	    	console.log(wh)

	    	if (wh.data.object.object != "invoice") {
	    		console.log("stripe webhook not of objectType = invoice ; skipping")
	    		res.sendStatus(200);
	    		return res.send("");
	    	}

	    	var email = wh.data.object.lines.data[0].metadata.email
	    	var stripeEmail = wh.data.object.lines.data[0].metadata.stripeEmail
	    	var affiliate = wh.data.object.lines.data[0].metadata.affiliate==null?null:JSON.parse(wh.data.object.lines.data[0].metadata.affiliate)
	    	var chargeID = wh.data.object.charge
	    	var current_period_end = wh.data.object.lines.data[0].period.end *1000 + 1000*60*60*12 // add 12hr margin (the demo will give _end == now(), but live version will have now()+30days)
	    	var amount = Math.round(parseInt(wh.data.object.amount_paid)/100, 2)
	    	var currency = wh.data.object.currency

			var b = await payments.userAddPayment(email, stripeEmail, affiliate, "stripe", chargeID, new Date(), new Date(current_period_end), amount, currency)
			if (b.ok==1)  {
				console.log("new payment (db) added")
				notify(email, stripeEmail, affiliate)
			} else {
				console.log(b)
			}

			

	    	res.sendStatus(200)
    	} catch (err) {
    		console.log(err)
    		res.send("err")
    	}
    });

    app.post('/webhook-paypal', async (req, res) => {
		try {
	    	var wh = req.body;
	    	var a = await payments.recordMetaData("paypal", "webhook", wh) // we do want to record/log all IPN calls
	    	console.log(wh);

	    	if (wh && wh.txn_type && wh.txn_type == "subscr_payment") {
		    	//var meta = JSON.parse(wh.custom)
		    	var meta = await payments.getMetaData({"source":"paypal", "type":"custom", "data.email": wh.custom });
		    	console.log(meta)
		    	var email = meta.data.email
		    	var affiliate = meta.data.affiliate

		    	var email2 = wh.payer_email
		    	var tid = wh.txn_id
		    	var current_period_start = new Date() // add 12hr margin
		    	var current_period_end = new Date(current_period_start.getTime() + 1000*60*60*24*31 + 1000*60*60*12) // add 12hr margin

		    	var amount = parseFloat(wh.mc_gross);
		    	var currency = wh.mc_currency

				var b = await payments.userAddPayment(email, email2, affiliate, "paypal", tid, current_period_start, current_period_end, amount, currency)

				if (b.ok==1)  {
					console.log("new payment (db) added")
					notify(email, email2, affiliate)
				} else {
					console.log(b)
				}
			}

			

	    	res.sendStatus(200)
    	} catch (err) {
    		console.log(err)
    		res.send("err")
    	}
    });    

}
