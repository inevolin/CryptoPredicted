

var DATA = null;

$(document).ready(function() {
    $('canvas').css('opacity', .5);
    var now = new Date();
    $("#_datepicker").datetimepicker({
        //mask: "____-__-__ __-__",
        format: 'Y-m-d H:i',
        value: $("#_datepicker").val() == ""?now:$("#_datepicker").val()
        // http://www.jquerybyexample.net/2012/05/add-timepicker-to-jquery-ui-datepicker.html    
    });
    $('#_trendlinegroup').on('change', function() {
        redrawTrends();
    });
    $('#_emaRecur').on('change', function() {
        redrawTrends();
    });
    requestAndDraw();   
});

function adaptDateTimeToCache() {
    var now = localToUTC(new Date());
    var dtime = $("#_datepicker").length == 0 || $("#_datepicker").val() == "" ? now : localToUTC($("#_datepicker").val());
    if (dtime > now) {
        dtime = now;
    }

    $("#_datepicker").val( UTCtoLocal(dtime).format("YYYY-MM-DD HH:mm") ); // change datetime depending on chosen interval
    
    return dtime;
}

function parseDateTime_dt(str, format) {
    if (typeof format == "undefined" || format == null) {
        format="YYYY-MM-DDTHH:mm";
    }
    return moment.utc(str, format).local(); 
}
function parseDateTime_string(str, format) {
    if (typeof format == "undefined" || format == null) {
        format="YYYY-MM-DDTHH:mm";
    }
    return parseDateTime_dt(str).format(format)  ;
}
function UTCtoLocal(dt) {
    return moment.utc(dt).local(); 
}
function localToUTC_string(dt, format) {
    if (typeof format == "undefined" || format == null) {
        format="YYYY-MM-DDTHH:mm";
    }
    return localToUTC(dt).format(format);
}
function localToUTC(dt, format) {
    if (typeof format == "undefined" || format == null) {
        format="YYYY-MM-DDTHH:mm";
    }
    return moment(dt, format).utc()
}

function preventCrazySettings() {
    var hmin = parseInt($('#_historymins').find(':selected').val());
    var int = parseInt($('#_interval').find(':selected').val());
    /*if (hmin/int > 2000) {
        alert("Please choose a larger interval and/or a smaller history size."); 
        return false;
    }
    if (int > hmin) {
        alert("Please choose an interval smaller than the history size.");
        return false;
    }*/
    return true;
}
isObject = function(a) {
    return (!!a) && (a.constructor === Object);
};

function xaxis_dtick() {
    //var x = 1000 * 60 * Math.ceil( Math.sqrt($("#_historymins").val())*Math.sqrt($("#_interval").val()) ); // $('#_interval').val()
    //return x;
    return $('#_interval').val()*1000*60*2;
}
function redrawTrends() {
    if (typeof Plotly !== "undefined") {
        $('#chart').css('opacity', .5);
        //drawGraphs();
        var updateArr = [];
        var updateTraces = [];
        var plotDiv = document.getElementById('chart');
        var plotData = plotDiv.data;
        for (var i in plotData) {
            var obj = plotData[i];
            if ('isTrend' in obj) {
                arrs = obj.isTrend(DATA);
                //normalize(arrs);
                for (var j in arrs) {
                    var newTrace = arrs[j];
                    if ('isTrend' in newTrace && newTrace.name == obj.name) {
                        var newData = {y:[]};
                        newData.y = newTrace.y.slice();
                        updateArr.push(newData);
                        updateTraces.push(parseInt(i));
                    }
                }
            }
        }
        var layout = {
            // 'xaxis.dtick': xaxis_dtick(),
        }
        Plotly.animate('chart', {data:updateArr, traces:updateTraces, layout:layout}, {transition: {duration: 250,easing: 'cubic-out'}} );
        $('#chart').css('opacity', 1);
    } else {
        draw_mobile_app_chart_predictions();
    }
}

function addClickEvents() {
    var myPlot = document.getElementById('chart');
    myPlot.on('plotly_click', function(data){
        var label = data.points[0].x;
        label = localToUTC_string(label)
        $('#socialMentions').html('');
        $('#newsMentions').html('');
        $.getJSON('api.php', {'type':'generalChart_socialMentions', 'coin':$('#_crypto').val(), 'interval':$('#_interval').val(), 'datetime': label.replace(' ', 'T')}, function (data, status) {
            var html = "<h2>Social mentions:</h2>";
            for (var k in data) {
                var d = data[k];
                var str = d['body'];
                str = str.replace(/(?:\r\n|\r|\n)/g, '<br />');
                var url = d['url'];
                var src = d['source'];
                html +='<span>'+str+'</span> <a href="'+url+'" target="_blank">('+src+')</a><br>---------------<br>';
            }
            $('#socialMentions').html(html);
            $('html, body').animate({
                scrollTop: $("#scrollHere_1").offset().top/2
            }, 200);
        });
        $.getJSON('api.php', {'type':'generalChart_newsMentions', 'coin':$('#_crypto').val(), 'interval':$('#_interval').val(), 'datetime':label.replace(' ', 'T')}, function (data, status) {
            var html = "<h2>News headlines:</h2>";
            for (var k in data) {
                var d = data[k];
                var str = d['title'];
                str = str.replace(/(?:\r\n|\r|\n)/g, '<br />');
                var url = d['url'];
                var src = d['source'];
                html +='<span>'+str+'</span> <a href="'+url+'" target="_blank">('+src+')</a><br>---------------<br>';
            }

            $('#newsMentions').html(html);
            $('html, body').animate({
                scrollTop: $("#scrollHere_1").offset().top/2
            }, 200);
        });
    });
}
function setTraceVisibility(obj) {
    var plotDiv = document.getElementById('chart');
    if (plotDiv == null) {
        return;
    }
    var plotData = plotDiv.data;
    for (var i in plotData) {
        var o = plotData[i];
        if (o.name == obj.name && 'visible' in o) {
            obj.visible = o.visible;
            break;
        }
    }
}
function draw_price(data) {

    var trace_avg = {
        name: 'Price avg',
        x: [], y: [],
        type: 'scatter',
        fill: 'tonexty',
        fillcolor:'#ffcd56',
        line: {shape: 'spline', smoothing: 1.3, color:'#9e821c'},
        mode:'lines+markers',
    };
    setTraceVisibility(trace_avg);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace_avg.x.push(dt);
        if ('open' in val) {
            trace_avg.y.push( (val['open']+val['close']+val['low']+val['high'])/4 );
        } else {
            trace_avg.y.push( NaN );
        }
    });
    return [trace_avg];
}
function draw_price_trend(data) {

    var trace = {
        name: 'EMA(price)',
        x: [], y: [],
        type: 'scatter',
        line: {color:'black'},
        visible: 'legendonly',
        isTrend : draw_price_trend,
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('open' in val) {
            trace.y.push( (val['open']+val['close']+val['low']+val['high'])/4 );
        } else {
            trace.y.push( NaN );
        }
    });
    trace.y = createTrendLine_EMA(trace.y);
    return [trace];
}

//todo: EMA - https://github.com/patharanordev/ema


function draw_price_candles(data) {

    var trace = {
        name: 'Price (USD)',
        decreasing: {line: {color: '#f75656'}},
        increasing: {line: {color: '#6bf755'}}, 
        line: {color: 'rgba(31,119,180,1)'}, 
        x: [],
        low: [],
        high: [],
        open: [],
        close: [],
        type: 'candlestick', 
        xaxis: 'x', 
        yaxis: 'y',
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('low' in val) {
            trace.low.push( val['low']);
            trace.high.push( val['high']);
            trace.open.push( val['open']);
            trace.close.push( val['close']);
        } else {
            trace.low.push( NaN );
            trace.high.push( NaN );
            trace.open.push( NaN );
            trace.close.push( NaN );
        }
    });
    return [trace];
}

