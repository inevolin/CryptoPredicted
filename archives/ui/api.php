<?php
	header('Content-type: application/json');
	$working_rootdir = "/home/nevolin/public_html/cryptoproto";
	$CRYPTO = array('BTC','ETH','LTC','DASH','XMR','NXT','ZEC','DGB','XRP','EOS', 'BCH', 'ETC', 'IOT', 'XLM', 'NEO', 'DOGE', 'TRX', 'ADA', 'OMG');


	if(isset($_GET['type']) && isset($_GET['coin'])) {
		$coin = $_GET['coin'];
		if (!in_array($coin, $CRYPTO)) {
			die("cr value inexistent");
		}
		
		switch($_GET['type']) {
			case "generalChart":
				$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : null; 
				if ($interval == null) die("missing interval");

				$historymins = isset($_GET['historymins']) && $_GET['historymins'] > 0 ? escapeshellcmd($_GET['historymins']) : null; 
				if ($historymins == null) die("missing historymins");

				$currentDateTime = isset($_GET['currentDateTime']) ? escapeshellcmd(parseDateTime_toString($_GET['currentDateTime'], $interval)) : null; 
				if ($currentDateTime == null) die("missing currentDateTime");

				if ($interval >= $historymins) die("Interval must be smaller than historymins.");
				generalChart($coin, $interval, $historymins, $currentDateTime);
				break;
			case "priceChart":
				$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : null; 
				if ($interval == null) die("missing interval");

				$historymins = isset($_GET['historymins']) && $_GET['historymins'] > 0 ? escapeshellcmd($_GET['historymins']) : null; 
				if ($historymins == null) die("missing historymins");

				$currentDateTime = isset($_GET['currentDateTime']) ? escapeshellcmd(parseDateTime_toString($_GET['currentDateTime'], $interval)) : null; 
				if ($currentDateTime == null) die("missing currentDateTime");

				if ($interval >= $historymins) die("Interval must be smaller than historymins.");
				priceChart($coin, $interval, $historymins, $currentDateTime);
				break;
			case "predictionChart":
			case "predictionChart3":
				$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : null; 
				if ($interval == null) die("missing interval");

				$historymins = isset($_GET['historymins']) && $_GET['historymins'] > 0 ? escapeshellcmd($_GET['historymins']) : null; 
				if ($historymins == null) die("missing historymins");

				$currentDateTime = isset($_GET['currentDateTime']) ? escapeshellcmd(parseDateTime_toString($_GET['currentDateTime'], $interval)) : null; 
				if ($currentDateTime == null) die("missing currentDateTime");

				$featuresID = isset($_GET['featuresID']) ? escapeshellcmd($_GET['featuresID']) : null; 
				if ($featuresID == null) die("missing featuresID");
				
				$batchSize = isset($_GET['batchsize']) ? escapeshellcmd($_GET['batchsize']) : null; 
				if ($batchSize == null) die("missing batchSize");
				
				$neurons = isset($_GET['neurons']) ? escapeshellcmd($_GET['neurons']) : null; 
				if ($neurons == null) die("missing neurons");

				$hiddenlayers = isset($_GET['hiddenlayers']) ? escapeshellcmd($_GET['hiddenlayers']) : null; 
				if ($hiddenlayers == null) die("missing hiddenlayers");

				$windowsize = isset($_GET['windowsize']) ? escapeshellcmd($_GET['windowsize']) : null; 
				if ($neurons == null) die("missing windowsize");

				$epochs = isset($_GET['epochs']) ? escapeshellcmd($_GET['epochs']) : null; 
				if ($epochs == null) die("missing epochs");

				$predicted_feature = isset($_GET['predicted_feature']) ? escapeshellcmd($_GET['predicted_feature']) : null; 
				if ($predicted_feature == null) die("missing predicted_feature");
				
				
				//if ($interval >= $historymins) die("Interval must be smaller than historymins.");

				if ($_GET['type'] == "predictionChart")
					predictionChart($coin, $interval, $historymins, $currentDateTime, $featuresID, $batchSize, $neurons, $hiddenlayers, $windowsize, $epochs, $predicted_feature, 'predictionChart');	
				else if ($_GET['type'] == "predictionChart3")
					predictionChart3($coin, $interval, $historymins, $currentDateTime, $featuresID, $batchSize, $neurons, $hiddenlayers, $windowsize, $epochs, $predicted_feature, 'predictionChart3');	
				break;
			case "generalChart_socialMentions":
				$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : ''; # custom interval, if any specified
				$datetime = isset($_GET['datetime']) && $_GET['datetime'] > 0 ? escapeshellcmd($_GET['datetime']) : ''; # custom interval, if any specified
				generalChart_socialMentions($coin, $datetime, $interval);
				break;

			case "generalChart_newsMentions":
				$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : ''; # custom interval, if any specified
				$datetime = isset($_GET['datetime']) && $_GET['datetime'] > 0 ? escapeshellcmd($_GET['datetime']) : ''; # custom interval, if any specified
				generalChart_newsMentions($coin, $datetime, $interval);
				break;

			default:
				print("incorrect paramaters");
				break;
				
		}
	} else if (isset($_GET['type']) && $_GET['type'] == "stagesChart") {
		$historymins = isset($_GET['historymins']) && $_GET['historymins'] > 0 ? escapeshellcmd($_GET['historymins']) : null; 
		if ($historymins == null) die("missing historymins");

		$currentDateTime = isset($_GET['currentDateTime']) ? escapeshellcmd(parseDateTime_toString($_GET['currentDateTime'], null)) : null; 
		if ($currentDateTime == null) die("missing currentDateTime");

		stagesChart($historymins, $currentDateTime);
	} else if (isset($_GET['type']) && $_GET['type'] == "backtest") {
		global $working_rootdir;
				
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/backtest.py 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		print $exec;
	} else if (isset($_GET['type']) && $_GET['type'] == "exchangeChart") {

		$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : null; 
		if ($interval == null) die("missing interval");
		
		$base_cur = isset($_GET['base_cur']) ? escapeshellcmd($_GET['base_cur']) : null; 
		if ($base_cur == null) die("missing base_cur");

		$quote_cur = isset($_GET['quote_cur']) ? escapeshellcmd($_GET['quote_cur']) : null; 
		if ($quote_cur == null) die("missing quote_cur");

		$exchange = isset($_GET['exchange']) ? escapeshellcmd($_GET['exchange']) : null; 
		if ($exchange == null) die("missing exchange");

		$historymins = isset($_GET['historymins']) && $_GET['historymins'] > 0 ? escapeshellcmd($_GET['historymins']) : null; 
		if ($historymins == null) die("missing historymins");

		$currentDateTime = isset($_GET['currentDateTime']) ? escapeshellcmd(parseDateTime_toString($_GET['currentDateTime'], null)) : null; 
		if ($currentDateTime == null) die("missing currentDateTime");

		exchangeChart($exchange, $base_cur, $quote_cur, $interval, $historymins, $currentDateTime);
	} else if (isset($_GET['type']) && $_GET['type'] == "predictionChart4") {

		$symbol = isset($_GET['symbol']) ? escapeshellcmd($_GET['symbol']) : null; 
		if ($symbol == null) die("missing symbol");

		$exchange = isset($_GET['exchange']) ? escapeshellcmd($_GET['exchange']) : null; 
		if ($exchange == null) die("missing exchange");

		$interval = isset($_GET['interval']) && $_GET['interval'] > 0 ? escapeshellcmd($_GET['interval']) : null; 
		if ($interval == null) die("missing interval");

		$historymins = isset($_GET['historymins']) && $_GET['historymins'] > 0 ? escapeshellcmd($_GET['historymins']) : null; 
		if ($historymins == null) die("missing historymins");

		$currentDateTime = isset($_GET['currentDateTime']) ? escapeshellcmd(parseDateTime_toString($_GET['currentDateTime'], $interval)) : null; 
		if ($currentDateTime == null) die("missing currentDateTime");

		$featuresID = isset($_GET['featuresID']) ? escapeshellcmd($_GET['featuresID']) : null; 
		if ($featuresID == null) die("missing featuresID");
		
		$batchSize = isset($_GET['batchsize']) ? escapeshellcmd($_GET['batchsize']) : null; 
		if ($batchSize == null) die("missing batchSize");
		
		$neurons = isset($_GET['neurons']) ? escapeshellcmd($_GET['neurons']) : null; 
		if ($neurons == null) die("missing neurons");

		$hiddenlayers = isset($_GET['hiddenlayers']) ? escapeshellcmd($_GET['hiddenlayers']) : null; 
		if ($hiddenlayers == null) die("missing hiddenlayers");

		$windowsize = isset($_GET['windowsize']) ? escapeshellcmd($_GET['windowsize']) : null; 
		if ($neurons == null) die("missing windowsize");

		$epochs = isset($_GET['epochs']) ? escapeshellcmd($_GET['epochs']) : null; 
		if ($epochs == null) die("missing epochs");

		$predicted_feature = isset($_GET['predicted_feature']) ? escapeshellcmd($_GET['predicted_feature']) : null; 
		if ($predicted_feature == null) die("missing predicted_feature");
		
		
		if ($interval >= $historymins) die("Interval must be smaller than historymins.");

		
		predictionChart4($exchange, $symbol, $interval, $historymins, $currentDateTime, $featuresID, $batchSize, $neurons, $hiddenlayers, $windowsize, $epochs, $predicted_feature, 'predictionChart4');	
		
	}

	function emptyElementExists($arr) {
		return array_search("", $arr) !== false;
	}

	function execCmd($command) {
		if (isset($command)) {
			$out = shell_exec($command);
			return $out;
		}
	}

	function parseDateTime_toString($currentDateTime, $interval) {
		$cur_currentDateTime = parseDateTime_toDate($currentDateTime, $interval);
		$currentDateTime = $cur_currentDateTime->format('Y-m-d\TH:i');
		return $currentDateTime;

	}

	function parseDateTime_toDate($currentDateTime, $interval) {
		$now = date_create_from_format('Y-m-d\TH:i', date('Y-m-d\TH:i'));
		if ($currentDateTime == "now") {
			$cur_currentDateTime = $now;
		} else {
			$cur_currentDateTime = date_create_from_format('Y-m-d\TH:i', $currentDateTime);
		}

		if ($cur_currentDateTime == '') {
			die("Invalid DateTime format")	;
		} else if ($cur_currentDateTime > $now) {
			die("DateTime cannot be in the future.");
		}

		if ($interval != null) {
			$Y = intval( $cur_currentDateTime->format('Y') );
			$M = intval( $cur_currentDateTime->format('m') );
			$d = intval( $cur_currentDateTime->format('d') );
			$H = intval( $cur_currentDateTime->format('H') );
			$m = intval( $cur_currentDateTime->format('i') );
			if ($interval <= 60) {
				$m = $m - ($m % $interval);
				$cur_currentDateTime->setTime($H, $m);
			} else if ($interval <= 1440) {
				$m = $m - ($m % 60);
				$H = $H - ($H % ($interval/60));
				$cur_currentDateTime->setTime($H, $m);
			} else if ($interal <= 40320) {
				$m = $m - ($m % 60);
				$H = $H - ($H % ($interval/60));
				$cur_currentDateTime->setTime($H, $m);

				$d = $d - ($d % ($interval/1440));
				$cur_currentDateTime->setDate($Y, $M, $d);
			} else {
				die("Intervals larger than 40320 minutes (= 28 days) not supported yet");
			}
		}

		return $cur_currentDateTime;
		/*
			example:
				"2018-02-04T17:59" will be transformed into:
				"2018-02-04T17:00" when interval is 60minutes
			
			the output is the upper bound datetime such that all data is available within all intervals (i.e. no yet evolving data)

		*/
	}

	function normalize_by_avg($arr) {
	    $min = -1;
	    $max = -1;
	    foreach ($arr as $_ => $val) {
	        if ($val == NULL) continue;
	        $min = $min==-1||abs($val) < $min ? abs($val) : $min;
	        $max = $max==-1||abs($val) > $max ? abs($val) : $max;
	    }
	    foreach ($arr as $_ => $val) {
	    	if ($val == NULL) continue;
	    	$arr[$_] = ($val*100.0/$max);
	    }
	    return $arr;
	}


	function findInCache($mongoClient, $params) {
		$query = new MongoDB\Driver\Query( $params ); 
		$rows = $mongoClient->executeQuery("crypto.caching", $query);
		foreach($rows as $row) {
			$ret = $row->data;
			updateCache($mongoClient, $row->accessCount+1, $row->_id);
			return $ret;
		}
		return null;
	}

	function storeCache($mongoClient, $params) {
		$bulk = new MongoDB\Driver\BulkWrite;
		$params['lastAccess'] = new MongoDB\BSON\UTCDateTime(time()*1000);
		$params['accessCount'] = 1;
		$bulk->insert($params);
		$mongoClient->executeBulkWrite("crypto.caching", $bulk);
	}



	function updateCache($mongoClient, $newcount, $_id) {
		$bulk = new MongoDB\Driver\BulkWrite;
		$bulk->update(
			['_id' => ($_id)],
			['$set' =>
				[
					'accessCount' => $newcount,
					'lastAccess' => new MongoDB\BSON\UTCDateTime(time()*1000)
				]
			],
			['multi' => false, 'upsert' => false]
		);
		$mongoClient->executeBulkWrite("crypto.caching", $bulk);
	}

	function generalChart($coin, $interval, $historymins, $currentDateTime) {

		if (isset($_GET['force']) && $_GET['force'] == "fez56") {
			// allow unlimited processing for predictions producer
		} else {
			if ($historymins / $interval > 2000) {
				die("Please choose a larger interval and/or smaller history size");
			}
		}

		$user = 'ilja47';
		$pass = 'tester123//';
		$mongoClient = new MongoDB\Driver\Manager("mongodb://${user}:${pass}@104.131.121.49/crypto");

		$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "generalChart");
		if (! emptyElementExists($params)) {
			$cache = findInCache($mongoClient, $params);
			if ($cache != null) {
				print($cache);
				return;
			}
		}

		global $working_rootdir;
				
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/socialMentions.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$socialMentions= json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/newsMentions.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$newsMentions = json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/currencyFilter.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$currencyOut = json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/sentimentsSocialFilter.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$socialSentiments = json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/sentimentsNewsFilter.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$newsSentiments = json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/volumeFilter.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$volumes = json_decode($exec, true);

		$kv = array();	

		$kv = add_currencies($kv, $coin, $currencyOut);
		$kv = add_volumes($kv, $coin, $volumes);
		$kv = add_socialMentions($kv, $socialMentions);
		$kv = add_newsMentions($kv, $newsMentions);
		$kv = add_socialsentiments($kv, $socialSentiments);
		$kv = add_newssentiments($kv, $newsSentiments);

		ksort($kv); // if values are inconsistent (with gaps, we sort on label) so we have a nice label-value mapping
		$out = json_encode($kv);
		if ($cache == null) {
			$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "generalChart", "data" => $out);
			// warn: someone can still mess up the results by tweaking currentDateTime by directly accessing API
			if (! emptyElementExists($params)) {
				storeCache($mongoClient, $params);
			}
		}
		print $out;
	}

	function priceChart($coin, $interval, $historymins, $currentDateTime) {

		if (isset($_GET['force']) && $_GET['force'] == "fez56") {
			// allow unlimited processing for predictions producer
		} else {
			if ($historymins / $interval > 2000) {
				die("Please choose a larger interval and/or smaller history size");
			}
		}

		$user = 'ilja47';
		$pass = 'tester123//';
		$mongoClient = new MongoDB\Driver\Manager("mongodb://${user}:${pass}@104.131.121.49/crypto");

		$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "priceChart");
		if (! emptyElementExists($params)) {
			$cache = findInCache($mongoClient, $params);
			if ($cache != null) {
				print($cache);
				return;
			}
		}

		global $working_rootdir;
				
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/currencyFilter.py $coin $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$currencyOut = json_decode($exec, true);

		$kv = array();	

		$kv = add_currencies_basic($kv, $coin, $currencyOut);

		ksort($kv); // if values are inconsistent (with gaps, we sort on label) so we have a nice label-value mapping
		$out = json_encode($kv);
		if ($cache == null) {
			$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "priceChart", "data" => $out);
			// warn: someone can still mess up the results by tweaking currentDateTime by directly accessing API
			if (! emptyElementExists($params)) {
				storeCache($mongoClient, $params);
			}
		}
		print $out;
	}

	function exchangeChart($exchange, $base_cur, $quote_cur, $interval, $historymins, $currentDateTime) {
		$user = 'ilja47';
		$pass = 'tester123//';
		$mongoClient = new MongoDB\Driver\Manager("mongodb://${user}:${pass}@104.131.121.49/crypto");

		$params = array("exchange" => $exchange, "base_cur" => $base_cur, "quote_cur" => $quote_cur, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "exchangeChart");
		if (! emptyElementExists($params)) {
			$cache = findInCache($mongoClient, $params);
			if ($cache != null) {
				print($cache);
				return;
			}
		}
		// warning !! eventhough we update our candlesticks in pseudo real-time (every 20 sec), we may not cache them unless they are fully complete
		// that's what the exchangeFilter.py takes care

		global $working_rootdir;
		
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/exchangeFilter.py $exchange $base_cur $quote_cur $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$currencyOut = json_decode($exec, true);


		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/socialMentions.py $base_cur $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$socialMentions= json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/newsMentions.py $base_cur $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$newsMentions = json_decode($exec, true);


		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/sentimentsSocialFilter.py $base_cur $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$socialSentiments = json_decode($exec, true);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/sentimentsNewsFilter.py $base_cur $interval $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$newsSentiments = json_decode($exec, true);


		$kv = array();	

		$kv = add_socialMentions($kv, $socialMentions);
		$kv = add_newsMentions($kv, $newsMentions);
		$kv = add_socialsentiments($kv, $socialSentiments);
		$kv = add_newssentiments($kv, $newsSentiments);

		$kv = add_exchangeData($kv, $currencyOut);

		ksort($kv);
		$out = json_encode($kv);
		if ($cache == null) {
			$params = array("exchange" => $exchange, "base_cur" => $base_cur, "quote_cur" => $quote_cur, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "exchangeChart", "data" => $out);
			if (! emptyElementExists($params)) {
				storeCache($mongoClient, $params);
			}
		}
		print $out;
	}
	function add_exchangeData_predictionChart($kv, $currentDateTime, $interval, $historymins, $exchange, $base_cur, $quote_cur) {
		global $working_rootdir;

		$cur_currentDateTime = date_create_from_format('Y-m-d\TH:i', $currentDateTime);
		$cur_currentDateTime->add(new DateInterval('PT' . (20*$interval) . 'M'));
		$str_cur_currentDateTime = $cur_currentDateTime->format('Y-m-d\TH:i');
		$cur_historymins = $historymins + (20*$interval);

		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/exchangeFilter.py $exchange $base_cur $quote_cur $interval $cur_historymins $str_cur_currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		
		$predictiontDateTime = date_create_from_format('Y-m-d\TH:i', $currentDateTime);
		$currencyOut = json_decode($exec, true);
		foreach ($currencyOut as $key => $value) {
			$label = $value["label"];
			$labelDt = date_create_from_format('Y-m-d\TH:i', $label);
			
			if ($labelDt >= $predictiontDateTime) {
				$kv['history_extended'][$label] = $value;
			} else {
				$kv['history'][$label] = $value;
			}
		}
		ksort($kv);
		return $kv;
	}
	function add_currencies($kv, $coin, $currencyOut) {
		foreach ($currencyOut as $key => $value) {
			$label = $value["label"];
			$avg = $value["avg"];
			$min = $value["min"];
			$max = $value["max"];
			$open = $value["open"];
			$close = $value["close"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if ($avg == NULL) continue;

			
			$kv[$label]['coins'][$coin]['price-avg'] = $avg;
			$kv[$label]['coins'][$coin]['price-min'] = $min;
			$kv[$label]['coins'][$coin]['price-max'] = $max;
			$kv[$label]['coins'][$coin]['price-open'] = $open;
			$kv[$label]['coins'][$coin]['price-close'] = $close;
		}
		return $kv;
	}
	function add_currencies_basic($kv, $coin, $currencyOut) {
		foreach ($currencyOut as $key => $value) {
			$label = $value["label"];
			$avg = $value["avg"];
			$min = $value["min"];
			$max = $value["max"];
			$open = $value["open"];
			$close = $value["close"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if ($avg == NULL) continue;

			
			$kv[$label]['price-avg'] = $avg;
			$kv[$label]['price-min'] = $min;
			$kv[$label]['price-max'] = $max;
			$kv[$label]['price-open'] = $open;
			$kv[$label]['price-close'] = $close;
		}
		return $kv;
	}
	function add_exchangeData($kv, $currencyOut) {

		foreach ($currencyOut as $key => $value) {

			$label 		= $value["label"];
			$open 		= $value["open"];
			$close 		= $value["close"];
			$low 		= $value["low"];
			$high 		= $value["high"];
			$volume 	= $value["volume"];
			$trades 	= $value["trades"];
			$count 		= $value["count"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if ($open == NULL) continue;
			
			$kv[$label]['low'] = $low;
			$kv[$label]['high'] = $high;
			$kv[$label]['open'] = $open;
			$kv[$label]['close'] = $close;
			$kv[$label]['volume'] = $volume;
			$kv[$label]['trades'] = $trades;
			$kv[$label]['count'] = $count;
			
		}
		return $kv;
	}
	function add_volumes($kv, $coin, $volumes) {
		$VTemp = array();
		foreach ($volumes as $key => $value) {
			$label = $value["label"];
			$avg = $value["avg"];
			$avg_delta = $value["avg_delta"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if($avg==NULL) continue; # warning: a zero value is treated as NULL

			$kv[$label]['coins'][$coin]['volume24h_avg'] = $avg;
			$kv[$label]['coins'][$coin]['volume24h_avg_delta'] = $avg_delta;
			$VTemp[$label] = array('avg' => $avg, 'avg_delta' => $avg_delta);
		}

		return $kv;
	}
	function add_socialMentions($kv, $socialMentions) {
		$socialMTemp = array();
		$MAX_social_sum = 0;
		foreach ($socialMentions as $key => $value) {
			$label = $value["label"];
			$src = $value["source"];
			$count = $value["count"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if($count==NULL) continue;
			
			$kv[$label]['mentions']['social'][$src] = $count;

			if (!isset($kv[$label]['mentions']['social_sum'])) { $kv[$label]['mentions']['social_sum'] = 0; }
			$kv[$label]['mentions']['social_sum'] += $count;
			if ($kv[$label]['mentions']['social_sum'] > $MAX_social_sum) $MAX_social_sum = $kv[$label]['mentions']['social_sum'];

			if (!isset($socialMTemp[$src]))
				foreach($socialMentions as $kk => $vv)
					$socialMTemp[$src][$vv['label']] = NULL;
			$socialMTemp[$src][$label] = $count;
		}

		return $kv;
	}

	function add_newsMentions($kv, $newsMentions) {
		$newsMTemp = array();
		foreach ($newsMentions as $key => $value) {
			$label = $value["label"];
			$count = $value["count"];
			$src = $value["source"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if($count==NULL) continue;

			$kv[$label]['mentions']['news'][$src] = $count;

			if (!isset($kv[$label]['mentions']['news_sum'])) { $kv[$label]['mentions']['news_sum'] = 0; }
			$kv[$label]['mentions']['news_sum'] += $count;

			if (!isset($newsMTemp[$src]))
				foreach($newsMentions as $kk => $vv)
					$newsMTemp[$src][$vv['label']] = NULL;
			$newsMTemp[$src][$label] = $count;
		}
		return $kv;
	}

	function add_socialsentiments($kv, $socialSentiments) {
		$sentimentsMTemp = array();

		foreach ($socialSentiments as $key => $value) {
			$label = $value["label"];
			$pos = $value["positive"];
			$neg = $value["negative"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if($pos==NULL || $neg==NULL) continue;

			$kv[$label]['sentiments']['social'] = array('pos' => $pos, 'neg' => $neg);
			$kv[$label]['sentiments']['social_delta'] = ($pos-$neg);
			$sentimentsMTemp[$label] = array('pos' => $pos, 'neg' => $neg);
		}
		return $kv;
	}

	function add_newssentiments($kv, $newsSentiments) {
		$sentimentsMTemp = array();

		foreach ($newsSentiments as $key => $value) {
			$label = $value["label"];
			$pos = $value["positive"];
			$neg = $value["negative"];

			if(!isset($kv[$label])) $kv[$label] = array();
			if($pos==NULL || $neg==NULL) continue;

			$kv[$label]['sentiments']['news'] = array('pos' => $pos, 'neg' => $neg);
			$kv[$label]['sentiments']['news_delta'] = ($pos-$neg);
			$sentimentsMTemp[$label] = array('pos' => $pos, 'neg' => $neg);
		}
		return $kv;
	}

	function generalChart_socialMentions($coin, $datetime, $interval) {
		global $working_rootdir;
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/socialMentionsExtended.py $coin '$datetime' $interval 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$socialMentions = $exec;
	
		print ($socialMentions);
	}

	function generalChart_newsMentions($coin, $datetime, $interval) {
		global $working_rootdir;
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/newsMentionsExtended.py $coin '$datetime' $interval 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$socialMentions = ($exec);
	
		print ($socialMentions);
	}

	function stagesChart($historymins, $currentDateTime) {

		$user = 'ilja47';
		$pass = 'tester123//';
		$mongoClient = new MongoDB\Driver\Manager("mongodb://${user}:${pass}@104.131.121.49/crypto");

		$params = array("historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "stagesChart");
		if (! emptyElementExists($params)) {
			$cache = findInCache($mongoClient, $params);
			if ($cache != null) {
				print($cache);
				return;
			}
		}

		global $working_rootdir;
				
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/stagesFilter.py $historymins $currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		$data= json_decode($exec, true);

		$kv = array();	

		$tmparr = array();
		foreach ($data['currencies'] as $key => $value) {
			$label = $value['_id']['crypto'];
			$tmparr[$label] = $value["avg"];
		}		
		//$tmparr = normalize_by_avg($tmparr);
		foreach($tmparr as $key => $value) {
			$kv[$key]['price'] = $value;
		}


		$tmparr = array();
		foreach ($data['volumes'] as $key => $value) {
			$label = $value['_id']['crypto'];
			$tmparr[$label] = $value["avg"];
		}		
		//$tmparr = normalize_by_avg($tmparr);
		foreach($tmparr as $key => $value) {
			$kv[$key]['volume'] = $value;
		}


		
		$tmparr = array();
		foreach ($data['socialHype'] as $key => $value) {
			$label = $value['_id']['crypto'];
			$tmparr[$label] = $value["sum"];
		}		
		//$tmparr = normalize_by_avg($tmparr);
		foreach($tmparr as $key => $value) {
			$kv[$key]['socialHype'] = $value;
		}



		$tmparr = array();
		foreach ($data['newsHype'] as $key => $value) {
			$label = $value['_id']['crypto'];
			$tmparr[$label] = $value["sum"];
		}		
		//$tmparr = normalize_by_avg($tmparr);
		foreach($tmparr as $key => $value) {
			$kv[$key]['newsHype'] = $value;
		}
		


		ksort($kv);
		$out = json_encode($kv);
		
		if ($cache == null) {
			$params = array("historymins" => $historymins, "currentDateTime" => $currentDateTime, "func" => "stagesChart", "data" => $out);
			if (! emptyElementExists($params)) {
				storeCache($mongoClient, $params);
			}
		}
		print $out;
	}

	function add_currency_predictionChart($kv, $currentDateTime, $interval, $historymins, $coin) {
		global $working_rootdir;

		$cur_currentDateTime = date_create_from_format('Y-m-d\TH:i', $currentDateTime);
		$cur_currentDateTime->add(new DateInterval('PT' . (sizeof(reset($kv['predictions']))*$interval) . 'M'));

		$str_cur_currentDateTime = $cur_currentDateTime->format('Y-m-d\TH:i');
		$cur_historymins = $historymins + (sizeof(reset($kv['predictions']))*$interval);
		
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/currencyFilter.py $coin $interval $cur_historymins $str_cur_currentDateTime 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		
		$predictiontDateTime = date_create_from_format('Y-m-d\TH:i', $currentDateTime);
		$currencyOut = json_decode($exec, true);
		foreach ($currencyOut as $key => $value) {
			$label = $value["label"];
			if (date_create_from_format('Y-m-d\TH:i', $label) >= $predictiontDateTime) {
				$kv['history_extended'][$label] = $value["avg"];
			} else {
				$kv['history'][$label] = $value["avg"];
			}
		}
		ksort($kv);
		return $kv;
	}



	function count_predictions_completed($mongoClient, $version, $timestamp_predic) {
		$timestamp_predic = new MongoDB\BSON\UTCDateTime($timestamp_predic->getTimestamp()*1000);
		
		$query = new MongoDB\Driver\Query( array('version'=>$version, 'timestamp_predic'=>$timestamp_predic) );
		$rows = $mongoClient->executeQuery("crypto.predictions_completed", $query);
		$count = 0;
		foreach ($rows as $row) {
			$count++;
		}
		return $count;
	}

	function predictionChart3($coin, $interval, $historymins, $currentDateTime, $featuresID, $batchSize, $neurons, $hiddenlayers, $windowsize, $epochs, $predicted_feature, $func) {
		$start = microtime(true);

		$user = 'ilja47';
		$pass = 'tester123//';
		$mongoClient = new MongoDB\Driver\Manager("mongodb://${user}:${pass}@104.131.121.49/crypto");

		$kv = array( 'history'=>[], 'predictions'=>[], 'predictions_traindata'=>[] );	

		$predictionExists = count_predictions_completed($mongoClient, 3, parseDateTime_toDate($currentDateTime, $interval));
        if ($predictionExists == 0) {
        	print json_encode($kv); // no predictions made yet for the given version and datetime
        	return;
        }

		$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "featuresID" => $featuresID, "batchSize" => $batchSize, "neurons" => $neurons, "hiddenlayers" => $hiddenlayers, "windowsize" => $windowsize, "epochs" => $epochs, "predicted_feature" => $predicted_feature, "func" => $func);
		if (! emptyElementExists($params)) {
			$cache = findInCache($mongoClient, $params);
			if ($cache != null) {
				$kv = json_decode($cache, true);
				$kv = add_currency_predictionChart($kv, $currentDateTime, $interval, $historymins, $coin);
				$kv = json_encode($kv);
				print($kv);
				return;
			}
		}

		global $working_rootdir;
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/predictionsFilter3.py $coin $interval $historymins $currentDateTime $featuresID $batchSize $neurons $windowsize $epochs $predicted_feature $hiddenlayers 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		//die($exec);
		$data= json_decode($exec, true);

		foreach ($data['predictions'] as $uid => $arr) {
			foreach ($arr as $key => $value) {
				$label = $value["label"];
				$kv['predictions'][$uid][$label] = $value["value"];
			}
			
		}

		foreach ($data['predictions_traindata'] as $uid => $arr) {
			foreach ($arr as $key => $value) {
				$label = $value["label"];
				$kv['predictions_traindata'][$uid][$label] = $value["value"];
			}
		}

		ksort($kv);
			
		if ($cache == null && sizeof(array_keys($kv['predictions'])) > 0 ) {
			$out = json_encode($kv);
			$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "featuresID" => $featuresID, "batchSize" => $batchSize, "neurons" => $neurons, "hiddenlayers" => $hiddenlayers, "windowsize" => $windowsize, "epochs" => $epochs, "predicted_feature" => $predicted_feature, "func" => $func, "data" => $out);
			if (! emptyElementExists($params)) {
				storeCache($mongoClient, $params);
			}
		}
	
		# don't store history in cache! add it now:
		$kv = add_currency_predictionChart($kv, $currentDateTime, $interval, $historymins, $coin);
		$out = json_encode($kv);
		
		print $out;
	}

	function predictionChart4($exchange, $symbol, $interval, $historymins, $currentDateTime, $featuresID, $batchSize, $neurons, $hiddenlayers, $windowsize, $epochs, $predicted_feature, $func) {
		$start = microtime(true);

		$user = 'ilja47';
		$pass = 'tester123//';
		$mongoClient = new MongoDB\Driver\Manager("mongodb://${user}:${pass}@104.131.121.49/crypto");

		$kv = array( 'history'=>[], 'predictions'=>[], 'predictions_traindata'=>[] );	

		/*$predictionExists = count_predictions_completed($mongoClient, 4, parseDateTime_toDate($currentDateTime, $interval));
        if ($predictionExists == 0) {
        	print json_encode($kv); // no predictions made yet for the given version and datetime
        	return;
        }*/

		/*$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "featuresID" => $featuresID, "batchSize" => $batchSize, "neurons" => $neurons, "hiddenlayers" => $hiddenlayers, "windowsize" => $windowsize, "epochs" => $epochs, "predicted_feature" => $predicted_feature, "func" => $func);
		if (! emptyElementExists($params)) {
			$cache = findInCache($mongoClient, $params);
			if ($cache != null) {
				$kv = json_decode($cache, true);
				$kv = add_currency_predictionChart($kv, $currentDateTime, $interval, $historymins, $coin);
				$kv = json_encode($kv);
				print($kv);
				return;
			}
		}*/

		global $working_rootdir;
		$command = ("$working_rootdir/ENV/bin/python3 ../presenters/predictionsFilter4.py $exchange $symbol $interval $historymins $currentDateTime $featuresID $batchSize $neurons $windowsize $epochs $predicted_feature $hiddenlayers 2>&1"); # escapeshellcmd
		$exec = execCmd($command);
		//die($exec);
		$data= json_decode($exec, true);

		foreach ($data['predictions'] as $uid => $arr) {
			foreach ($arr as $key => $value) {
				$label = $value["label"];
				$kv['predictions'][$uid][$label] = array(
					'low' => $value["low"],
					'high' => $value["high"],
					'open' => $value["open"],
					'close' => $value["close"],
					'volume' => $value['volume'],
					'signal' => $value['signal'],
				);
			}
		}

		// if we predict more than one length, and also wish to show previous predictions
		// then predictionsFilter4 ensures that entries are returned sorted (from oldest to newest)
		// and the above foreach loop will then override oldest by most recent entry for each given $label/timestamp
		// this is how it happens ;)


		ksort($kv);
			
		/*if ($cache == null && sizeof(array_keys($kv['predictions'])) > 0 ) {
			$out = json_encode($kv);
			$params = array("coin" => $coin, "interval" => $interval, "historymins" => $historymins, "currentDateTime" => $currentDateTime, "featuresID" => $featuresID, "batchSize" => $batchSize, "neurons" => $neurons, "hiddenlayers" => $hiddenlayers, "windowsize" => $windowsize, "epochs" => $epochs, "predicted_feature" => $predicted_feature, "func" => $func, "data" => $out);
			if (! emptyElementExists($params)) {
				storeCache($mongoClient, $params);
			}
		}*/
	
		# don't store history in cache! add it now:
		$kv = add_exchangeData_predictionChart($kv, $currentDateTime, $interval, $historymins, $exchange, 'BTC', 'USDT');
		$out = json_encode($kv);
		
		print $out;
	}

?>