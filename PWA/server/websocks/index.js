
// https://stackoverflow.com/questions/6873607/socket-io-rooms-difference-between-broadcast-to-and-sockets-in

/*
	authenticate users (preventing piracy)

	user joins room --> send cached JSON
	user changes settings --> leave room, join new room
*/ 

module.exports = function(io, cryptoDB, auth, payments) {

	require('./predictions.js')(io, cryptoDB, auth, payments) 
	require('./table.js')(io, cryptoDB, auth, payments) 
	
}

