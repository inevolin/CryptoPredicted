exports.pad = function (n, width, z) {
	z = z || '0';
	n = n + '';
	return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

exports.formatDateToString = function (dt) {
	return 	dt.getUTCFullYear() + "-" +
			exports.pad(dt.getUTCMonth()+1, 2) + "-" +
			exports.pad(dt.getUTCDate(), 2) + "T" +
			exports.pad(dt.getUTCHours(), 2) + ":" +
			exports.pad(dt.getUTCMinutes(), 2);

}

exports.roundDateToInterval = function (timestamp, interval) {
	var dt = timestamp.getTime() - (new Date(0)).getTime();
	var mod = dt % (1000*60*interval);
	var sub = dt - mod;
	var add = sub + (new Date(0)).getTime();
	return new Date(add);
}

exports.addDocument = function (docs, key, doc) {
	if (!(key in docs)) {
		docs[key] = doc;	
	} else {
		const deepAssign = require('deep-assign');
		//Object.assign(docs[key], doc);
		deepAssign(docs[key], doc);
	}
}