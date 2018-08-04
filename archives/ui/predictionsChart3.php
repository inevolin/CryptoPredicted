<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Using machine learning and big data we are able to analyze cryptocurrencies and make short-term predictions. This allows us to make better investing decisions in a highly uncertain crypto world.">
        <meta name="author" content="Ilya Nevolin">

        <link rel="shortcut icon" href="assets/images/fav.ico">

        <title>CryptoAnalysis | Predicting crypto prices using AI and big data</title>

        <link href="assets/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
        <link href="assets/css/icons.css" rel="stylesheet" type="text/css" />
        <link href="assets/css/style.css" rel="stylesheet" type="text/css" />

        <script src="assets/js/modernizr.min.js"></script>

        <style>
            html {
                overflow-y: scroll;
            }
        </style>


    </head>


    <body class="fixed-left">

        <!-- Begin page -->
        <div id="wrapper">

            <?php include_once('header.php'); ?>

            <?php include_once('sidebar.php'); ?>




            <!-- ============================================================== -->
            <!-- Start right Content here -->
            <!-- ============================================================== -->
            <div class="content-page">
                <!-- Start content -->
                <div class="content">
                    <div class="container-fluid">
                        <div class="row">
                            
                            <div class="col-sm-12 card-box">
                                <div class="row">
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Crypto:</b></h4>
                                        <select class="form-control" id="_crypto">
                                            <option value="BTC" selected="">Bitcoin (BTC)</option>
                                            <option value="ETH">Ethereum (ETH)</option>
                                            <!--
                                            <option value="LTC">Litecoin (LTC)</option>
                                            <option value="DASH">DigitalCash (DASH)</option>
                                            <option value="XMR">Monero (XMR)</option>
                                            <option value="NXT">NXT</option>
                                            <option value="ZEC">ZCash (ZEC)</option>
                                            <option value="DGB">DigiByte (DGB)</option>
                                            <option value="XRP">Ripple (XRP)</option>
                                            <option value="EOS">EOS</option>

                                            <option value="BCH">Bitcoin Cash (BCH)</option>
                                            <option value="ETC">Ethereum Classic (ETC)</option>
                                            <option value="IOT">IOTA</option>
                                            <option value="XLM">Stellar (XLM)</option>
                                            <option value="NEO">NEO</option>
                                            <option value="DOGE">Doge</option>
                                            <option value="TRX">Tronix (TRX)</option>
                                            <option value="ADA">Cardano (ADA)</option>
                                            <option value="OMG">OmiseGo (OMG)</option> -->
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Interval:</b></h4>
                                        <select class="form-control" id="_interval">
                                            <option value="10" selected>10min</option>
                                            <option value="60">1h</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>History size:</b></h4>
                                        <select class="form-control" id="_historymins">
                                            <option value="60">1h</option>
                                            <option value="120">2h</option>
                                            <option value="180" selected>3h</option>
                                            <option value="360">6h</option>
                                            <option value="720">12h</option>
                                            <option value="1440">1 day</option>
                                            <option value="2880">2d</option>
                                            <option value="4320">3d</option>
                                            <option value="5760">4d</option>
                                            <option value="7200">5d</option>
                                            <option value="8640">6d</option>
                                            <option value="10080">7d</option>
                                            <option value="11520">8d</option>
                                            <option value="12960">9d</option>
                                            <option value="14400">10d</option>
                                            <option value="15840">11d</option>
                                            <option value="17280">12d</option>
                                            <option value="18720">13d</option>
                                            <option value="20160">14d</option>
                                            <option value="28800">20d</option>
                                            <option value="57600">40d</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Datetime:</b></h4>
                                        <input class="form-control" type="text" id="_datepicker">
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>features type:</b></h4>
                                        <select class="form-control" id="_featuresID">
                                            <option value="-1" selected>all</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Batch size:</b></h4>
                                        <select class="form-control" id="_batchsize">
                                            <option value="256">256</option>
                                            <option value="512">512</option>
                                            <option value="-1" selected>all</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>neurons:</b></h4>
                                        <select class="form-control" id="_neurons">
                                            <option value="2">2</option>
                                            <option value="4">4</option>
                                            <option value="-1" selected>all</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>hidden layers:</b></h4>
                                        <select class="form-control" id="_hiddenlay">
                                            <option value="1">1</option>
                                            <option value="-1" selected>all</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>sequence size:</b></h4>
                                        <select class="form-control" id="_windowsize">
                                            <option value="8">8</option>
                                            <option value="-1" selected>all</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>epochs:</b></h4>
                                        <input class="form-control" id="_epochs" value="1000" disabled>
                                    </div>
                                    <div class="col-sm-1">
                                        <button class="btn btn-success waves-effect waves-light m-t-20" onclick="requestAndDraw()">Generate</button>
                                    </div>
                                    <div class="col-sm-2">
                                        <button class="btn btn-success waves-effect waves-light m-t-20" onclick="prev()">prev</button>
                                        <button class="btn btn-success waves-effect waves-light m-t-20" onclick="next()">next</button>
                                    </div>
                                </div>
                                <div class="row m-t-10">
                                    <div class="col-sm-12">
                                        <span id="_status"></span>
                                    </div>
                                </div>
                                <div class="row m-t-10">
                                    <div id="chart" style="min-height:100px;"></div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Moving average size:</b></h4>
                                        <select id="_trendlinegroup" class="form-control" >
                                            <option value="1" selected>original</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                            <option value="4">4</option>
                                            <option value="5">5</option>
                                            <option value="6">6</option>
                                            <option value="7">7</option>
                                            <option value="8">8</option>
                                            <option value="9">9</option>
                                            <option value="10">10</option>
                                            <option value="11">11</option>
                                            <option value="12">12</option>
                                            <option value="13">13</option>
                                            <option value="14">14</option>
                                            <option value="15">15</option>
                                            <option value="16">16</option>
                                            <option value="17">17</option>
                                            <option value="18">18</option>
                                            <option value="19">19</option>
                                            <option value="20">20</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>

                        

                        <div class="row">
                            <div class="col-sm-12 card-box">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <p>
                                            For more information about this tool and settings please read <a href="https://medium.com/@cryptopredicted/improving-our-autopilot-crypto-predictions-system-41360a82484b" target="_blank">this</a> 
                                            and <a href="https://medium.com/@cryptopredicted/the-analysis-of-our-autopilot-system-for-predicting-crypto-prices-part-1-bd31429d1a17" target="_blank">this</a>.
                                            
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                            
                        

                    </div> <!-- container -->

                </div> <!-- content -->

                <?php include_once('footer.php'); ?>

            </div>


            <!-- ============================================================== -->
            <!-- End Right content here -->
            <!-- ============================================================== -->


        </div>
        <!-- END wrapper -->



        <script>
            var resizefunc = [];
        </script>

        <!-- jQuery  -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/popper.min.js"></script><!-- Popper for Bootstrap -->
        <script src="assets/js/bootstrap.min.js"></script>
        <script src="assets/js/detect.js"></script>
        <script src="assets/js/fastclick.js"></script>
        <script src="assets/js/jquery.slimscroll.js"></script>
        <script src="assets/js/jquery.blockUI.js"></script>
        <script src="assets/js/waves.js"></script>
        <script src="assets/js/wow.min.js"></script>
        <script src="assets/js/jquery.nicescroll.js"></script>
        <script src="assets/js/jquery.scrollTo.min.js"></script>

        <script src="./plugins/peity/jquery.peity.min.js"></script>


        <!-- datepicker -->
        <script src="js/plotly-latest.min.js"></script>
        <script src="js/jquery.datetimepicker.full.min.js"></script>
        <script src="js/moment.js"></script>
        <script src="js/moment-timezone.js"></script>
        <script src="js/moment-timezone-with-data-2012-2022.js"></script>
        <link rel="stylesheet" href="css/jquery.datetimepicker.min.css">

        <!-- jQuery  -->

        <script src="assets/js/jquery.core.js"></script>
        <script src="assets/js/jquery.app.js"></script>


        <!-- custom -->
        <script src="js/custom.js?random=<?php echo filemtime("js/custom.js"); ?>"></script>
        <script>
            function drawGraphs() {
                data = [];

                console.log(DATA);
                _price = draw_predictionsChart(DATA);
                if (_price == null) {
                    return null;
                }

                $.each(_price, function(idx, a) {
                    data = data.concat(a);
                });


                var WIDTH_IN_PERCENT_OF_PARENT = 100,    HEIGHT_IN_PERCENT_OF_PARENT = 70;
                $("#chart").css({
                    width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                    height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
                });
                
                window.onresize = function() {
                    Plotly.Plots.resize('chart');
                };

                console.log( );
                var layout = {
                    /*plot_bgcolor: 'rgba(0,0,0,0)',
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    font: {
                        color: '#fff',
                    },*/
                    dragmode:'pan',
                    legend: { },
                    xaxis: {
                        type: 'date',
                    },
                    yaxis: {
                        title: 'Price (USD)',
                        showgrid:false,
                    },

                    annotations: [],
                };

                $.each(DATA['_buys'], function(i, val) {
                    var ann = {
                        x: ( val ),
                        y: 0.99,
                        xref: 'x',
                        yref: 'paper',
                        text: 'buy',
                        font: {color: 'magenta'},
                        showarrow: true,
                        ax: 0,
                        ay: 30
                    };
                    layout.annotations.push(ann);
                });
                $.each(DATA['_sells'], function(i, val) {
                    var ann = {
                        x: ( val ),
                        y: 0.99,
                        xref: 'x',
                        yref: 'paper',
                        text: 'sell',
                        font: {color: 'magenta'},
                        showarrow: true,
                        ax: 0,
                        ay: -30
                    };
                    layout.annotations.push(ann);
                });

                Plotly.newPlot('chart', data, layout, {scrollZoom: true});
            }
            function requestAndDraw() {
                $('#_status').text('');
                if (preventCrazySettings() == false) {
                    return;
                }
                var loaderGif = 'assets/images/loader.gif';
                $("#chart").parent().prepend("<img id='imgloader' height='100' style='position:absolute;' alt='loading...' title='loading...' src="+loaderGif+" />");
                
                var dtime = adaptDateTimeToCache();

                $('#chart').css('opacity', .5);
                $.getJSON('api.php', {   
                        'type':'predictionChart3',
                        'coin':         $('#_crypto').find(':selected').val(),
                        'interval':     $('#_interval').find(':selected').val(), 
                        'historymins':  $('#_historymins').find(':selected').val(),
                        'currentDateTime': (dtime).format("YYYY-MM-DDTHH:mm"), // UTC
                        'featuresID': $('#_featuresID').find(':selected').val(),
                        'batchsize': $('#_batchsize').find(':selected').val(),
                        'neurons': $('#_neurons').find(':selected').val(),
                        'windowsize': $('#_windowsize').find(':selected').val(),
                        'epochs': $('#_epochs').val(),
                        'hiddenlayers': $('#_hiddenlay').find(':selected').val(),
                        'predicted_feature': 'price3',
                    }, function (data, status) {
                        DATA = data;
                        console.log(DATA);
                        if (isObject(data)) {
                            drawGraphs();
                        } else {
                            alert("Empty dataset returned from server");
                        }
                        $('#chart').css('opacity', 1);
                        $("body #imgloader").remove()
                }).fail(function (jqxhr, status, error) { 
                    console.log('error', status, error);
                    alert("Something went wrong...");
                    $("body #imgloader").remove()
                });
            }
            function prev() {
                var now = localToUTC(new Date());
                var dtime = $("#_datepicker").val() == "" ? now : localToUTC($("#_datepicker").val());
                dmom = moment(dtime);
                dmom.add(-$('#_interval').find(':selected').val(), 'minutes');
                $("#_datepicker").val( UTCtoLocal(dmom).format("YYYY-MM-DD HH:mm") );
                requestAndDraw();
            }
            function next() {
                var now = localToUTC(new Date());
                var dtime = $("#_datepicker").val() == "" ? now : localToUTC($("#_datepicker").val());
                dmom = moment(dtime);
                dmom.add($('#_interval').find(':selected').val(), 'minutes');
                $("#_datepicker").val( UTCtoLocal(dmom).format("YYYY-MM-DD HH:mm") );
                requestAndDraw();
            }
        </script>

    </body>
</html>