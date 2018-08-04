<html>
	<head>
		<style type="text/css" media="screen">

		table{
			border-collapse:collapse;
			border:1px solid black;
		}

		table td{
			border:1px solid black;
			padding:10px;
		}
		</style>
	</head>
	<body>

<?php
	function execCmd($command) {
		if (isset($command)) {
			$out = shell_exec($command);
			return $out;
		}
	}

	$working_rootdir = "/home/nevolin/public_html/cryptoproto";
	$command = ("$working_rootdir/ENV/bin/python3 $working_rootdir/status.py liveness database"); # escapeshellcmd
	$exec = execCmd($command);
	$res = json_decode($exec, true);
	$liveness = $res['liveness'];

	print("<div style='float:left;'>");
	print("<strong>System stats</strong>");
	print("<table>");
		print("<thead>");
			print("<tr>");
				print("<td>name");
				print("</td>");
				print("<td>notif (sec)");
				print("</td>");
				print("<td>notif (min)");
				print("</td>");
				print("<td>status");
				print("</td>");
			print("</tr>");
		print("</thead>");
	foreach($liveness as $key => $obj) {
		print("<tr>");
			print("<td>");
				print($obj["name"]);
			print("</td>");
			print("<td>");
				print($obj["last_notif_sec"]);
			print("</td>");
			print("<td>");
				print($obj["last_notif_min"]);
			print("</td>");
			print("<td>");
				print($obj["status"] == true? "<img src='images/ok.png'>" : "<img src='images/down.png'>");
			print("</td>");
		print("</tr>");
	}
	print("</table>");
	print("</div>");

	$database = $res['database'];
	print("<div style='float:left; margin-left:10px;'>");
	print("<strong>Database stats</strong>");
	print("<table>");
		print("<thead>");
			print("<tr>");
				print("<td>collection");
				print("</td>");
				print("<td>count");
				print("</td>");
			print("</tr>");
		print("</thead>");
	foreach($database as $key => $obj) {
		print("<tr>");
			print("<td>");
				print($obj['name']);
			print("</td>");
			print("<td>");
				print(number_format($obj['count'], 0, ',','.'));
			print("</td>");
		print("</tr>");
	}
	print("</table>");
	print("</div>");

?>
	</body>
</html>