function draw_mentions_social_sum(data) {
    var trace = {
        name: 'mentions_social_sum',
        x: [], y: [],
        type: 'scatter',
        mode:'markers',
        yaxis: 'y2',
        visible: 'legendonly',
    };
    var trace_trend = {
        name: 'EMA(mentions_social_sum)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        isTrend : draw_mentions_social_sum,
        visible: 'legendonly',
    };
    setTraceVisibility(trace);
    setTraceVisibility(trace_trend);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('mentions' in val && 'social_sum' in val['mentions']) {
            trace.y.push( val['mentions']['social_sum'] );
        } else { 
            trace.y.push( NaN );
        }
    });
    normalize_max(trace.y);
    trace_trend.x = trace.x.slice();
    trace_trend.y = trace.y.slice();
    trace_trend.y = createTrendLine_EMA(trace.y);
    return [trace_trend];
}
function draw_mentions_social_avg(data) {
    var trace = {
        name: 'mentions_social_avg',
        x: [], y: [],
        type: 'scatter',
        mode:'markers',
        yaxis: 'y2',
        visible: 'legendonly',
    };
    var trace_trend = {
        name: 'EMA(mentions_social_avg)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        isTrend : draw_mentions_social_avg,
        visible: 'legendonly',
    };
    setTraceVisibility(trace);
    setTraceVisibility(trace_trend);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('mentions' in val && 'social' in val['mentions']) {
            trace.y.push( average(Object.values(val['mentions']['social'])) );
        } else { 
            trace.y.push( NaN );
        }
    });
    normalize_max(trace.y);
    trace_trend.x = trace.x.slice();
    trace_trend.y = trace.y.slice();
    trace_trend.y = createTrendLine_EMA(trace.y);
    return [ trace_trend]; // exclude scatter dots: trace
}
function draw_mentions_news_avg(data) {
    var trace = {
        name: 'mentions_news_avg',
        x: [], y: [],
        type: 'scatter',
        mode:'markers',
        yaxis: 'y2',
        visible: 'legendonly',
    };
    var trace_trend = {
        name: 'EMA(mentions_news_avg)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        visible: 'legendonly',
        isTrend : draw_mentions_news_avg,
    };
    setTraceVisibility(trace);
    setTraceVisibility(trace_trend);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('mentions' in val && 'news' in val['mentions']) {
            trace.y.push( average(Object.values(val['mentions']['news'])) );
        } else { 
            trace.y.push( NaN );
        }
    });
    normalize_max(trace.y);
    trace_trend.x = trace.x.slice();
    trace_trend.y = trace.y.slice();
    trace_trend.y = createTrendLine_EMA(trace.y);
    return [ trace_trend]; // exclude scatter dots: trace
}
function draw_mentions_social(data) {
    var socialData = {};
    $.each(data, function(label, obj) {
        if ('mentions' in obj && 'social' in obj['mentions']) {
            $.each(obj['mentions']['social'], function(source, count) {
                if (!(source in socialData)) {
                    socialData[source] = {};
                    $.each(data, function(label, _) {
                        _label = parseDateTime_string(label);
                        socialData[source][_label]=NaN;
                    });
                }
                _label = parseDateTime_string(label);
                socialData[source][_label]=count;
            });
        }
    });

    var traces = [];
    var socialDataNew = {};
    $.each(socialData, function(source, obj) {
        if (!(source in socialDataNew)) {
            socialDataNew[source] = {};
        }
        socialDataNew[source]['y'] = Object.values(obj);
        normalize_max(socialDataNew[source]['y']);
        socialDataNew[source]['x'] = Object.keys(obj);
    });
    $.each(socialDataNew, function(source, arr_normal) {   
        var trace = {
            name: 'mentions_social: '+source,
            x: [], y: [],
            type: 'scatter',
            mode:'markers',
            yaxis: 'y2',
            visible: 'legendonly',
        };
        var trace_trend = {
            name: 'EMA(mentions_social): '+source,
            x: [], y: [],
            type: 'scatter',
            yaxis: 'y2',
            visible: 'legendonly',
            isTrend : draw_mentions_social,
            visible: 'legendonly',
        };
        setTraceVisibility(trace);
        setTraceVisibility(trace_trend);
        trace.x = arr_normal.x.slice();
        trace.y = arr_normal.y.slice();
        trace_trend.x = trace.x.slice();
        trace_trend.y = trace.y.slice();
        trace_trend.y = createTrendLine_EMA(trace.y).slice();
        //traces.push(trace);
        traces.push(trace_trend);
    });
    return traces;
}
function draw_sentiments_social_delta(data) {
    var trace = {
        name: 'EMA(sentiments_social_delta)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        visible: 'legendonly',
        isTrend : draw_sentiments_social_delta,
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('sentiments' in val && 'social_delta' in val['sentiments']) {
            trace.y.push( val['sentiments']['social_delta'] );
        } else { 
            trace.y.push( NaN );
        }
    });
    normalize_max(trace.y);
    trace.y = createTrendLine_EMA(trace.y);
    return [trace];
}
function draw_sentiments_news_delta(data) {
    var trace = {
        name: 'EMA(sentiments_news_delta)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        visible: 'legendonly',
        isTrend : draw_sentiments_news_delta,
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('sentiments' in val && 'news_delta' in val['sentiments']) {
            trace.y.push( val['sentiments']['news_delta'] );
        } else { 
            trace.y.push( NaN );
        }
    });
    console.log(trace.y)
    normalize_max(trace.y);
    console.log(trace.y)
    trace.y = createTrendLine_EMA(trace.y);
    return [trace];
}

function draw_volume24h_avg(data) {

    var trace = {
        name: 'EMA(volume24h_avg trend)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        visible: 'legendonly',
        isTrend : draw_volume24h_avg,
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('volume' in val) {
            trace.y.push( val['volume']);
        } else {
            trace.y.push( NaN );
        }
    });
    normalize_max(trace.y);
    trace.y = createTrendLine_EMA(trace.y);
    return [trace];
}
function draw_volume24h_avg_delta(data) {

    var trace = {
        name: 'EMA(volume24h_avg_delta trend)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        isTrend : draw_volume24h_avg_delta,
        visible: 'legendonly',
    };
    setTraceVisibility(trace);

    var prev_vol = null;
    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        if ('volume' in val) {
            if (prev_vol != null) {
                trace.y.push( val['volume'] - prev_vol );
            } else {
                trace.y.push( NaN );
            }
            prev_vol = val['volume'];
        } else {
            trace.y.push( NaN );
        }
    });
    normalize_max(trace.y);
    trace.y = createTrendLine_EMA(trace.y);
    return [trace];
}


function draw_TimePriceVolume_3d(data) {

    var trace_dots = {
        name: "dots",
        x: [], y: [], z: [],
        type: 'scatter3d',
        mode: 'markers',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 2
        }
    };
    var trace_mesh = {
        names:"mesh",
        x: [], y: [], z: [],
        alphahull: 40,
        opacity: .3,
        type: 'mesh3d',
    };
    $.each(data, function(k,val) {
        var x, y, z;
        x =  parseDateTime_string(k) ;
        if ('low' in val) {
            z = (val['low']+val['open']+val['close']+val['high'])/4;
            y = val['volume'];
        }
        if (y != undefined && z != undefined) {
            trace_dots.x.push(x);
            trace_dots.y.push(y);
            trace_dots.z.push(z);
        }
    });
    trace_mesh.x = trace_dots.x;
    trace_mesh.y = trace_dots.y;
    trace_mesh.z = trace_dots.z;
    var data = [trace_dots , trace_mesh];
    return data;
}

function draw_TimeVolumeHype_3d(data) {
    var trace_dots = {
        name: "dots",
        x: [], y: [], z: [],
        type: 'scatter3d',
        mode: 'markers',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 2
        }
    };
    var trace_mesh = {
        names:"mesh",
        x: [], y: [], z: [],
        alphahull: 40,
        opacity: .3,
        type: 'mesh3d',
    };
    $.each(data, function(k,val) {
        var x, y, z;
        x =  parseDateTime_string(k) ;
        if ('low' in val) {
            y = (val['low']+val['high']+val['open']+val['close'])/4;

            if ('mentions' in val && 'social' in val['mentions']) {
                if (z == undefined) z = 1;
                z *= average(Object.values(val['mentions']['social']))
            }
            if ('mentions' in val && 'news' in val['mentions']) {
                if (z == undefined) z = 1;
                z *= average(Object.values(val['mentions']['news']))
            }
        }
        if (y != undefined && z != undefined) {
            trace_dots.x.push(x);
            trace_dots.y.push(y);
            trace_dots.z.push(z);
        }
    });
    trace_mesh.x = trace_dots.x;
    trace_mesh.y = trace_dots.y;
    trace_mesh.z = trace_dots.z;
    var data = [trace_dots , trace_mesh];
    return data;
}

