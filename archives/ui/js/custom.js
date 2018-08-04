

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
        var qry = {
            //'base_cur': -1,
            'base_cur': $('#_base').val(), 
            'interval':$('#_interval').val(), 
            'currentDateTime': label.replace(' ', 'T')
        };
        $.getJSON('https://cryptopredicted.com/PWA/api/extended/social/', qry, function (data, status) {
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
        $.getJSON('https://cryptopredicted.com/PWA/api/extended/news/', qry, function (data, status) {
            var html = "<h2>News headlines:</h2>";
            for (var k in data) {
                var d = data[k];
                var str = d['title'];
                console.log(d);
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
