

// sendmail can be used to send emails directly from the server (but these may end up in spam inbox).
// It's okay to use this for sending emails to our own (sys admin) address,
// but for sending emails to users it's better to use GSuite or Gmail SMTP to ensure better delivery.

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