function draw_TimePriceHype_3d(data) {
    var trace_dots = {
        name: "dots",
        x: [], y: [], z: [],
        type: 'scatter3d',
        mode: 'markers',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 2
        }
    };
    var trace_mesh = {
        names:"mesh",
        x: [], y: [], z: [],
        alphahull: 15, //larger value, smaller cluster mesh
        opacity: .5,
        type: 'mesh3d',
    };
    $.each(data, function(k,val) {
        var x, y, z;
        x =  parseDateTime_string(k) ;
        
        if ('low' in val)
            z = (val['low']+val['high']+val['open']+val['close'])/4;

        if ('mentions' in val && 'social' in val['mentions']) {
            if (y == undefined) y = 1;
            y *= average(Object.values(val['mentions']['social']))
        }
        if ('mentions' in val && 'news' in val['mentions']) {
            if (y == undefined) y = 1;
            y *= average(Object.values(val['mentions']['news']))
        }

        if (y != undefined && z != undefined) {
            trace_dots.x.push(x);
            trace_dots.y.push(y);
            trace_dots.z.push(z);
        }
    });
    trace_mesh.x = trace_dots.x;
    trace_mesh.y = trace_dots.y;
    trace_mesh.z = trace_dots.z;
    var data = [trace_dots , trace_mesh];
    return data;
}
function draw_VolumePriceHype_3d(data) {
    var trace_dots = {
        name: "dots",
        x: [], y: [], z: [],
        type: 'scatter3d',
        mode: 'markers',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 2
        }
    };
    var trace_mesh = {
        names:"mesh",
        x: [], y: [], z: [],
        alphahull: 25, //larger value, smaller cluster mesh
        opacity: .5,
        type: 'mesh3d',
    };
    $.each(data, function(k,val) {
        var x, y, z;
        if ('low' in val ) {
            z = (val['low']+val['high']+val['open']+val['close'])/4;
            x = val['volume'];
        }
        if ('mentions' in val && 'social' in val['mentions']) {
            if (y == undefined) y = 1;
            y *= average(Object.values(val['mentions']['social']))
        }
        if ('mentions' in val && 'news' in val['mentions']) {
            if (y == undefined) y = 1;
            y *= average(Object.values(val['mentions']['news']))
        }

        if (x != undefined && y != undefined && z != undefined) {
            trace_dots.x.push(x);
            trace_dots.y.push(y);
            trace_dots.z.push(z);
        }
    });
    trace_mesh.x = trace_dots.x;
    trace_mesh.y = trace_dots.y;
    trace_mesh.z = trace_dots.z;
    var data = [trace_dots , trace_mesh];
    return data;
}

function commarize(val) {
  // Alter numbers larger than 1k
  if (val >= 1e3) {
    var units = ["k", "M", "B", "T"];
    
    // Divide to get SI Unit engineering style numbers (1e3,1e6,1e9, etc)
    var unit = Math.floor(((val).toFixed(0).length - 1) / 3) * 3;
    // Calculate the remainder
    var num = (val / ('1e'+unit)).toFixed(2)
    var unitname = units[Math.floor(unit / 3) - 1]
    
    // output number remainder + unitname
    return num + unitname
  }
  
  // return formatted original number
  return val.toLocaleString()
}

function draw_stagesPriceHype3d(data) {
    
    var ret = [];

    var minVol=-1, maxVol=-1;
    $.each(data, function(k,val) {
        var trace_dots = {
            name: k,
            x: [], y: [], z: [],
            volume24: 1,
            text: [],
            type: 'scatter3d',
            mode: 'markers',
            marker: {
              //color: 'rgb(23, 190, 207)',
              //size: 7
              opacity:0.8,
            }
        };
        var x, y=0, z=0;
        if ('price' in val) {
            x = val['price'];
        }

        if ('newsHype' in val) {
            y = val['newsHype'];
        } 

        if ('socialHype' in val) {
            z = val['socialHype'];
        }

        if ('volume' in val) {
            trace_dots.volume24 = val['volume'];
            if (minVol==-1 || val['volume'] < minVol) minVol = val['volume'];
            if (maxVol==-1 || val['volume'] > maxVol) maxVol = val['volume'];
        } 

        if (x != undefined && y != undefined && z != undefined) {
            trace_dots.x.push(x);
            trace_dots.y.push(y);
            trace_dots.z.push(z);
            trace_dots.text.push('vol24h: '+commarize(trace_dots.volume24)+'\n<br>'+k);

            ret.push(trace_dots);
        }
    });
    $.each(ret, function(k, val) {
        val.marker.size  =  Math.log( (val.volume24)*(val.volume24)  )/Math.log(6);
    });

    return ret;
}

function indexOfMax(arr) {
    if (arr.length === 0) {
        return -1;
    }
    var max = arr[0];
    var maxIndex = 0;
    for (var i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            maxIndex = i;
            max = arr[i];
        }
    }
    return maxIndex;
}
function indexOfMin(arr) {
    if (arr.length === 0) {
        return -1;
    }
    var max = arr[0];
    var maxIndex = 0;
    for (var i = 1; i < arr.length; i++) {
        if (arr[i] < max) {
            maxIndex = i;
            max = arr[i];
        }
    }
    return maxIndex;
}

