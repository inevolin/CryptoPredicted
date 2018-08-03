const moment = require('moment');
const querystring = require('querystring');

module.exports = function(cryptoDB) {

	var module = {};

	module.price_regular = 60;
	module.price_discounted = 54;

// test keys:
	module.stripe_keyPublishable = "pk_test_7lZ0YdNArUpUq9zoGGNt7YZh"
	module.stripe_keySecret = "sk_test_n3JgRrCyD6diFOJZGoCwykzO"
// live keys:
   // ... removed due to migration

	module.coupon_affiliate_mapping = {
        "MAY31": {email:null, pct:0.0},
        
    };
    module.getCouponFromEmail = function (email) {
    	for (var coupon in module.coupon_affiliate_mapping) {
    		if (module.coupon_affiliate_mapping[coupon].email == email)
    			return coupon
    	}
    	return null;
    }
    module.getCommissionPctFromEmail = function (email) {
    	for (var coupon in module.coupon_affiliate_mapping) {
    		if (module.coupon_affiliate_mapping[coupon].email == email)
    			return module.coupon_affiliate_mapping[coupon].pct;
    	}
    	return 0;
    }

    module.page_args_not_paid = () => {return {
        need_to_pay : 1,
        keyPublishable: module.stripe_keyPublishable,
        amount: '$'+module.price_regular+'.00'
    }}
    module.page_args_paid_success = () => {return {
        need_to_pay : 0,
        success : 1 
    }}
    module.page_args_paid_premium = () => {return {
        need_to_pay : 0,
    }}
    module.page_args_paid_premium_trial = () => {return {
        need_to_pay : 1,
        keyPublishable: module.stripe_keyPublishable,
        amount: '$'+module.price_regular+'.00'
    }}
    module.page_args_paid_fail = () => {return {
        need_to_pay : 1,
        keyPublishable: module.stripe_keyPublishable,
        amount: '$'+module.price_regular+'.00',
        success : 0
    }}

	module.hasExclusiveAccess = async function(user, next, fail) {
		if (user.type == "affiliate") {
			if (next) return next()
		} else if (user.email == undefined) {
			console.log("undefined user.email : ")
			//console.log(user)
        	if (fail) return fail()
        } else {
        	var obj = await module.findUserLatestPayment(user.email);
        	if (obj && obj.expiry) {
        		if (new Date() < obj.expiry) {
        			console.log("is premium")
        			if (next) return next("premium")
        		}
        	}
        	
        	if (await module.findActiveTrialExpiry(user.email)) {
        		if (next) return next("trial")
        	}
        	
        	console.log("is not premium")
        	if (fail) return fail()
        }
	}
	module.findUserLatestPayment = async function(email) {
		console.log("db: findUserLatestPayment")
		try {
			var query = {email: email}
			var cursor = await cryptoDB.collection('payments').find(query).sort({_id:-1}).limit(1).toArray()
			if (cursor && cursor.length == 1) {
				///console.log(cursor[0])
				return cursor[0]
			}
		} catch (err) { 
			console.log(err)
		}
		return null;
	}

	module.findActiveTrialExpiry = async function(email) {
		var obj = await module.findUserTrialState(email);
    	if (obj && obj.expiry) {
    		if (new Date() < obj.expiry) {
    			console.log("is trial")
    			return obj.expiry;
    		}
    	}
    	return null;
	}

	module.mayActivateTrial = async function(email) {
		// trial only if never had trial, and never had a payment
		var mayActivateTrial = false;
        var findTrial = await module.findUserTrialState(email);
        if (findTrial == null) {
        	var findPayment = await module.findUserLatestPayment(email);
        	if (findPayment == null) {
        		mayActivateTrial = true; // never had a trial record
        	}
            
        }
        return mayActivateTrial;
	}
	module.findUserTrialState = async function(email) {
		console.log("db: isUserTrial")
		try {
			var query = {email: email}
			var cursor = await cryptoDB.collection('trials').find(query).sort({_id:-1}).limit(1).toArray()
			if (cursor && cursor.length == 1) {
				//console.log(cursor[0])
				return cursor[0]
			}
		} catch (err) { 
			console.log(err)
		}
		return null;
	}

	module.findUserPayments = async function(email) {
		try {
			var query = {email: email}
			var cursor = cryptoDB.collection('payments').find(query).sort({'_id':-1});
			var docs = [];
			while(await cursor.hasNext()) {
				const doc = await cursor.next();
				docs.push(doc);
				doc['date_pretty'] = moment(doc.date).format('DD MMM YYYY')
			}
			return {ok:1, docs:docs};
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}

	module.findAffiliateStats = async function(email) {
		try {
			var query = {'affiliate.email': email}
			var cursor = cryptoDB.collection('payments').find(query).sort({'_id':-1});
			var docs = [];
			while(await cursor.hasNext()) {
				const doc = await cursor.next();
				docs.push(doc);
				doc['date_pretty'] = moment(doc.date).format('DD MMM YYYY')
				doc['commission'] = ((doc.amount * doc.affiliate.pct) / 100.0).toFixed(2)
				doc['commission_paid'] = (doc.affiliate.paid ? "yes" : "no")
			}
			return {ok:1, docs:docs};
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}

	module.recordMetaData = async function(source, type, data) {
		try {
			var query = {source: source, type: type, data: data}
			var cursor = await cryptoDB.collection('paymentsMetaData').insert(query);
			return {ok:(cursor.result.ok && cursor.result.n)};
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}

	module.getMetaData = async function(query) {
		console.log("getMetaData:")
		console.log(JSON.stringify(query))
		try {
			var cursor = await cryptoDB.collection('paymentsMetaData').find(query).sort({'_id':-1}).limit(1).toArray();
			if (cursor && cursor.length == 1) {
				///console.log(cursor[0])
				return cursor[0]
			}
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}

	module.userAddPayment = async function(email, email2, affiliate, source, tid, date, expiry, amount, currency) {
		try {
			if (affiliate)
				affiliate['paid'] = false;
			var query = {email: email, email2:email2, affiliate: affiliate, source:source, tid: tid, date:date, expiry: expiry, amount: amount, currency: currency}
			var cursor = await cryptoDB.collection('payments').insert(query);
			return {ok:(cursor.result.ok && cursor.result.n)};
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}

	module.createSubscription_Stripe = async function(email, stripeEmail, stripeToken, coupon) {
		var stripe = require("stripe")(module.stripe_keySecret);

		var customer = await stripe.customers.create({
			email: stripeEmail,
			source: stripeToken
		})
		if (customer)  {
			var a = await module.recordMetaData("stripe", "customer", customer)
			if (a.ok==1) console.log("stripe: new customer added")
			else console.log(a)
		}


		var chargeObj = {
			//ilja's:
			//items: [{plan: 'plan_CrrFPdIaBfN7le'}], // live
			items: [{plan: 'CryptoPredicted_v1'}],  // test

			customer: customer.id,
			metadata: {
				"email": email,
				"stripeEmail": stripeEmail,
				"affiliate": ""
			}
		}
		if (coupon in module.coupon_affiliate_mapping) {// check if coupon exists
			chargeObj['coupon']='cryptopredicted-coupon-v1'; // 10% off lifetime
			chargeObj['metadata']['affiliate'] = JSON.stringify(module.coupon_affiliate_mapping[coupon])
		}

		var subscrip = await stripe.subscriptions.create(chargeObj)
		if (subscrip) {
			var a = await module.recordMetaData("stripe", "subscriptions", subscrip)
			if (a.ok==1) console.log("stripe: new subscription (metadata) added")
			else console.log(a)
		}

		
		// create subscription succeeded (= no exception thrown by stripe)

		return {ok:1}
	
	}

	module.createSubscription_PayPal = async function(res, email, coupon) {
	    var meta = {};
	    meta["email"] = email
	    meta["affiliate"] = (coupon in module.coupon_affiliate_mapping ? module.coupon_affiliate_mapping[coupon] : null)
	    var a = await module.recordMetaData("paypal", "custom", meta)

		query = {};
		query['item_name'] = 'CryptoPredicted Premium';
		query['notify_url'] = 'https://cryptopredicted.com/webhook-paypal';
		//query['image_url'] = 'https://clicktrait.com/ab/images/pp_logo.png';
		query['return'] = 'https://cryptopredicted.com/billing?paypal=1';
		query['business'] = 'pp@nevolin.be';          
		query['currency_code'] = 'USD';            
		query['no_shipping'] = '1';      
		query['custom'] = meta.email;


		query['cmd'] = '_xclick-subscriptions';
		query['a3'] = (coupon in module.coupon_affiliate_mapping ? module.price_discounted : module.price_regular); //price
		query['p3'] = 1; //one month
		query['t3'] = 'M'; //monthly
		query['src'] = 1; //recurring

	    query_string = querystring.stringify(query);           
	    res.redirect('https://www.paypal.com/cgi-bin/webscr?' + query_string); // sandbox testing doesn't work, use a 2nd account

	}

	module.createTrial = async function(res, email) {
	    if (await module.mayActivateTrial(email)) {
			try {
				var expiry = new Date( (new Date()).getTime() + 1000*60*60*24*7);
				var query = {email: email, expiry: expiry}
				var cursor = await cryptoDB.collection('trials').insert(query);
				return {ok:(cursor.result.ok && cursor.result.n)};
			} catch (err) { 
				console.log(err)
				return {ok:0, err:"An unexpected error occurred, please contact support."};
			}
	    } else {
	    	return {ok:0, err:"Not eligible for trial."};
	    }
	}


	return module;
}
