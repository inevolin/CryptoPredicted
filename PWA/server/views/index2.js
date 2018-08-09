
// front-end logic with endpoint definitions

const assert = require('assert');
const minify = require('express-minify'); 
const compression = require('compression');
const minifyHTML = require('express-minify-html');
const validator = require('validator');


module.exports = function(app, express, auth, root_node, payments, notifiers, mailer) {

	// unit_tests.test2(auth).catch(err => { console.log(err)});
	
	app.set('view engine', 'ejs');
	app.use(minifyHTML({
	    override:      true,
	    exception_url: false,
	    htmlMinifier: {
	        removeComments:            true,
	        collapseWhitespace:        true,
	        collapseBooleanAttributes: true,
	        removeAttributeQuotes:     true,
	        removeEmptyAttributes:     true,
	        //minifyCSS: true, // too slow
	        //minifyJS:                  true // don't use too slow
	    }
	}));
	app.use(compression());
	app.use(minify()); // minify static server files (we put them all in-line)
	app.use(express.static(__dirname + '/public2'));


	app.get('/', async (req, res) => {
        res.render('pages2/index.ejs', {  }); 
    });
    app.get('/pricing', async (req, res) => {
        res.render('pages2/pricing.ejs', {  }); 
    });
    app.get('/terms', async (req, res) => {
        res.render('pages2/terms.ejs', {  }); 
    });
    app.get('/privacy', async (req, res) => {
        res.render('pages2/privacy.ejs', {  }); 
    });
    app.get('/support', async (req, res) => {
        res.render('pages2/support.ejs', {  }); 
    });
    app.get('/faq', async (req, res) => {
        res.render('pages2/faq.ejs', {  }); 
    });


    app.get('/404', async (req, res) => {
        res.render('pages2/404.ejs', {  }); 
    });
    app.get('/505', async (req, res) => {
        res.render('pages2/505.ejs', {  }); 
    });

    app.post('/optin', async (req, res) => {
    	try {
    		var body = JSON.parse(req.body);
	    	if (!('email' in body) || !validator.isEmail(body.email)) {
	    		return res.send({ok:0, err:'Invalid email address.'});
	    	}
	    	auth.optin_list(body.email);
	    	res.send({ok:1})
		} catch (err) {
			console.log(err);
		}
    });


	require('./users2.js')(app, auth, root_node, payments)
	require('./dashboard2.js')(app, auth, root_node, payments, notifiers)
	require('./checkout.js')(app, mailer, payments)

};