function create_trace_sma_draw_predictionsChart(data, name) {
    var trace_sma = {
        'name': name,
        x: [], y: [],
        type: 'scatter',
        mode:'lines+markers',
        //visible: 'legendonly',
        isTrend : draw_predictionsChart,
    };
    setTraceVisibility(trace_sma);
    $.each(data, function(k,val) {    
        trace_sma.x.push(parseDateTime_string(k)); // UTC to local
        trace_sma.y.push( val );
    });

    trace_sma.y = createTrendLine_EMA(trace_sma.y);
    return trace_sma;
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function uuidv4() {
    return ""+(getRandomInt(9)+""+getRandomInt(9)+""+getRandomInt(9)+""+getRandomInt(9)+"");
}


function reduce_sum_arr(arr) {
    var sum = 0;
    $.each(arr, function(k, v) {
        if (!isNaN(v) && v != null) {
            sum += v;
        }
    });
    return sum;
}

function draw_predictionsChart(data) {

    if (data['predictions'].length == 0) {
        $('#_status').text('No prediction data (yet) - try updating the datetime.');
        $("#chart img:last-child").remove();
       // Plotly.newPlot(chart, []);
        return null;
    }
    
    var ret = [];
    
    var trace_hist = {
        name: 'Price avg',
        x: [], y: [],
        type: 'scatter',
        fillcolor:'#000',
        line: {shape: 'spline', smoothing: 0, color:'#555'},
        mode:'lines+markers',
    };
    var trace_hist_ext = {
        name: 'Price avg extended',
        x: [], y: [],
        type: 'scatter',
        fillcolor:'#333',
        opacity:.5,
        line: {shape: 'spline', smoothing: 0, color:'#555'},
        mode:'lines+markers',
    };
    setTraceVisibility(trace_hist);
    setTraceVisibility(trace_hist_ext);
    $.each(data['history'], function(k,val) {
        var dt = parseDateTime_string(k);
        trace_hist.x.push(dt);
        trace_hist.y.push( val );
    });

    trace_hist_ext.x.push( trace_hist.x[trace_hist.x.length-1] );
    trace_hist_ext.y.push( trace_hist.y[trace_hist.y.length-1] );
    $.each(data['history_extended'], function(k,val) {
        var dt = parseDateTime_string(k);
        trace_hist_ext.x.push(dt);
        trace_hist_ext.y.push( val );
    });

    

    
    var smaprice = create_trace_sma_draw_predictionsChart(data['history'], 'EMA(Price avg)');
    var sma_price_tail = smaprice.y[ smaprice.y.length -1 ];
    var trace_largest = null;
    var trace_smallest = null;

    var trace_i = 0;
    $.each(data['predictions'], function(uid, arr) {
        var trace_predic = {
            x: [], y: [],
            type: 'scatter',
            fillcolor:'#973d3d',
            line: {shape: 'spline', smoothing: 0, color:'#5f1414'},
            mode:'lines+markers',
            opacity:.15,
            
            'legendgroup': 'Predictions',
            'name': 'Predictions',
            'showlegend': false,
            visible: 'legendonly',
        };
        if (trace_i++ == 0) {
            trace_predic['showlegend'] = true;
        }
        setTraceVisibility(trace_predic);

        var i = 0;
        $.each(arr, function(dt,val) {
            trace_predic.x.push(parseDateTime_string(dt));
            trace_predic.y.push( val );
        });
        if (trace_largest == null || reduce_sum_arr(trace_predic.y) > reduce_sum_arr(trace_largest.y)) {
            trace_largest = trace_predic;
        }
        if (trace_smallest == null || reduce_sum_arr(trace_predic.y) < reduce_sum_arr(trace_smallest.y)) {
            trace_smallest = trace_predic;
        }
        ret.push( trace_predic );
    });

    // SMA(price avg + min(prediction))
    var head = {};
    $.each(data['history'], function(key, val) {
        head[key] = val;
    });
    for (var i = 0; i < trace_smallest.y.length; i++) {
        head[ localToUTC_string(trace_smallest.x[i], "YYYY-MM-DDTHH:mm") ] = trace_smallest.y[i];
    }
    var smaprice_extended_min = create_trace_sma_draw_predictionsChart(head, 'SMA(Price avg + min(prediction))');
    /*for (var key = 0; key < Object.keys(data['history']).length; key++) {
        smaprice_extended_min.y[key] = NaN;
    }*/
    
    
    // SMA(price avg + max(prediction))
    var head = {};
    $.each(data['history'], function(key, val) {
        head[key] = val;
    });
    for (var i = 0; i < trace_largest.y.length; i++) {
        head[ localToUTC_string(trace_largest.x[i], "YYYY-MM-DDTHH:mm") ] = trace_largest.y[i];
    }

    var smaprice_extended_max = create_trace_sma_draw_predictionsChart(head, 'SMA(Price avg + max(prediction))');
    /*for (var key = 0; key < Object.keys(data['history']).length; key++) {
        smaprice_extended_max.y[key] = NaN;
    }*/


    // average prediction:
    predictions_avg = { x:[], y:[] };
    $.each(data['predictions'], function(uid, arr) {
        var i = 0;
        $.each(arr, function(dt,val) {
            if (predictions_avg.x[i] == undefined) {
                predictions_avg.x[i] = parseDateTime_string( dt );
                predictions_avg.y[i] = [];
            }
            predictions_avg.y[i].push(val);
            ++i;
        });
    });
    
    $.each(predictions_avg.y, function(idx, arr) {
        var sum = reduce_sum_arr(arr);
        predictions_avg.y[idx] = sum/arr.length;
    });
    var trace_predic_avg = {
        name: 'Predicted price avg.',
        x: predictions_avg.x.slice(),
        y: predictions_avg.y.slice(),
        type: 'scatter',
        fillcolor:'red',
        line: {shape: 'spline', smoothing: 0, color:'red'},
        mode:'lines+markers',
        opacity:.6,
        visible: 'legendonly',
    };
    setTraceVisibility(trace_predic_avg);
    

    // SMA(Price avg + avg(prediction))
    var head = {};
    $.each(data['history'], function(key, val) {
        head[key] = val;
    });
    for (var i = 0; i < trace_predic_avg.y.length; i++) {
        head[ localToUTC_string(trace_predic_avg.x[i], "YYYY-MM-DDTHH:mm") ] = trace_predic_avg.y[i];
    }
    var smaprice_extended_avg = create_trace_sma_draw_predictionsChart(head, 'SMA(Price avg + avg(prediction))');
    /*for (var key = 0; key < Object.keys(data['history']).length; key++) {
        smaprice_extended_avg.y[key] = NaN;
    }*/

    ret.unshift( trace_hist );
    ret.unshift( smaprice_extended_max);
    ret.unshift( smaprice_extended_avg);
    ret.unshift( smaprice_extended_min);
    ret.unshift( trace_hist_ext );
    
    ret.push( trace_predic_avg );   

    // signals
    var firstVal = predictions_avg.y[0];
    var indexOfMaxValue = indexOfMax( predictions_avg.y );
    var indexOfMinValue = indexOfMin( predictions_avg.y );
    var buys = [], sells = [];
    if (indexOfMinValue != indexOfMaxValue) {
        buys.push(  predictions_avg.x[indexOfMinValue] );
        sells.push( predictions_avg.x[indexOfMaxValue] );
    }
    if (indexOfMinValue > indexOfMaxValue && firstVal < predictions_avg.y[indexOfMaxValue]) {
        buys.push(  predictions_avg.x[0] );
    }
    data['_buys'] = buys;       // notice we change the data object (by reference)
    data['_sells'] = sells;     // notice we change the data object (by reference)



    trace_i = 0;
    $.each(data['predictions_traindata'], function(uid, arr) {
        var trace_predic_traindata = {
            //name: 'train: ' + uid,
            x: [], y: [],
            type: 'scatter',
            fillcolor:'#2c7a36',
            line: {shape: 'spline', smoothing: 0, color:'#39bf4b'},
            mode:'lines+markers',
            opacity:.15,
            
            'legendgroup': 'Predictions (train data)',
            'name': 'Predictions (train data)',
            showlegend: false,
            visible: 'legendonly',
        };
        if (trace_i++ == 0) {
            trace_predic_traindata['showlegend'] = true;
        }

        setTraceVisibility(trace_predic_traindata);
        var len = Object.keys(arr).length;
        var i = 0;
        $.each(arr, function(dt, val) {
            i++;
            if (i < len*0) {
                return; // only show last 10% of testdata
            }
            trace_predic_traindata.x.push(parseDateTime_string(dt));
            trace_predic_traindata.y.push( val );

        });
        ret.push( trace_predic_traindata );
    });

    return ret;
}


function draw_predictionsChart_Exchange(data) {
    if (data['predictions'].length == 0) {
        $('#_status').text('No prediction data (yet) - try updating the datetime.');
        $("#chart img:last-child").remove();
       // Plotly.newPlot(chart, []);
        return null;
    }
    
    var ret = [];
    
    var trace_hist = {
        name: 'Price (BTC-USDT)',
        decreasing: {line: {color: '#f75656'}},
        increasing: {line: {color: '#6bf755'}}, 
        line: {color: 'rgba(31,119,180,1)'}, 
        x: [],
        low: [],
        high: [],
        open: [],
        close: [],
        type: 'candlestick', 
        xaxis: 'x', 
        yaxis: 'y',
    };
    var trace_hist_ext = {
        name: 'Price ext. (BTC-USDT)',
        decreasing: {line: {color: '#d889f9'}},
        increasing: {line: {color: '#9df989'}}, 
        line: {color: 'rgba(31,119,180,1)'}, 
        x: [],
        low: [],
        high: [],
        open: [],
        close: [],
        type: 'candlestick', 
        xaxis: 'x', 
        yaxis: 'y',
        opacity: 0.3,
    };
    var trace_vol = {
        name:'volume',
        x: [], y: [],
        type: 'scatter',
        mode:'lines+markers',
        yaxis: 'y2',
        visible: 'legendonly',
    };
    var trace_vol_ext = {
        name:'volume ext.',
        x: [], y: [],
        type: 'scatter',
        mode:'lines+markers',
        yaxis: 'y2',
        visible: 'legendonly',
    };
    setTraceVisibility(trace_hist);
    setTraceVisibility(trace_hist_ext);
    setTraceVisibility(trace_vol);
    setTraceVisibility(trace_vol_ext);

    $.each(data['history'], function(k,val) {
        var dt = parseDateTime_string(k);
        trace_hist.x.push(dt);
        trace_hist.low.push( val['low'] );
        trace_hist.high.push( val['high'] );
        trace_hist.open.push( val['open'] );
        trace_hist.close.push( val['close'] );
        
        trace_vol.x.push(dt);
        trace_vol.y.push(val['volume']);
    });

/*    trace_hist_ext.x.push( trace_hist.x[trace_hist.x.length-1] );
    trace_hist_ext.low.push( trace_hist.low[trace_hist.low.length-1] );
    trace_hist_ext.high.push( trace_hist.high[trace_hist.high.length-1] );
    trace_hist_ext.open.push( trace_hist.open[trace_hist.open.length-1] );
    trace_hist_ext.close.push( trace_hist.close[trace_hist.close.length-1] );*/

    trace_vol_ext.y.push( trace_vol.y[trace_vol.y.length-1] );

    
    $.each(data['history_extended'], function(k,val) {
        var dt = parseDateTime_string(k);
        trace_hist_ext.x.push(dt);
        trace_hist_ext.low.push( val['low'] );
        trace_hist_ext.high.push( val['high'] );
        trace_hist_ext.open.push( val['open'] );
        trace_hist_ext.close.push( val['close'] );

        trace_vol_ext.x.push(dt);
        trace_vol_ext.y.push( val['volume'] );
    });

    var opens=[], closes=[], lows=[], highs=[];
    var vols = [];
    var dts = [];
    var _init = true;
    $.each(data['predictions'], function(uid, arr) {
        var trace_predic = {
            name: '' + uid,
            decreasing: {line: {color: '#000'}},
            increasing: {line: {color: '#0c65f4'}}, 
            line: {color: 'black'}, 
            x: [],
            low: [],
            high: [],
            open: [],
            close: [],
            type: 'candlestick', 
            xaxis: 'x', 
            yaxis: 'y',

            //opacity:.15,
            visible: 'legendonly',
        };
        var trace_vol_predic = {
            name: 'vol ' + uid,
            x: [], y: [],
            type: 'scatter',
            fillcolor:'#2c7a36',
            line: {shape: 'spline', smoothing: 0, color:'#39bf4b'},
            mode:'lines+markers',
            //opacity:.15,
            
            visible: 'legendonly',
            yaxis: 'y2',
        };

        var trace_signal = {
            name: 'signal ' + uid,
            x: [], y: [],
            type: 'scatter',
            fillcolor:'purple',
            line: {shape: 'spline', smoothing: 0, color:'purple'},
            mode:'lines+markers',
            opacity:1,
            
            //visible: 'legendonly',
            yaxis: 'y2',
        };

        setTraceVisibility(trace_signal);
        setTraceVisibility(trace_predic);
        setTraceVisibility(trace_vol_predic);

        var i = 0;
        $.each(arr, function(dt,val) {
            dt = parseDateTime_string(dt);
            trace_predic.x.push(dt);
            trace_predic.low.push( val['low'] ); 
            trace_predic.high.push( val['high'] );
            trace_predic.open.push( val['open'] );
            trace_predic.close.push( val['close'] );

            trace_vol_predic.x.push(dt);
            trace_vol_predic.y.push( val['volume'] );

            trace_signal.x.push(dt);
            //trace_signal.y.push( (val['signal']<0.5?0 : (val['signal']>=2?2:1 )) );
            trace_signal.y.push( val['signal'] );

            if (_init) {
                dts.push(dt);
                lows.push(val['low']);
                highs.push(val['high']);
                opens.push(val['open']);
                closes.push(val['close']);
                vols.push(val['volume']);
            }
        });
        ret.push( trace_predic );
        ret.push( trace_vol_predic );
        ret.push(trace_signal);
        _init = false;

        if (lows.length != 0) {
            $.each(lows, function(i,_) {
                lows[i] = (lows[i]+trace_predic.low[i])/2;
                highs[i] = (highs[i]+trace_predic.high[i])/2;
                opens[i] = (opens[i]+trace_predic.open[i])/2;
                closes[i] = (closes[i]+trace_predic.close[i])/2;
                vols[i] = (vols[i]+trace_vol_predic.y[i])/2;
            });
        }
    });

    var trace_predic = {
            name: 'avg predic',
            decreasing: {line: {color: 'red'}},
            increasing: {line: {color: 'green'}}, 
            line: {color: 'black'}, 
            x: dts,
            low: lows,
            high: highs,
            open: opens,
            close: closes,
            type: 'candlestick', 
            xaxis: 'x', 
            yaxis: 'y',

            //opacity:.15,
            visible: 'legendonly',
        };
    var trace_vol_predic = {
        name: 'vol avg predic',
        x: dts, y: vols,
        type: 'scatter',
        fillcolor:'#2c7a36',
        line: {shape: 'spline', smoothing: 0, color:'#39bf4b'},
        mode:'lines+markers',
        //opacity:.15,
        
        visible: 'legendonly',
        yaxis: 'y2',
    };
    setTraceVisibility(trace_predic);
    setTraceVisibility(trace_vol_predic);
    ret.unshift( trace_predic );
    ret.unshift( trace_vol_predic );




  
    ret.unshift( trace_hist );
    ret.unshift( trace_hist_ext );
    ret.unshift( trace_vol );
    ret.unshift( trace_vol_ext );
    //ret.push( trace_predic_avg );   

    

    
    return ret;
}


function findLineByLeastSquares(values_x, values_y) {
    var sum_x = 0;
    var sum_y = 0;
    var sum_xy = 0;
    var sum_xx = 0;
    var count = 0;

    var x = 0;
    var y = 0;
    var values_length = values_x.length;

    if (values_length != values_y.length) {
        throw new Error('The parameters values_x and values_y need to have same size!');
    }

    if (values_length === 0) {
        return [ [], [] ];
    }

    for (var v = 0; v < values_length; v++) {
        x = values_x[v];
        y = values_y[v];
        sum_x += x;
        sum_y += y;
        sum_xx += x*x;
        sum_xy += x*y;
        count++;
    }

    var m = (count*sum_xy - sum_x*sum_y) / (count*sum_xx - sum_x*sum_x);
    var b = (sum_y/count) - (m*sum_x)/count;

    var result_values_x = [];
    var result_values_y = [];

    for (var v = 0; v < values_length; v++) {
        x = values_x[v];
        y = x * m + b;
        result_values_x.push(x);
        result_values_y.push(y);
    }

    return {x:result_values_x, y:result_values_y}; // output are the points of the trendline x:[...],y:[...]
}

function createTrendLine_SMA(data_y, default_size) {
    if (typeof default_size == "undefined" || default_size == null) {
        default_size=1;
    }

    sma_size = parseInt($('#_trendlinegroup').val() || default_size);
    var out = [];
    var values = [];
    $.each(data_y, function(k,y) {
        values.push(y);
        if (values.length == sma_size) {
            var sum = reduce_sum_arr(values);
            var avg = sum/values.length;
            out.push(avg);
            values.shift(); //remove first
        } else {
            out.push(NaN);
        }
    });
    return out;
}

function createTrendLine_EMA(data_y, default_size, default_recur) {
    if (typeof default_size == "undefined" || default_size == null) {
        default_size=1;
    }

    ema_size = parseInt($('#_trendlinegroup').val() || default_size);
    ema_recur = parseInt($('#_emaRecur').val() || default_recur);
    var out = EMACalc(data_y, ema_size, ema_recur);
    return out;
}

function draw_predictionsChart_mobile(data) {

    if (data['predictions'].length == 0) {
        $('#_status').text('No prediction data (yet) - try updating the datetime.');
        $("#chart img:last-child").remove();
       // Plotly.newPlot(chart, []);
        return null;
    }
    
    var ret = [];
    
    var trace_hist = {
        name: 'Price avg',
        x: [], y: [],
        type: 'scatter',
        fillcolor:'#000',
        line: {shape: 'spline', smoothing: 0, color:'#555'},
        mode:'lines+markers',
    };
    var trace_hist_ext = {
        name: 'Price avg extended',
        x: [], y: [],
        type: 'scatter',
        fillcolor:'#333',
        opacity:.5,
        line: {shape: 'spline', smoothing: 0, color:'#555'},
        mode:'lines+markers',
    };
    setTraceVisibility(trace_hist);
    setTraceVisibility(trace_hist_ext);
    $.each(data['history'], function(k,val) {
        var dt = parseDateTime_string(k);
        trace_hist.x.push(dt);
        trace_hist.y.push( val );
    });

    trace_hist_ext.x.push( trace_hist.x[trace_hist.x.length-1] );
    trace_hist_ext.y.push( trace_hist.y[trace_hist.y.length-1] );
    $.each(data['history_extended'], function(k,val) {
        var dt = parseDateTime_string(k);
        trace_hist_ext.x.push(dt);
        trace_hist_ext.y.push( val );
    });


    trace_hist.x = trace_hist.x.slice(-5);
    trace_hist.y = trace_hist.y.slice(-5);

    
    var smaprice = create_trace_sma_draw_predictionsChart(data['history'], 'EMA(Price avg)');
    var sma_price_tail = smaprice.y[ smaprice.y.length -1 ];
    var trace_largest = null;
    var trace_smallest = null;

    var trace_i = 0;
    $.each(data['predictions'], function(uid, arr) {
        var trace_predic = {
            x: [], y: [],
            type: 'scatter',
            fillcolor:'#973d3d',
            line: {shape: 'spline', smoothing: 0, color:'#5f1414'},
            mode:'lines+markers',
            opacity:.15,
            
            'legendgroup': 'Predictions',
            'name': 'Predictions',
            'showlegend': false,
            visible: 'legendonly',
        };
        if (trace_i++ == 0) {
            trace_predic['showlegend'] = true;
        }
        setTraceVisibility(trace_predic);

        var i = 0;
        $.each(arr, function(dt,val) {
            trace_predic.x.push(parseDateTime_string(dt));
            trace_predic.y.push( val );
        });
        if (trace_largest == null || reduce_sum_arr(trace_predic.y) > reduce_sum_arr(trace_largest.y)) {
            trace_largest = trace_predic;
        }
        if (trace_smallest == null || reduce_sum_arr(trace_predic.y) < reduce_sum_arr(trace_smallest.y)) {
            trace_smallest = trace_predic;
        }
        ret.push( trace_predic );
    });

    // SMA(price avg + min(prediction))
    var head = {};
    for (var i = 0; i < trace_smallest.y.length; i++) {
        head[ localToUTC_string(trace_smallest.x[i], "YYYY-MM-DDTHH:mm") ] = trace_smallest.y[i];
    }
    var smaprice_extended_min = create_trace_sma_draw_predictionsChart(head, 'min');
    /*for (var key = 0; key < Object.keys(data['history']).length; key++) {
        smaprice_extended_min.y[key] = NaN;
    }*/
    
    
    // SMA(price avg + max(prediction))
    var head = {};
    for (var i = 0; i < trace_largest.y.length; i++) {
        head[ localToUTC_string(trace_largest.x[i], "YYYY-MM-DDTHH:mm") ] = trace_largest.y[i];
    }

    var smaprice_extended_max = create_trace_sma_draw_predictionsChart(head, 'max');
    /*for (var key = 0; key < Object.keys(data['history']).length; key++) {
        smaprice_extended_max.y[key] = NaN;
    }*/


    // average prediction:
    predictions_avg = { x:[], y:[] };
    $.each(data['predictions'], function(uid, arr) {
        var i = 0;
        $.each(arr, function(dt,val) {
            if (predictions_avg.x[i] == undefined) {
                predictions_avg.x[i] = parseDateTime_string( dt );
                predictions_avg.y[i] = [];
            }
            predictions_avg.y[i].push(val);
            ++i;
        });
    });
    
    $.each(predictions_avg.y, function(idx, arr) {
        var sum = reduce_sum_arr(arr);
        predictions_avg.y[idx] = sum/arr.length;
    });
    var trace_predic_avg = {
        name: 'Predicted price avg.',
        x: predictions_avg.x.slice(),
        y: predictions_avg.y.slice(),
        type: 'scatter',
        fillcolor:'red',
        line: {shape: 'spline', smoothing: 0, color:'red'},
        mode:'lines+markers',
        opacity:.6,
        visible: 'legendonly',
    };
    setTraceVisibility(trace_predic_avg);
    

    // SMA(Price avg + avg(prediction))
    var head = {};
    for (var i = 0; i < trace_predic_avg.y.length; i++) {
        head[ localToUTC_string(trace_predic_avg.x[i], "YYYY-MM-DDTHH:mm") ] = trace_predic_avg.y[i];
    }
    var smaprice_extended_avg = create_trace_sma_draw_predictionsChart(head, 'avg');


    ret.unshift( trace_hist );
    ret.unshift( smaprice_extended_max);
    ret.unshift( smaprice_extended_avg);
    ret.unshift( smaprice_extended_min);
    ret.unshift( trace_hist_ext );
    
    ret.push( trace_predic_avg );   

    return ret;
}


function draw_mobile_app_chart_price() {
    var trace_h = {
        label : "Actual price (USD)",
        data : [],
        color: "#000",
        lines : {
            show : true,
        },
        points : {
            show : true,
        }
    };
    var ticks = [];

    var i = 1;
    $.each(DATA, function(label, obj) {
        trace_h.data.push([i, obj['price-avg']]);
        ticks.push([i, parseDateTime_dt(label).format("HH:mm")  ]);
        i++;
    });

    $.each(ticks, function(i, t) {
        if (i%2!=0) {
            ticks[i] = "";
        }
    });
    
    
    
    var data = [trace_h];
    var options = {
        series : {
            shadowSize : 0
        },
        grid : {
            hoverable : true,
            clickable : true,
            tickColor : "#f9f9f9",
            borderWidth : 1,
            borderColor : "#eeeeee"
        },
        colors : ["#6e8cd7", "#34d3eb", "#5fbeaa"],
        tooltip : true,
        tooltipOpts : {
            defaultTheme : false
        },
        legend : {
            position : "ne",
            margin : [0, -24],
            noColumns : 0,
            labelBoxBorderColor : null,
            labelFormatter : function(label, series) {
                // just add some space to labes
                return '' + label + '&nbsp;&nbsp;';
            },
            width : 30,
            height : 2
        },
        yaxis : {
            tickColor : '#f5f5f5',
            font : {
                color : '#bdbdbd'
            }
        },
        xaxis : {
            ticks: ticks,
            tickColor : '#f5f5f5',
            font : {
                color : '#bdbdbd'
            }
        }
    };

    $.plot($("#chart"), data, options);

    $("#chart").css({
        height: window.innerHeight * .6,
    });
}

function draw_exchangeVolume(data) {

    var trace = {
        name: 'EMA(volume)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        visible: 'legendonly',
        isTrend: draw_exchangeVolume,
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        var v = val['volume'];
        trace.y.push( v );
    });
    normalize_max(trace.y);

    trace.y = createTrendLine_EMA(trace.y);

    return [trace];
}
function draw_exchangeTrades(data) {

    var trace = {
        name: 'EMA(trades)',
        x: [], y: [],
        type: 'scatter',
        yaxis: 'y2',
        visible: 'legendonly',
        isTrend: draw_exchangeTrades,
    };
    setTraceVisibility(trace);

    var min = null, max = null;
    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);

        var v = val['trades'];
        if (min == null || v < min) {
            min = v;
        }
        if (max == null || v > max) {
            max = v;
        }
        
        trace.y.push( v );
    
    });

    $.each(trace.y, function(k,val) {
        trace.y[k] = trace.y[k]/max*100;
    });
    normalize_max(trace.y);

    trace.y = createTrendLine_EMA(trace.y);

    return [trace];
}

