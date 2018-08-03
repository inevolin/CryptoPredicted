

module.exports = function(app, auth, root_node, payments) {

	app.get('/login', async function(req, res) {
    	auth.authenticate(req.cookies.sessionID, async function() {
    		res.redirect(root_node+'dashboard')
	    }, async function() {
	    	auth.desessionize(res);
	    	res.render('pages2/login.ejs', {  }); 
	    })
    });

    app.post('/login', async function(req, res) {
    	// is authenticate necessary in a POST?
    	auth.authenticate(req.cookies.sessionID, async function() {
	    	console.log("already logged in")
	    	res.redirect(root_node+'dashboard')
	    }, async function() { 
	        auth.desessionize(res);

	        var email = req.body.email;
	        var pass = req.body.password;
	        var remember = req.body.remember;

	        var out = await auth.tryLogin(res, email, pass, remember);
	        if (out.ok == 1) {
		        res.redirect(root_node+'dashboard')
	        } else {
	        	res.render('pages2/login.ejs', { err: out.err, email:email,pass:pass, remember:remember }); 
	        }
	    	
	    })
    });

    app.get('/signup', async function(req, res) {
    	auth.authenticate(req.cookies.sessionID, async function() {
    		console.log("already logged in")
	    	res.redirect(root_node+'dashboard')
	    }, async function() {
	    	auth.desessionize(res);
	    	res.render('pages2/signup.ejs', {  }); 
	    })
    });

    var registerUser = async function (req, res, type) {
    	// is authenticate necessary in a POST? --> avoid duplicate account creation (if missing index)
    	auth.authenticate(req.cookies.sessionID, async function() {
	    	console.log("already logged in")
	    	res.redirect(root_node+'dashboard')
	    }, async function() {
	        auth.desessionize(res);

	        var name = req.body.name;
	        var email = req.body.email;
	        var pass = req.body.password;
	        var remember = req.body.remember;

	        var out = await auth.tryRegister(res, name, email, pass, remember, type);

	        if (out.ok == 1) {
		        res.redirect(root_node+'dashboard')
	        } else {
	        	res.render('pages2/signup.ejs', { err: out.err, name:name, email:email, pass:pass, remember:remember }); 
	        }
	    	
	    })
    }
    app.post('/signup', async function(req, res) {
    	registerUser(req, res, "normal")
    });
    app.get('/signup/aff/18283848', async function(req, res) {
    	auth.authenticate(req.cookies.sessionID, async function() {
    		console.log("already logged in")
	    	res.redirect(root_node+'dashboard')
	    }, async function() {
	    	auth.desessionize(res);
	    	res.render('pages2/signup.ejs', {  }); 
	    })
    });
    app.post('/signup/aff/18283848', async function(req, res) {
    	registerUser(req, res, "affiliate")
    });

    app.get('/forgot', async function(req, res) {
    	// is authenticate necessary in a POST? --> avoid duplicate account creation (if missing index)
    	auth.authenticate(req.cookies.sessionID, async function() {
	    	console.log("already logged in")
	    	res.redirect(root_node+'dashboard')
	    }, async function() {
	        auth.desessionize(res);
	    	res.render('pages2/forgot.ejs', {  }); 
	    })
    });

    app.post('/forgot', async function(req, res) {
    	// is authenticate necessary in a POST? --> avoid duplicate account creation (if missing index)
    	auth.authenticate(req.cookies.sessionID, async function() {
	    	console.log("already logged in")
	    	res.redirect(root_node+'dashboard')
	    }, async function() {
	        auth.desessionize(res);
	        var email = req.body.email;
	        var out = await auth.resetPass(email);
	        if (out.ok == 1) {
		        res.render('pages2/forgot.ejs', { suc: out.suc }); 
	        } else {
	        	res.render('pages2/forgot.ejs', { err: out.err, email:email }); 
	        }
	    	
	    })
    });


    app.get('/logout', async function(req, res) {
    	auth.desessionize(res);
    	res.redirect(root_node+'login')
    });



    

}