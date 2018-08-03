

const MongoClient   = require('mongodb').MongoClient;
const dbCfg         = require('../db.js');
const schedule 		= require('node-schedule');
const mailer         = require('../mail')();

console.log("start ops")

MongoClient.connect(dbCfg.url, dbCfg.settings, async (err, database) => {
	if (err) {
		console.log("ici");
		return console.log(err)
	}
	cryptoDB = database.db('crypto');

	notifyExpiredTrialUsers(cryptoDB)
});

function notifyExpiredTrialUsers(cryptoDB) {
	schedule.scheduleJob('0 * * * * *', async function() {
		step1();
	});
	async function step1() {
		var qry = { expiry: { '$lte': new Date() }}
		var cursor = cryptoDB.collection('trials').find(qry);
		while(await cursor.hasNext()) {
			const doc = await cursor.next();
			if (doc != null) {
				step2(doc);
			}
		}
	}
	async function step2(doc) {
		// this trial has expired
		if ('expireNotified' in doc && doc.expireNotified==true) {
			return; // prevent step3
		} else {
			step3(doc);
		}
	}
	async function step3(doc) {
		var c2 = cryptoDB.collection('payments').find({email: doc.email}).count(function(e, count) {
			//console.log(count+':'+doc.email)
			if (count == 0) { // user has never paid 
				console.log(doc.email)
				step4(doc.email)
			}
		});
	}
	async function step4(email) {
		//if (email.indexOf('cryptopredicted.com') != -1 || email.indexOf('nevolin.be') != -1) // testing purposes
		{ 
			console.log('notifying: ' + email);
			mailer.send_trial_expired(email)
			cryptoDB.collection('trials').update({email:email}, {'$set': {expireNotified: true}})
		}
	}
}