function EMACalc(mArray, mRange, times) {
    mArray = mArray.slice();
    for (var j = 0; j < times; j++) {
        $.each(mArray, function(i, v) {
            if (isNaN(v)) {
                mArray[i] = 0;
            }
        });
        var k = (2.0/(mRange + 1.0));
        emaArray = [mArray[0]];
        var v;
        for (var i = 1; i < mArray.length; i++) {
            v = (mArray[i] * k) + (emaArray[i - 1] * (1 - k));
            emaArray.push(v);
        }
        mArray = emaArray.slice();
    }

    return mArray;
}

function make_EMA_trace(data, size) {
    var trace = {
        name: 'MACD ' + size,
        x: [],
        y: [],
        type: 'scatter',
        yaxis: 'y', // y2
        visible: 'legendonly',
    };
    setTraceVisibility(trace);
    
    var min = null, max = null;
    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);

        //var v = val['close'];
        //var v = val['open'];
        var v = (val['open']+val['close'])/2;
        //var v = (val['high']+val['open']+val['low'])/3;
        
        if (max == null || v > max) { max = v; }
        if (min == null || v < min) { min = v; }
        
        trace.y.push( v );
    });
    trace.y = EMACalc(trace.y, size, 1);

    $.each(trace.y, function(k,val) {
        //trace.y[k] = (trace.y[k]-min)/(max-min)*100;
        //don't normalize, otherwise if we change "history mins" size, it will give us different results because histogram values are different (and we use histogram values as is)
    });

    return trace;
}

