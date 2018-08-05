

// dashboard front-end logic


const moment = require('moment');

module.exports = function(app, auth, root_node, payments, notifiers) {

    var proceed_conditional_premium = async function (req, res, ejs, isPremium, args) {
        if (!args) args = {}
        args['premiumStatus'] = isPremium ? "PREMIUM" : "Account limited.";
        res.render(ejs, args, function(err, html) {
            if (err) {
                console.log(err)
                app.render500(req,res)
            }
            res.send(html)
        }); 
    }


    app.get('/predictions', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            payments.hasExclusiveAccess(user, function() {
                proceed_conditional_premium(req,res, 'pages2/predictions.ejs', true, {root_node})
            }, function() {
                res.redirect(root_node+"billing")
            })
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

    app.get('/dashboard', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            payments.hasExclusiveAccess(user, function() {
                proceed_conditional_premium(req,res, 'pages2/dashboard.ejs', true, {root_node})
            }, function() {
                res.redirect(root_node+"billing")
                //proceed_conditional_premium(req,res, 'pages2/dashboard.ejs', false, {root_node})
            })
            
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

    app.get('/notifications', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            payments.hasExclusiveAccess(user, function() {
                var telegram_command = '/enable_signals '+user.email+':'+user._id;
                proceed_conditional_premium(req,res, 'pages2/notifications.ejs', true, {root_node, telegram_command})
            }, function() {
                res.redirect(root_node+"billing")
            })
            
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });



    app.post('/test/telegram/setup/', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                res.status(413);
                return res.send("email not verified");
            }
            payments.hasExclusiveAccess(user, async function() {
                var out = await notifiers.telegram_bot_sendMessage(user.email, "testing success!");
                if (out == 1) {
                    res.send("ok");
                } else {
                    res.send("something went wrong.");
                }
            }, function() {
                res.status(413);
                return res.send("premium membership required");
            })
            
        }, async function() {
            auth.desessionize(res);
            res.status(413);
            return res.send("whoops...");
        })
    });
    
    app.get('/check-coupon', async (req, res) => { // used by AJAX to verify coupon on checkout
        auth.authenticate(req.cookies.sessionID, async function() {
            var coupon = req.query.coupon;
            if (coupon && coupon.length > 0) {
                if (coupon in payments.coupon_affiliate_mapping) {
                    // var affiliate = payments.coupon_affiliate_mapping[coupon];
                    return res.send("$"+payments.price_discounted+".00");
                }
            }
            return res.send("0");
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

    app.get('/check-premium', async (req, res) => { // used by AJAX after payment
        auth.authenticate(req.cookies.sessionID, async function(user) {
            await payments.hasExclusiveAccess(user, function() {
                res.send("1")
            }, function() {
                res.send("0")
            })
            
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

    app.get('/billing', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            var args = {};
            var isPremium = false;
            await payments.hasExclusiveAccess(user, async function() {
                isPremium = true;
                args['findActiveTrialExpiry'] = await payments.findActiveTrialExpiry(user.email);
                if (args['findActiveTrialExpiry'])
                    args = Object.assign(args, payments.page_args_paid_premium_trial());
                else
                    args = Object.assign(args, payments.page_args_paid_premium());
            }, function() {
                if (req.query && (req.query.paypal || req.query.auth))
                    args = payments.page_args_paid_success() // paid (paypal) ; returns GET request, so we use "?paypal=1" query param
                else
                    args = payments.page_args_not_paid(); // user didn't pay yet
            })
            args['mayActivateTrial'] = await payments.mayActivateTrial(user.email);
            args['moment'] = moment;

            var p = await payments.findUserPayments(user.email)
            if (p && p.ok == 1 && !args['mayActivateTrial'] && p.docs.length > 0) args['payments'] = p.docs

            proceed_conditional_premium(req,res, 'pages2/billing.ejs', isPremium, args)

        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

	app.post('/billing', async (req, res) => {
    	auth.authenticate(req.cookies.sessionID, async function(user) {
    		if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
    		try {

                if (!req.body || !req.body.payment) throw Error("Missing payment type #DP63")
                if (req.body.payment == "stripe") {
                    var email = user.email;
    	    		var stripeEmail = req.body.stripeEmail;
    	    		var stripeToken = req.body.stripeToken;
                    var coupon = req.body.coupon;

    	        	var a = await payments.createSubscription_Stripe(email, stripeEmail, stripeToken, coupon);
    	        	
                    var args = payments.page_args_paid_success(); // paid (stripe)
                    args['mayActivateTrial'] = false;
                    args['moment'] = moment;

                    var p = await payments.findUserPayments(user.email)

                    if (p && p.ok == 1 && !args['mayActivateTrial'] && p.docs.length > 0) args['payments'] = p.docs

                    payments.hasExclusiveAccess(user, async function() {
                        args['findActiveTrialExpiry'] = await payments.findActiveTrialExpiry(user.email);
                        proceed_conditional_premium(req,res, 'pages2/billing.ejs', true, args)
                    }, function() {
                        proceed_conditional_premium(req,res, 'pages2/billing.ejs', false, args)
                    })
                } else if (req.body.payment == "paypal") {
                    var coupon = req.body.coupon;
                    var a = await payments.createSubscription_PayPal(res, user.email, coupon);
                } else if (req.body.payment == "trial") {
                    var a = await payments.createTrial(res, user.email);
                    if (a.ok == 0) {
                        var args = payments.page_args_paid_fail();
                        args['mayActivateTrial'] = false;
                        args['moment'] = moment;

                        var p = await payments.findUserPayments(user.email)
                        if (p && p.ok == 1 && !args['mayActivateTrial'] && p.docs.length > 0) args['payments'] = p.docs;
                        
                        payments.hasExclusiveAccess(user, async function() {
                            args['findActiveTrialExpiry'] = await payments.findActiveTrialExpiry(user.email);
                            proceed_conditional_premium(req,res, 'pages2/billing.ejs', true, args)
                        }, function() {
                            proceed_conditional_premium(req,res, 'pages2/billing.ejs', false, args)
                        })
                    }
                    else {
                        // var args = payments.page_args_paid_premium();
                        res.redirect(root_node+'dashboard')
                    }

                    
                } else {
                     throw Error("Missing payment type #DP88")
                }
        	} catch (err) {

        		var args = {};
                var isPremium = false;
                if (err && err.code == "token_already_used") {
                    return res.redirect(root_node+'billing')
                } else {
                    args = payments.page_args_paid_fail(); // something went wrong
                    args['mayActivateTrial'] = await payments.mayActivateTrial(user.email);
                    args['findActiveTrialExpiry'] = await payments.findActiveTrialExpiry(user.email);
                    args['moment'] = moment;

                    console.log(err);
                    var p = await payments.findUserPayments(user.email)
                    if (p && p.ok == 1 && !args['mayActivateTrial'] && p.docs.length > 0) args['payments'] = p.docs;
                    proceed_conditional_premium(req,res, 'pages2/billing.ejs', isPremium, args)
                }
        	}
			
	    }, async function() {
            auth.desessionize(res);
    	    res.redirect(root_node+'login')
	    })
	});


    app.get('/partner', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            payments.hasExclusiveAccess(user, async function() {
                var args = {};
                if (user.type && user.type == "affiliate") {
                    args['isPartner'] = 1;
                    args['coupon'] = payments.getCouponFromEmail(user.email)
                    args['commission'] = payments.getCommissionPctFromEmail(user.email)
                    var a = await payments.findAffiliateStats(user.email)
                    if (a && a.ok && a.ok == 1)
                        args['stats'] = a.docs
                }
                proceed_conditional_premium(req,res, 'pages2/partner.ejs', true, args)
            }, async function() {
                proceed_conditional_premium(req,res, 'pages2/partner.ejs', false, {})
            })
            
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });



    app.post('/signals/:action/:type', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            console.log(req.params['type'])
            if ( ['email', 'telegram'].indexOf(req.params['type']) == -1 ) {
                res.send({ok:0, err:"invalid type parameter"});
                return;
            }
            payments.hasExclusiveAccess(user, async function() {
                var body = JSON.parse(req.body);
                if (req.params['action'] == 'sub') {
                    var out = await notifiers.subUserToAlgo(user, body.name, body.base_cur, body.quote_cur, body.interval, body.exchange, req.params['type']);
                    res.send(out);
                } else if (req.params['action'] == 'unsub') {
                    // first remove from FCM, then from DB
                    var out = await notifiers.unsubUserFromAlgo(user, body.name, body.base_cur, body.quote_cur, body.interval, body.exchange, req.params['type']);
                    res.send(out);
                } 
            }, async function() {
                console.log("user without exclusive access trying to update fcm token unsuccessfully.");
                res.send({ok:0, err:"fail exclusive access"});
            })
        }, async function() {
            auth.desessionize(res);
            res.send({ok:0, err:"fail auth"});
        });
    });

    app.get('/price', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            payments.hasExclusiveAccess(user, async function() {
                var args = {
                    root_node: root_node,
                    base_cur: req.query.base,
                    quote_cur: req.query.quote,
                }
                proceed_conditional_premium(req,res, 'pages2/price_chart.ejs', true, args)
            }, async function() {
                res.redirect(root_node+"billing")
            })
            
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });


    app.get('/signals', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            payments.hasExclusiveAccess(user, async function() {
                var args = {
                    root_node: root_node,
                }
                proceed_conditional_premium(req,res, 'pages2/signals.ejs', true, args)
            }, async function() {
                res.redirect(root_node+"billing")
            })
            
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

    app.get('/email_verification', async (req, res) => {

        if ('id' in req.query) { // a user may verify from another device (not-logged-in session)
            return await auth.tryVerifyEmail(req.query.id, function() { // but no message will be shown
                res.redirect(root_node+'dashboard')
            }, function() {
                res.redirect(root_node+'login')
            })
        }

        auth.authenticate(req.cookies.sessionID, async function(user) {
            var args = {
                root_node:root_node,
                email: user.email,
            };
            if ('resend' in req.query) {
                console.log("resending")
                auth.sendEmailVerification(user);
                args['msg'] = 'A new email has been sent to your inbox.';
            }

            payments.hasExclusiveAccess(user, function() {
                proceed_conditional_premium(req,res, 'pages2/email_verification.ejs', true, args)
            }, function() {
                proceed_conditional_premium(req,res, 'pages2/email_verification.ejs', false, args)
            });
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });


    app.get('/profile', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            var args = {
                root_node: root_node,
                email: user.email,
                name: user.name,
            }
            console.log(user)
            proceed_conditional_premium(req,res, 'pages2/profile.ejs', true, args)
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

    app.post('/profile', async (req, res) => {
        auth.authenticate(req.cookies.sessionID, async function(user) {
            if (!auth.isEmailVerified(user)) {
                return res.redirect(root_node+"email_verification");
            }
            
            var err = null;
            var name = req.body.name;
            var pass = req.body.password;
            var newpass = req.body.newpassword;


            var args = {
                root_node: root_node,
                email: user.email,
                name: name,
                pass: pass,
                newpass: newpass,
            }

            if (!name || name.length == 0) {
                err = 'Missing name.';
            } else {
                var out = await auth.updateUserName(user.email, name);
                console.log(out)
            }

            if (newpass && newpass.length > 0) {
                if (pass == newpass) {
                    err = 'New password must be different from current password.';
                } else if (!newpass || newpass.length <= 5) {
                    err = 'New password must consist of at least 6 characters.'
                } else  if (!(await auth.validUserPass(user, pass))) {
                    err='Current password is incorrect.';
                } else {
                    var out = await auth.changePass(user.email, newpass);
                    console.log(out)
                    delete args['pass']
                    delete args['newpass']
                }
            }

            
            
            if (err != null) {
                args['err'] = err;
            }
            proceed_conditional_premium(req,res, 'pages2/profile.ejs', true, args)
        }, async function() {
            auth.desessionize(res);
            res.redirect(root_node+'login')
        })
    });

}