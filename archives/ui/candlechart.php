<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Using machine learning and big data we are able to analyze cryptocurrencies and make short-term predictions. This allows us to make better investing decisions in a highly uncertain crypto world.">
        <meta name="author" content="Ilya Nevolin">

        <link rel="shortcut icon" href="assets/images/fav.ico">

        <title>CryptoPredicted | forecasting crypto prices using AI and big data</title>

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
                                        <h4 class="m-t-0 header-title"><b>Base:</b></h4>
                                        <select class="form-control" id="_base">
                                            <option value="BTC">Bitcoin (BTC)</option>
                                            <option value="ETH">Ethereum (ETH)</option>
                                            <option value="LTC">Litecoin (LTC)</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Quote:</b></h4>
                                        <select class="form-control" id="_quote">
                                            <option value="USDT">USDT</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>Interval:</b></h4>
                                        <select class="form-control" id="_interval">
                                            <option value="2">2min</option>
                                            <option value="5">5min</option>
                                            <option value="10">10min</option>
                                            <option value="30">30min</option>
                                            <option value="60" selected>1h</option>
                                            <option value="180">3h</option>
                                            <option value="360">6h</option>
                                            <option value="720">12h</option>
                                            <option value="1440">daily</option>
                                        </select>
                                    </div>
                                    <div class="col-sm-2">
                                        <h4 class="m-t-0 header-title"><b>History size:</b></h4>
                                        <select class="form-control" id="_historymins">
                                            <option value="20">20min</option>
                                            <option value="40">40min</option>
                                            <option value="60">1h</option>
                                            <option value="120">2h</option>
                                            <option value="180">3h</option>
                                            <option value="360">6h</option>
                                            <option value="720">12h</option>
                                            <option value="1440">1 day</option>
                                            <option value="2880">2d</option>
                                            <option value="4320" selected>3d</option>
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
                                        <button class="btn btn-success waves-effect waves-light m-t-20" onclick="requestAndDraw()">Generate</button>
                                    </div>
                                </div>
                                <div class="row m-t-10">
                                    <div id="chart"></div>
                                </div>
                                
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-sm-12 card-box">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <p>
                                            For more information about this tool and settings please read <a href="https://medium.com/@cryptopredicted/improving-our-autopilot-crypto-predictions-system-41360a82484b" target="_blank">this</a>.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>


                        <div class="row">
                            <div id="scrollHere_1"></div>
                            <div>
                                <p id="newsMentions">
                                </p>
                            </div>
                            <div>
                                <p id="socialMentions">
                                </p>
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

        <!-- jQuery  -->

        <script src="assets/js/jquery.core.js"></script>
        <script src="assets/js/jquery.app.js"></script>

        <!-- custom -->
        <script src="js/plotly-latest.min.js"></script>
        <script src="js/jquery.datetimepicker.full.min.js"></script>
        <script src="js/moment.js"></script>
        <script src="js/moment-timezone.js"></script>
        <script src="js/moment-timezone-with-data-2012-2022.js"></script>
        <link rel="stylesheet" href="css/jquery.datetimepicker.min.css">
        <script src="js/custom.js?random=<?php echo filemtime("js/custom.js"); ?>"></script>
        <script>
            function drawGraphs() {
                data = [];                
                data = data.concat(draw_price_candles(DATA));
                // data = data.concat(draw_price_trend(DATA));

                var WIDTH_IN_PERCENT_OF_PARENT = 100,    HEIGHT_IN_PERCENT_OF_PARENT = 70;
                $("#chart").css({
                    width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                    height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
                });
                window.onresize = function() {
                    Plotly.Plots.resize('chart');
                };

                var layout = {
                    dragmode: 'pan', 
                    margin: {
                        r: 50, 
                        t: 25, 
                        b: 40, 
                        l: 60
                    }, 
                    //showlegend: false, 
                    xaxis: {
                        autorange: true, 
                        domain: [0, 1], 
                        range: [ data[0].x[0], data[0].x[data[0].x.length-1] ], 
                        rangeslider: {range: [ data[0].x[0], data[0].x[data[0].x.length-1] ]}, 
                        title: 'Date', 
                        type: 'date',

                        
                    }, 
                    yaxis: {
                        //autorange: true, 
                        type: 'linear'
                    }
                };


                Plotly.newPlot('chart', data, layout, {scrollZoom: true});
            }
            function requestAndDraw() {
                if (preventCrazySettings() == false) {
                    return;
                }
                var loaderGif = 'assets/images/loader.gif';
                $("#chart").prepend("<img height='100' alt='loading...' title='loading...' src="+loaderGif+" />");
                
                var dtime = adaptDateTimeToCache();

                $('#chart').css('opacity', .5);
                $.getJSON('https://cryptopredicted.com/PWA/api/', {   
                        'type':         'exchange',
                        'exchange':     'binance',
                        'base_cur':     $('#_base').find(':selected').val(),
                        'quote_cur':    $('#_quote').find(':selected').val(),
                        'interval':     $('#_interval').find(':selected').val(), 
                        'historymins':  $('#_historymins').find(':selected').val(),
                        'currentDateTime': (dtime).format("YYYY-MM-DDTHH:mm"), // UTC
                    }, function (data, status) {
                        DATA = data;
                        console.log(DATA);
                        if (isObject(data)) {
                            drawGraphs();
                        } else {
                            alert("Empty dataset returned from server");
                        }
                        $('#chart').css('opacity', 1);
                        $("#chart img").remove();
                }).fail(function (jqxhr, status, error) { 
                    console.log('error', status, error);
                    alert("Something went wrong...");
                    $("#chart img").remove()
                });
            }
        </script>

    </body>
</html>