function draw_MACDs(data) {
    var ret = [];

    var ema0 = make_EMA_trace(data, 2);
    var ema1 = make_EMA_trace(data, 9);
    var ema2 = make_EMA_trace(data, 24);

    ret.push(ema0);
    ret.push(ema1);
    ret.push(ema2);

    var histogram = [];
    var min=null,max = null;
    $.each(ema1.y, function(i, _) {
        var v = (ema1.y[i]-ema2.y[i]);
        histogram.push(v);
        if (max == null || v > max) { max = v; }
        if (min == null || v < min) { min = v; }
    });
    $.each(histogram, function(i, v) {
        // don't normalize 
        //histogram[i] = (histogram[i]-min)/(max-min)
    });
    //histogram = EMACalc(histogram, 7, 3);

    var trace = {
        name: 'histogram',
        x: ret[0].x,
        y: histogram,
        type: 'bar',
        yaxis: 'y2',
        opacity:0.5,
    };
    ret.unshift(trace);
    setTraceVisibility(trace);
    
    
    return ret;
}

function draw_exchangeCandles(data) {

    var trace = {
        name: 'Price (BTC-USDT)',
        decreasing: {line: {color: '#f75656'}},
        increasing: {line: {color: '#6bf755'}}, 
        line: {color: 'rgba(31,119,180,1)'}, 
        x: [],
        low: [],
        high: [],
        open: [],
        close: [],
        type: 'candlestick', 
        xaxis: 'x', 
        yaxis: 'y',
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);
        
        trace.low.push( val['low'] );
        trace.high.push( val['high'] );
        trace.open.push( val['open'] );
        trace.close.push( val['close'] );
    
    });


    

    return [trace];
}

function draw_exchangeOC(data) {
    var trace_OC = {
        name: 'OC',
        x: [],
        y: [],
        type: 'scatter',
        yaxis: 'y', // y2
        visible: 'legendonly',
    };
    setTraceVisibility(trace_OC);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace_OC.x.push(dt);  
        trace_OC.y.push( (val['open']+val['close'])/2 );
    });
    // normalize_max(trace_OC.y);
    //trace_OC.y = createTrendLine_EMA(trace_OC.y);

    return [trace_OC];
}

