

// SMTP settings and mailing functions used by other modules:


module.exports = function(root_node) {
	var module = {};

	const fromEmail = 'support@cryptopredicted.com';
	const nodemailer = require('nodemailer');
	var ejs = require('ejs');
	var fs = require('fs');
	var htmlToText = require('html-to-text');

	const simplemail = require('./simplemail.js')();

	/*
	when using Gmail:
    Enable less secure apps - https://www.google.com/settings/security/lesssecureapps
    Disable Captcha temporarily so you can connect the new device/server - https://accounts.google.com/b/0/displayunlockcaptcha
	*/

	let transporter = nodemailer.createTransport({
        host: 'smtp.gmail.com',
        port: 465,
        secure: true, // true for 465, false for other ports
        auth: {
        	// regular (limited) GMail account:
            user: 'cryptopredicted@gmail.com',
            pass: 'tteesstteerr112233++++',
            // or use your G Suite email account (higher sending limits)
            //user: 'ilja@nevolin.be', 
            //pass: '',
        }
    });
    function doSend(mailOptions) {
    	try {

			transporter.sendMail(mailOptions, (error, info) => {
		        if (error) {
		        	console.log("mail send error:")
		            return console.log(error);
		        }
		        console.log('Message sent: %s', info.messageId);
		    });

    	} catch (err) {
    		console.log(err)
    	}
    }

	module.send_new_user = function(email) {
	    var htmlContent = fs.readFileSync('/home/cryptopredicted/PWA/server/mail/templates/new_user.ejs', 'utf8');
		var htmlRenderized = ejs.render(htmlContent, {});
		var text = htmlToText.fromString(htmlRenderized, { wordwrap: 130 });
		var subject ='Welcome to CryptoPredicted!';
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: subject, 
	        text: text, 
	        html: htmlRenderized 
	    };
	    doSend(mailOptions);

	    text = 'New verified user: ' + email;
	    simplemail.notifyAdmin(subject, text, text);
	}

	

	module.send_new_password = function(email, pass) {
	    var htmlContent = fs.readFileSync('/home/cryptopredicted/PWA/server/mail/templates/new_password.ejs', 'utf8');
		var htmlRenderized = ejs.render(htmlContent, {email:email, pass:pass});
		var text = htmlToText.fromString(htmlRenderized, { wordwrap: 130 });
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: 'Your new password', 
	        text: text, 
	        html: htmlRenderized 
	    };
	    doSend(mailOptions);
	}

	module.send_new_payment = function(email) {
	    var htmlContent = fs.readFileSync('/home/cryptopredicted/PWA/server/mail/templates/new_payment.ejs', 'utf8');
		var htmlRenderized = ejs.render(htmlContent, {});
		var text = htmlToText.fromString(htmlRenderized, { wordwrap: 130 });
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: 'Payment received', 
	        text: text, 
	        html: htmlRenderized 
	    };
	    doSend(mailOptions);
	}

	module.send_trial_expired = function(email) {
	    var htmlContent = fs.readFileSync('/home/cryptopredicted/PWA/server/mail/templates/trial_expired.ejs', 'utf8');
		var htmlRenderized = ejs.render(htmlContent, {});
		var text = htmlToText.fromString(htmlRenderized, { wordwrap: 130 });
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: 'Become a Premium member', 
	        text: text, 
	        html: htmlRenderized 
	    };
	    doSend(mailOptions);
	}

	module.send_custom = function(email, subject, text, html) {
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: subject, 
	        text: text, 
	        html: html 
	    };
	    doSend(mailOptions);
	}

	module.send_to_admin = function(subject, text, html) {
	    simplemail.notifyAdmin(subject, html, text);
	}

	// module.send_new_user('ilja@nevolin.be')
	// module.send_new_password('ilja@nevolin.be', 'test555')
	// module.send_new_payment('ilja@nevolin.be')
	// module.send_to_admin('hi admin', 'hey', 'hey')

	module.send_trade_signal = function(email, title, message) {
	    var htmlContent = fs.readFileSync('/home/cryptopredicted/PWA/server/mail/templates/trade_signal.ejs', 'utf8');
		var htmlRenderized = ejs.render(htmlContent, {message:message, title: title});
		var text = htmlToText.fromString(htmlRenderized, { wordwrap: 130 });
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: title, 
	        text: text, 
	        html: htmlRenderized 
	    };
	    doSend(mailOptions);
	}

	module.send_email_verification = function(email, id) {
	    var htmlContent = fs.readFileSync('/home/cryptopredicted/PWA/server/mail/templates/email_verification.ejs', 'utf8');
	    var link = 'https://cryptopredicted.com'+root_node+'email_verification?id='+encodeURIComponent(id);
		var htmlRenderized = ejs.render(htmlContent, {link:link});
		var text = htmlToText.fromString(htmlRenderized, { wordwrap: 130 });
	    let mailOptions = {
	        from: 'CryptoPredicted <'+ fromEmail +'>', 
	        to: email, // list of receivers : bar@example.com, baz@example.com
	        subject: 'Verify your email', 
	        text: text, 
	        html: htmlRenderized 
	    };
	    doSend(mailOptions);
	}


	return module
}
