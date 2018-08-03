
/*
	db.users.createIndex({"email":1},{unique:true})
*/

const mongo = require('mongodb');
const bcrypt = require('bcrypt');
const validator = require('validator'); // https://www.npmjs.com/package/validator
const request = require('request'); 


module.exports = function(cryptoDB, mailer) {
	var module = {};

	var authenticated_users_cache = {};

	module.sessionize = function(res, sessionID, cookieOption) {
		res.cookie('sessionID', sessionID, cookieOption)
	}

	module.desessionize = function(res) {
        res.clearCookie('sessionID')
        // this will log the user out from his/her device only
        // other devices may still use same sessionID to authenticate
        // if he/she wishes to logout everywhere, then we need to change the sessionID's value in DB and cache.
	}


	module.authenticate = async function(sessionID, next, fail) {
		// User may login on many devices using same account (because of local cache structure).
		// Even if server restarts, user will remain logged in everywhere because of code in this function.
		if (sessionID == undefined) {
        	fail();
        } else {
        	var user = null;
        	user = await module.findUserSession(sessionID);

        	if (!user) {
        		console.log("invalid session");
        		fail();
        	} else {
	        	next(user)
        	}
        }
	}

	module.isEmailVerified = function(user) {
		if (!('emailVerified' in user) || user.emailVerified == false) {
			return false;
		} else {
			return true;
		}
	}
	module.sendEmailVerification = function(user) {
		mailer.send_email_verification(user.email, user._id);
	}

	function getCookieOption(remember) {
		return (remember == undefined ? {} : { maxAge: 1000*60*60*24*14 }) // remember for 14 days
	}

	module.tryLogin = async function(res, email, pass, remember) {
		if (!email || !validator.isEmail(email)) return {ok:0, err: "Invalid email address."}
        if (!pass || pass.length == 0) return {ok:0, err: "Password cannot be empty"}
        

        var user = await module.findUser(email);
        if (!user) return {ok:0, err: "No such account: check your email address."};
        if (!(await module.validUserPass(user, pass))) return {ok:0, err: "Incorrect password."};


    	var sessionID = user.sessionID;
        module.sessionize(res, sessionID, getCookieOption(remember));

        return {ok:1}
	}


	module.tryRegister = async function(res, name, email, pass, remember, type) {
		if (!name || name.length <= 1) return {ok:0, err: "Invalid name."}
		if (!email || !validator.isEmail(email)) return {ok:0, err: "Invalid email address."}
        if (!pass || pass.length == 0) return {ok:0, err: "Password cannot be empty."}
        if (pass.length <= 5) return {ok:0, err: "Password must contain at least 6 characters."}
        

        var user = await module.findUser(email);
        if (user) return {ok:0, err: "Email address already in use."}

        var sessionID = await module.createSession(email)
    	if (sessionID == null) return {ok:0, err: "Internal server error #AuthTryR1"}

        var a = await module.addUser(name, email, pass, sessionID, type)
        if (a.ok == 1) {
        	console.log("user added successfully")
        	module.sessionize(res, sessionID, getCookieOption(remember))

        	var user = await module.findUser(email);
            module.sendEmailVerification(user);

            module.optin_list(email);
        } else {
        	return {ok:0, err:  "Internal server error #AuthTryR2"}
        }

        return {ok:1}
	}

	module.resetPass = async function(email) {
		if (!email || !validator.isEmail(email)) return {ok:0, err: "Invalid email address."}

        var user = await module.findUser(email);
        if (!user) return {ok:0, err: "No account found with that email address."}

        var generator = require('generate-password');
		var password = generator.generate({
		    length: 6,
		    numbers: true,
		    uppercase: true,
		});
    	var hash = await bcrypt.hash(password, 10);
        var a = await module.updateUserPass(email, hash)
        if (a.ok == 1) {
        	console.log("user password changed successfully")
        	mailer.send_new_password(email, password)
        	return {ok:1, suc: "A new password has been sent to your email's inbox."}
        } else {
        	return {ok:0, err:  "Internal server error #AuthResetP1"}
        }
	}

	module.changePass = async function(email, password) {
		if (!email || !validator.isEmail(email)) return {ok:0, err: "Invalid email address."}

        var user = await module.findUser(email);
        if (!user) return {ok:0, err: "No account found with that email address."}

    	var hash = await bcrypt.hash(password, 10);
        var a = await module.updateUserPass(email, hash)
        if (a.ok == 1) {
        	return {ok:1, suc: "Password changed successfully."}
        } else {
        	return {ok:0, err:  "Internal server error #AuthResetP1"}
        }
	}

	var findUser = async function (query) {
		try {
			var cursor = await cryptoDB.collection('users').findOne(query);
			return cursor
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}
	module.findUser = async function(email) {
		var query = {email: email}
		return await findUser(query)
	}

	module.findUserSession = async function(sessionID) {
		console.log("db: findUserSession");
		var query = {sessionID: sessionID}
		return await findUser(query)
	}

	module.addUser = async function(name, email, pass, sessionID, type) {
		try {
			var hash = await bcrypt.hash(pass, 10);
			var query = {
				email: email,
				name: name,
			   	pass: hash, 
				sessionID: sessionID,
				type: type,
				dateAdded: new Date(),
				emailVerified: false,
			}
			
			var cursor = await cryptoDB.collection('users').insert(query);
			return {ok:(cursor.result.ok && cursor.result.n)}
		} catch (err) {
			if (err.code && err.code == 11000) { // E11000 duplicate key error collection
				return {ok:0, err:"Email address already in use."};
			} else {
				console.log(err)
				return {ok:0, err:"An unexpected error occurred, please contact support."};
			}
		}
	}
	module.updateUserName = async function(email, name) {
		try {
			var query = {email: email}
			var querySet = {'$set' : {name: name} }
			var cursor = await cryptoDB.collection('users').update(query, querySet);
			return {ok:(cursor.result.ok && cursor.result.n)}
		} catch (err) {
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}
	module.updateUserSession = async function(email, sessionID) {
		try {
			var query = {email: email}
			var querySet = {'$set' : {sessionID: sessionID} }
			var cursor = await cryptoDB.collection('users').update(query, querySet);
			return {ok:(cursor.result.ok && cursor.result.n)}
		} catch (err) {
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}
	module.updateUserPass = async function(email, hash) {
		try {
			var query = {email: email}
			var querySet = {'$set' : {pass: hash} }
			var cursor = await cryptoDB.collection('users').update(query, querySet);
			return {ok:(cursor.result.ok && cursor.result.n)}
		} catch (err) {
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}
	module.validUserPass = async function(user, testPass) {
		try {
			var valid = await bcrypt.compare(testPass, user.pass);
			return valid
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}
	module.removeUser = async function(email) {
		try {
			var query = {email: email}
			var cursor = await cryptoDB.collection('users').remove(query);
			return {ok:(cursor.result.ok && cursor.result.n)}
		} catch (err) { 
			console.log(err)
			return {ok:0, err:"An unexpected error occurred, please contact support."};
		}
	}

	module.createSession = async function(email) {
		try {
			var token = email + "_" + (Math.random() * Math.random())
			var iterations = 2+Math.floor(Math.random()*8)
			var hash = await bcrypt.hash(token, iterations)
			return hash;
		} catch (err) {
			console.log(err)
			return null;
		}
	}

	module.tryVerifyEmail = async function(id, next, fail) {
		try {
			var o_id = new mongo.ObjectID(id);

			var query = {_id: o_id}
			var querySet = {'$set' : {emailVerified: true} }
			var cursor = await cryptoDB.collection('users').update(query, querySet);
			
			if (cursor.result.ok && cursor.result.nModified) {
				try {
					var user = await findUser(query);
					mailer.send_new_user(user.email)
				} catch (err) {
					console.log(err)
				}
				next()
			} else {
				console.log("not sending welcome message -- already sent")
				fail()
			}
		} catch (err) {
			console.log(err)
			fail()
		}
	}

	module.optin_list = async function(email) {
		var data = {"email":email , "fields": {}, };
		request({
		    uri: "https://api.mailerlite.com/api/v2/groups/8558744/subscribers",
		    method: "POST",
		    json: true,  
		    body: data,
		    headers: {
		    	"Content-Type": "application/json",
		    	"X-MailerLite-ApiKey": "6eeb4559d19e05552199b627104de432",
		    }
		}, function (error, response, body){
		    console.log(error)
		    console.log(body)
		});
	}

	return module;
}