function draw_exchangeOC_testA(data) {
    var trace_OC = {
        name: 'OC testA',
        x: [],
        y: [],
        type: 'scatter',
        yaxis: 'y2', 
        //visible: 'legendonly',
    };
    setTraceVisibility(trace_OC);

    prev = [];
    prev_len = 8;
    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace_OC.x.push(dt);  
        
        var price = (val['open']+val['close'])/2;
        if (prev.length > 0) {
            var x = price- average(prev);
            //x = (x < 0 ? -1 : 1) * Math.log(Math.abs(x)) // prev_len = 4
            //x = (x < 0 ? -1 : 1) * Math.cosh(Math.log(Math.abs(x))) // prev_len = 4
   
            // prev_len = 8
            var z = 0;
            for (var i = 1; i < prev_len; i++) {
                var u = EMACalc(prev, i, Math.round(1+i/2))
                z += average(u)
            }
            x = (x < 0 ? -1 : 1) * Math.log(Math.abs(z/prev_len))
            x = (x < 0 ? -2 : 2)

            trace_OC.y.push(x)
        } else {
            trace_OC.y.push(NaN);
        }
        prev.push(price)
        if (prev.length > prev_len) prev.shift()

    });
    // normalize_max(trace_OC.y);
    //trace_OC.y = createTrendLine_EMA(trace_OC.y);


    return [trace_OC];

}
function draw_exchangeOC_testB(data) {
    var trace_OC = {
        name: 'OC testB',
        x: [],
        y: [],
        type: 'scatter',
        yaxis: 'y2', 
        //visible: 'legendonly',
    };
    setTraceVisibility(trace_OC);

    prev = [];
    prev_len = 4;
    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace_OC.x.push(dt);  
        
        var price = (val['open']+val['close'])/2;
        if (prev.length > 0) {
            var x = price- average(prev);
            //x = (x < 0 ? -1 : 1) * Math.log(Math.abs(x)) // prev_len = 4
            //x = (x < 0 ? -1 : 1) * Math.cosh(Math.log(Math.abs(x))) // prev_len = 4
            
            
            // prev_len = 4
            var z = 0;
            for (var i = 1; i < 10; i++) {
                var u = EMACalc(prev, i, 1+i/2)
                z += average(u)
            }
            x = (x < 0 ? -1 : 1) * Math.log(Math.abs(z/10))
            x = (x < 0 ? -1 : 1)


            
            trace_OC.y.push(x)
        } else {
            trace_OC.y.push(NaN);
        }
        prev.push(price)
        if (prev.length > prev_len) prev.shift()

    });
    // normalize_max(trace_OC.y);
    //trace_OC.y = createTrendLine_EMA(trace_OC.y);


    return [trace_OC];

}

function draw_exchangeOC_trend(data) {
    var trace_OC = {
        name: 'EMA(OC)',
        x: [],
        y: [],
        type: 'scatter',
        yaxis: 'y', // y2
        visible: 'legendonly',
        isTrend: draw_exchangeOC_trend,
    };
    setTraceVisibility(trace_OC);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace_OC.x.push(dt);  
        trace_OC.y.push( (val['open']+val['close'])/2 );
    });
    // normalize_max(trace_OC.y);
    trace_OC.y = createTrendLine_EMA(trace_OC.y);

    return [trace_OC];

}
function draw_exchangeOHLC(data) {
    var trace = {
        name: 'EMA(OHLC)',
        x: [],
        y: [],
        type: 'scatter',
        yaxis: 'y', // y2
        visible: 'legendonly',
        isTrend: draw_exchangeOC,
    };
    setTraceVisibility(trace);

    $.each(data, function(k,val) {
        var dt = parseDateTime_string(k);
        trace.x.push(dt);  
        trace.y.push( (val['open']+val['close']+val['low']+val['high'])/4 );
    });
    // normalize_max(trace.y);
    trace.y = createTrendLine_EMA(trace.y);

    return [trace];

}


function standardDeviation(values){
    var avg = average(values);

    var squareDiffs = values.map(function(value){
    var diff = value - avg;
    var sqrDiff = diff * diff;
        return sqrDiff;
    });

    var avgSquareDiff = average(squareDiffs);

    var stdDev = Math.sqrt(avgSquareDiff);
    return stdDev;
}
function average(data){
    var tot = 0;
    var len = 0;
    $.each(data, function(k, v) {
        if (!isNaN(v)) { // we ignore NaN values
            tot += v;
            len++;
        }
    });

    return tot/len;
}

function normalize_max(data) {
    var min = null, max = null;
    $.each(data, function(k,val) {
        if (isNaN(val)) {
            return;
        }
        val = Math.abs(val);
        if (min == null || val < min) {
            min = val;
        }
        if (max == null || val > max) {
            max = val;
        }
    });
    $.each(data, function(k,val) {
        data[k] = data[k]/max*100;
    });
}

function generate_exchangeAnnotations_socialSentiments(prices, OCs, sentiments) {
    var ret = [];
    var ann_template = {
        x: null, //parseDateTime_string('2018-03-13T13:00'),
        y: null,
        xref: 'x',
        yref: 'paper',
        text: 'buy',
        font: {color: 'magenta'},
        showarrow: true,
        ax: 0,
        ay: 30
    };

    function addAnnon(ret, ann_template, text, dt, yStart, color) {
        var ann = Object.assign({}, ann_template);
        ann.text=text;
        ann.x = dt;
        ann.y = yStart;
        ann.font = {color: ''+color};
        ret.push(ann);
    }

    function isIncreasingArrStrict(arr, from, to) {
        for (var i = from+1; i <= to; i++) {
            if (arr[i] < arr[i-1]) {
                return false;
            }
        }
        return true;
    }
    function isDecreasingArrStrict(arr, from, to) {
        for (var i = from+1; i <= to; i++) {
            if (arr[i] > arr[i-1]) {
                return false;
            }
        }
        return true;
    }

    function isRangeStrictlyPositive(arr, from, to) {
        for (var i = from; i <= to; i++) {
            if (arr[i] < 0) {
                return false;
            }
        }
        return true;
    }
    function isRangeStrictlyNegative(arr, from, to) {
        for (var i = from; i <= to; i++) {
            if (arr[i] > 0) {
                return false;
            }
        }
        return true;
    }

    
   
    var harr = [];
    var hlen = 3;
    var portfolio = [];
    var canBuy = true, calSell = false;;
    $.each(prices.low, function(k,hval) {
        var dt = parseDateTime_string( prices.x[k] );

        var price = (prices.open[k]+prices.close[k])/2 ;
        var prevPrice = (prices.open[k-1]+prices.close[k-1])/2 ;
        
        var lxA = 8, lxB = 11, lxC = 11, lxD = 10;
        /*console.log(sentiments.y.slice(k-lxA, k))
        console.log(OCs.y.slice(k-lxB, k))*/
        if (calSell && isIncreasingArrStrict(sentiments.y, k-lxA-1, k-1) && isIncreasingArrStrict(OCs.y, k-lxB-1, k-1)
            && !isIncreasingArrStrict(sentiments.y, k-lxA, k) && isIncreasingArrStrict(OCs.y, k-lxB, k)) {
            addAnnon(ret, ann_template, 'S', prices.x[k], 0.99, 'black');
            portfolio.push({'type':'sell', 'price':price });
            canBuy = true;
            calSell = false;
        }

        /*console.log(sentiments.y.slice(k-lxC, k))
        console.log(OCs.y.slice(k-lxD, k))*/
        if (canBuy && isDecreasingArrStrict(sentiments.y, k-lxC, k) && isDecreasingArrStrict(OCs.y, k-lxD, k)) {
            addAnnon(ret, ann_template, 'B', prices.x[k], 0.99, 'black');
            portfolio.push({'type':'buy', 'price':price });
            canBuy = false;
            calSell = true;
        }
        
        console.log("");
    });

    console.log(portfolio);

    
    /*var price = (prices.open[prices.open.length-1]+prices.close[prices.close.length-1])/2 ;
    addAnnon(ret, ann_template, '*S*', prices.x[prices.x.length-1], 1.1, 'black');
    portfolio.push({'type':'sell', 'price':price });*/
    processPortfolio(portfolio, 0.001, 1 , 1);

    return ret;
}

