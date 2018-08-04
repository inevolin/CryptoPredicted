
$(document).ready(function() {
    tag = "myOptionalVersion";
    // set optional message:
    //setTopLabel("We are currently working on improving our push notifications, as a result you may not receive any notifications until the next update has been released.", 0, tag);
});

function checkVersionCode(code) {
    tag = "myVersionCheck";
    var latestVersion = 11;
    clearTopLabel(tag);

    if (parseInt(code) < latestVersion) {
        setTopLabel("A new version is available, please update as soon as possible.", 1,  tag);
    } 
}

function createNotifLabel(msg, type, tag) {
    var P = $("#notifArea");
    var htmls = $('<div class="col-sm-12 removable '+tag+'" style="padding:0;"><div class="alert alert-'+type+'">'+msg+'</div></div>');
    P.append(htmls);
}

function removeNotifLabel(tag) {
    $('#notifArea .'+tag).remove();
    console.log("removeNotifLabel tag:"+tag);
}

$(window).ready(function() {
    $(document).on('dblclick', ".removable", function(e) {
        $(this).remove();
    });
});

function setTopLabel_Notification(json, tag) {
    console.log(json);
	json = 	JSON.parse(json);
	var dt = parseDateTime_string(json['dt'], "HH:mm");
    var msg = json['msg'];
    var type = json['type'];
    var lbl = "<strong>"+dt+"</strong>: " + msg;
    var level = json['level'];

    var created = parseDateTime_dt(json['dt'], "YYYY-MM-DD HH:mm");
    var expires = parseDateTime_dt(json['expires'], "YYYY-MM-DD HH:mm");
    
/*    console.log(type);
    console.log("expires: " + expires);
    console.log("created: " + created);
    console.log("now: " + Date.now());*/

    if (expires <= Date.now()) {
        console.log("expired...");
        clearTopLabel(tag);
    } else {
        setTopLabel(lbl, level, tag);
    }
}

function setTopLabel(lbl, level, tag) {
    if (level == 0) {
        createNotifLabel(lbl, "info", tag);
    } else if (level == 1) {
        createNotifLabel(lbl, "success", tag);
    } else if (level == 2) {
        createNotifLabel(lbl, "warning", tag);
    } else if (level == 3) {
        createNotifLabel(lbl, "danger", tag);
    }
}

function clearTopLabel(tag) {
	console.log("clearTopLabel tag: " + tag);
    removeNotifLabel(tag);
}


function openSettings() {
    JSReceiver.openSettings();
}
function openPriceChart() {
    JSReceiver.openPriceChart();
}
function openForecast() {
    JSReceiver.openForecast();
}

function toggleMoreInfo() {
	if ($('#moreInfoDiv:visible').length > 0) {
		$('#moreInfoDiv:visible').hide();
		return;
	}

	$('#moreInfoDiv:hidden').show();
	$('html, body').animate({
        scrollTop: $("#moreInfoDiv").offset().top
    }, 200);
}

