// 
process.env.NODE_ENV = 'development';

const root_node = '/PWA/';
const port_http = 8000;
const port_https = 8443;

var express 		= require('express');
var cookieParser = require('cookie-parser')
const MongoClient   = require('mongodb').MongoClient;
const bodyParser    = require('body-parser');
const dbCfg         = require('./db.js');
const mailer         = require('./mail')(root_node);
const fs 			= require('fs');
//var manifest = require('express-manifest');



var key = fs.readFileSync('/home/cryptopredicted/PWA/ssl/server.key');
var cert = fs.readFileSync( '/home/cryptopredicted/PWA/ssl/cryptopredicted_com.crt' );
var ca = fs.readFileSync( '/home/cryptopredicted/PWA/ssl/server-bundle.crt' );
var keys = { key: key, cert: cert, ca: ca }

var app = express();

/*var morgan = require('morgan')
app.use(morgan('combined'))*/

var http = require('http');
var http_server = http.createServer(function (req, res) {
    res.writeHead(301, { "Location": "https://" + req.headers.host.replace(''+port_http, ''+port_https) + req.url });
    res.end();
});
var https = require('https');
var https_server = https.createServer(keys, app)


http_server.listen(port_http);
https_server.listen(port_https);
var io = require('socket.io').listen(https_server);


MongoClient.connect(dbCfg.url, dbCfg.settings, (err, database) => {
	if (err) {
		console.log("ici");
		return console.log(err)
	}
	cryptoDB = database.db('crypto');

	app.use(bodyParser.urlencoded({ extended: true }));
	app.use(bodyParser.raw({type: "*/*"}));
	app.use(bodyParser.json())

	app.use(cookieParser()) // 

	const payments = require('./payments.js')(cryptoDB);
	const auth = require('./auth.js')(cryptoDB, mailer);
	const notifiers         = require('./notifiers/')(cryptoDB);

	require('./websocks')(io, cryptoDB, auth, payments);
	require('./api')(app, cryptoDB);
	require('./views/index2')(app, express, auth, root_node, payments, notifiers, mailer);

	app.render404 = render404
	app.render500 = render500
	app.get('/404', function(req, res) {
		render404(req, res);
	});
	app.get('/500', function(req, res) {
		render500(req, res);
	});

	app.use(function (req, res, next) {
		render404(req, res);
	});

	app.use(function (err, req, res, next) {
		render500(req, res);
	});

});



function render404(req, res) {
	res.status(404);
	res.render('pages2/404', {req:req}, function(err, html) {
		if (err) {
			 console.log(err);
			res.send("Error 404: The page you tried to access does not exist.")
		} else {
			res.send(html);
		}
	});
}
function render500(req, res) {
	res.status(500);
	res.render('pages2/500', {req:req}, function(err, html) {
		if (err) {
			 console.log(err);
			res.send("Error 500: Interval server error.")
		} else {
			res.send(html);
		}
	});
}