function generate_exchangeAnnotations_hypoB_1(prices, OCtrend) {
    var ret = [];
    var ann_template = {
        x: null, //parseDateTime_string('2018-03-13T13:00'),
        y: null,
        xref: 'x',
        yref: 'y', // paper
        text: 'buy',
        font: {color: 'magenta'},
        showarrow: true,
        ax: 0,
        ay: 30
    };

     function addAnnon(ret, ann_template, text, dt, yStart, color) {
        var ann = Object.assign({}, ann_template);
        ann.text=text;
        ann.x = dt;
        ann.y = yStart;
        ann.font = {color: ''+color};
        ret.push(ann);
    }

    function isUpTrend(arr, start, end) {
        return start >= 0 && end > start && arr[end] > arr[start]
    }

    var portfolio = []
    var bucket = {dt: null, arr: []}
    var canBuy = true;
    var canSell = false;
    $.each(prices.low, function(k,hval) {
        if (k == 0) return;

        var dt = parseDateTime_string( prices.x[k] );

        var open = prices.open[k];
        var openPrev = prices.open[k-1];
        var close = prices.close[k];
        var closePrev = prices.close[k-1];

        var price = (open+close)/2;
        var pricePrev = (openPrev+closePrev)/2;

        //var price = open+(close-open)*0.2
        //var pricePrev = (openPrev+closePrev)/2



        if (price >= pricePrev) {
            //if (isUpTrend(OCtrend.y, k-5, k)) {
                var slope = ( (price-pricePrev)/pricePrev * 100);
                if (bucket.dt==null) bucket.dt = dt;
                bucket['arr'].push(slope)

                /*
                    107+ % 30min intervals, arr.length==2 ; slope>=0
                    107+ % 60min intervals
                    108+ % 60min intervals; slope >= 0; arr.len >= 1

                */
                // buy
                console.log(slope)
                if (        canBuy
                        &&  slope >= 0.25
                        //&&  bucket.arr.length >= 1
                    ) {
                    //addAnnon(ret, ann_template, 'B', prices.x[k], 0.99, 'black');
                addAnnon(ret, ann_template, 'B', prices.x[k], price, 'black');
                    canBuy = false;
                    canSell = true;
                    portfolio.push({'type':'buy', 'price':price });
                }
            //}
        } else {
            if (canSell) {
                // sell
                //addAnnon(ret, ann_template, 'S', prices.x[k], 0.99, 'black');
                addAnnon(ret, ann_template, 'S', prices.x[k], price, 'black');
                canBuy = true;
                canSell = false;
                portfolio.push({'type':'sell', 'price':price });
                bucket = {dt: null, arr: []}
            }
        }
        
        
        /*addAnnon(ret, ann_template, 'B', prices.x[k], 0.99, 'black');
        portfolio.push({'type':'sell', 'price':price });
        portfolio.push({'type':'buy', 'price':price });*/
    });

    //console.log(portfolio);
    processPortfolio(portfolio, 0.001, 1 , 1);
    console.log(ret)

    return ret;
}

function generate_exchangeAnnotations_hypoB_2(prices, OCtrend) {
    var ret = [];
    var ann_template = {
        x: null, //parseDateTime_string('2018-03-13T13:00'),
        y: null,
        xref: 'x',
        yref: 'paper',
        text: 'buy',
        font: {color: 'magenta'},
        showarrow: true,
        ax: 0,
        ay: 30
    };

    function addAnnon(ret, ann_template, text, dt, yStart, color) {
        var ann = Object.assign({}, ann_template);
        ann.text=text;
        ann.x = dt;
        ann.y = yStart;
        ann.font = {color: ''+color};
        ret.push(ann);
    }

    var portfolio = []
    var bucket = {dt: null, arr: []}
    var canBuy = true;
    var canSell = false;
    var buyPrice = null;
    $.each(prices.low, function(k,hval) {
        if (k == 0) return;

        var dt = parseDateTime_string( prices.x[k] );

        var open = prices.open[k];
        var openPrev = prices.open[k-1];
        var close = prices.close[k];
        var closePrev = prices.close[k-1];

        var price = (open+close)/2;
        var pricePrev = (openPrev+closePrev)/2;
        //var price = open+(close-open)*0.3
        //var pricePrev = (openPrev+closePrev)/2

        var slope = ( (price-pricePrev)/pricePrev * 100);
        if (bucket.dt==null) bucket.dt = dt;
        bucket['arr'].push(slope)

        if (        canBuy
                &&  (OCtrend.y[k] < price && OCtrend.y[k-1] > pricePrev)
            ) {
            addAnnon(ret, ann_template, 'B', prices.x[k], 0.99, 'black');
            canBuy = false;
            canSell = true;
            buyPrice = price;
            portfolio.push({'type':'buy', 'price':price });
        }
        else if (       canSell
                    &&  (
                            // (OCtrend.y[k] > price && OCtrend.y[k-1] < pricePrev)
                            // ||
                            price/buyPrice > 1.01
                            ||
                            price/buyPrice < 0.98
                        )
            ) {
            addAnnon(ret, ann_template, 'S', prices.x[k], 0.99, 'black');
            canBuy = true;
            canSell = false;
            portfolio.push({'type':'sell', 'price':price });
            bucket = {dt: null, arr: []}
        }

    });

    //console.log(portfolio);
    processPortfolio(portfolio, 0.001, 1 , 1);
    console.log(ret)

    return ret;
}



function processPortfolio(portfolio, fee, buyRate, sellRate) {
    var cashStart = 10000;
    var cash = cashStart;
    var crypto = 0;


    while (portfolio.length > 0) {
        var i = portfolio.length -1;
        if (portfolio[i]['type'] == 'buy') {
            portfolio.splice(i, 1);
        } else {
            break;
        }
    }
    console.log(portfolio);

    $.each(portfolio, function(idx, obj) {
        if (obj.type == 'buy') {
            if (cash > 0) {
                crypto_x = cash * buyRate / obj.price
                crypto += crypto_x * (1-fee)
                cash -= cash * buyRate
            }

        } else if (obj.type == 'sell') {
            if (crypto > 0) {
                cash_x = crypto * sellRate * obj.price
                cash += cash_x * (1-fee)
                crypto -= crypto * sellRate
            }
        }
    });
    if (crypto > 0) { // sell what's left using last available price
        var obj = portfolio[portfolio.length-1];
        cash_x = crypto * 1 * obj.price
        cash += cash_x * (1-fee)
        crypto -= crypto * 1
    }
    console.log("cash: " + cash);
    console.log("crypto: " + crypto);
    console.log("ROI:" + (((cash/cashStart)-1)*100).toFixed(4) + "%" );
}

function generate_exchangeAnnotations_AI(data) {
    var ret = [];
    var ann_template = {
        x: null, //parseDateTime_string('2018-03-13T13:00'),
        y: null,
        xref: 'x',
        yref: 'paper',
        text: 'buy',
        font: {color: 'magenta'},
        showarrow: true,
        ax: 0,
        ay: 30
    };

    function addAnnonInfo(ret, ann_template, latest, mean, std, dt, yStart, color) {
        var ann = Object.assign({}, ann_template);
        ann.text=(latest < mean ?'-':'')+Math.round(Math.abs(latest-mean)/std);
        ann.x = dt;
        ann.y = yStart ;//(latest < mean ? -.01 : .01);
        ann.font = {color: ''+color};
        ret.push(ann);
    }
    function addAnnonAction(ret, ann_template, text, dt) {
        var ann = Object.assign({}, ann_template);
        ann.text=text;
        ann.x = dt;
        ann.y = .1;
        ret.push(ann);
    }

    data = Object.keys(data).map(function(key) {
        data[key]['label'] = key;
        return data[key];
    });
    
    
    for(var i = 0; i < data.length; i++) {
        console.log("i: " + i);
        var k = data[i]["label"];
        var val = data[i];

        var dt = parseDateTime_string(k);
        var price = (val['open'] + val['close'])/2 ;
        //console.log(price);
        

        var largestPriceFuture = null;
        var largestJ = 0;
        for (var j = i+1; j < data.length && j <= i+10; j++) {
            kFuture = data[j]["label"];
            valFuture = data[j];

            dtFuture = parseDateTime_string(kFuture);
            priceFuture = (valFuture['open'] + valFuture['close'])/2 ;
            // console.log(priceFuture);

            if (priceFuture >= price * 1.005) {
                if (largestPriceFuture == null || priceFuture > largestPriceFuture) {
                    largestPriceFuture = priceFuture;
                    largestJ = j;
                }
            }
        }
        if (largestJ > 0) {
            console.log("buy: " + k + "\t" + price)
            console.log("sell: " + data[largestJ]['label'] + "\t" + largestPriceFuture);
            i = largestJ;
            console.log("largestJ: " + largestJ);

            addAnnonAction(ret, ann_template, "B", dt);
            addAnnonAction(ret, ann_template, "S", parseDateTime_string(data[largestJ]['label']));
        }
        

    }

    // addAnnonInfo(ret, ann_template, latestPrice, meanPrice, stdPrice, dt, 1.1, 'black');
    // addAnnonAction(ret, ann_template, "S", dt);
    return ret;
}