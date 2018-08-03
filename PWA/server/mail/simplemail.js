
module.exports = function() {
	var module = {};
	
	const sendmail = require('sendmail')();

	module.notifyAdmin = function(subject, html, text) {
		sendmail({
		    from: 'server@cryptopredicted.com',
		    to: 'admin@cryptopredicted.com',
		    subject: subject,
		    html: html,
		    text: text,
		  }, function(err, reply) {
		    console.log(err && err.stack);
		    console.dir(reply);
		});
	}

	return module;
}