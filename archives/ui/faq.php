<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Using machine learning and big data we are able to analyze cryptocurrencies and make short-term predictions. This allows us to make better investing decisions in a highly uncertain crypto world.">
        <meta name="author" content="Ilya Nevolin">

        <link rel="shortcut icon" href="assets/images/fav.ico">

        <title>CryptoPredicted | forecasting crypto prices using AI and big data</title>

        <!--Morris Chart CSS -->
		<link rel="stylesheet" href="./plugins/morris/morris.css">

        <link href="assets/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
        <link href="assets/css/icons.css" rel="stylesheet" type="text/css" />
        <link href="assets/css/style.css" rel="stylesheet" type="text/css" />

        <script src="assets/js/modernizr.min.js"></script>


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
                                <h4>General chart explained</h4>

                                <div class="row">
                                    <div class="col-sm-12">
                                        <p>
                                            On top there are a few settings you can play with:
                                        </p>
                                    </div>
                                    <div class="col-sm-12">
                                        <img src="assets/images/generalChartOptions.png" style="max-width: 600px; border:1px solid #DBDDDE; margin:20px 0px 20px 0px;">
                                    </div>
                                    <div class="col-sm-12">
                                        <ul>
                                            <li><strong>Crypto: </strong>here you can choose which coin to analyze.</li>
                                            <li><strong>Interval: </strong>at what time intervals to aggregate data by: every 30 minutes, hourly, daily, ...</li>
                                            <li><strong>History size: </strong>data is generated ending in "Datetime" and going back the selected history size.</li>
                                            <li><strong>Datetime: </strong>the maximum datetime to display for the data (most right interval on the x-axis). By default "Datetime" is set to your local date and time.</li>
                                            <li><strong>Generate: </strong>this button will request the necessary data from our API and then redraw the entire chart.</li>
                                        </ul>
                                        <span>
                                            Example: from the screenshot above, the hourly intervals will be in range of [Jan 23 14:00 -- Jan 24 14:00].
                                            <br>On the chart itself the very first tick/interval will be <u>Jan 23 14:00</u> because "14:00" includes everything from 14:00:00 until 14:59:59.
                                        </span><br><br>
                                    </div>

                                    <div class="col-sm-12">
                                        <p>
                                            When you hover over the chart you will see a toolbox appear in the top right corner:
                                        </p>
                                    </div>
                                    <div class="col-sm-12">
                                        <img src="assets/images/generalChartToolbox.png" style="max-width: 350px; border:1px solid #DBDDDE; margin:20px 0px 20px 0px;">
                                    </div>
                                    <div class="col-sm-12">
                                        <p>
                                            One of the most important tools is the "Reset axes" button. If for some reason you have messed up the chart a bit, then you can go back to the original view.
                                            Beware that this does not reset your settings (interval, history size, ...). To reset the latter you have to re-open the webpage (not just F5).
                                        </p>
                                    </div>
                                    
                                </div>

                                <div class="row" style="border-top: 1px solid #DBDDDE;">
                                    <div class="col-sm-12 m-t-20">
                                        <p>
                                            On the general chart there are many different graphs which you can show/hide by clicking on the labels.
                                            <br>Let me provide a briefy explanation of every graph.
                                        </p>
                                    </div>
                                    <div class="col-sm-12">
                                        <img src="assets/images/labels01.png" style="max-width: 800px; border:1px solid #DBDDDE; margin:20px 0px 20px 0px;">
                                    </div>
                                    <div class="col-sm-12">
                                        <ul>
                                            <li><strong>Price max/avg/min:</strong> the maximum/average/minimum recorded price within each interval.</li>
                                            <li><strong>Price trend:</strong> this draws trendlines through the "Price avg" points.<br><br></li>

                                            <li><strong>volume24h_avg_rel trend:</strong> the relative average traded volume 24h as recorded for each interval.</li>
                                            <li><strong>volume24h_avg_delta_rel trend:</strong> the average traded volume of the past 24 hours for a given interval T, minus the volume of T-1 to obtain a delta-value that indicates whether the traded volume went up/down at T.<br><br></li>
                                            
                                            <li><strong>sentiments_news_rel_delta trend:</strong> the result of sentiment analysis for news articles. At each interval the positive scores are subtracted from negative scores.</li>
                                            <li><strong>sentiments_social_rel_delta trend:</strong> the result of sentiment analysis for social media mentions (idem dito).<br><br></li>

                                            <li><strong>mentions_news_rel_avg:</strong> the relative number of news articles published during a given interval.</li>
                                            <li><strong>mentions_news_rel_avg trend:</strong> idem dito.<br><br></li>
                                            
                                            <li><strong>mentions_social_rel_avg:</strong> idem dito for social media mentions, here average means we take the average value of all social media sites.</li>
                                            <li><strong>mentions_social_rel_avg trend:</strong> idem dito.<br><br></li>
                                            
                                            <li><strong>mentions_social_abs_sum_rel:</strong> previously it took the average value of all social media sites, here we make a sum of the mentions count of every social site. It's not very recommended to use this because there are way more Tweets than Facebook/Reddit posts per second - so Tweets shall dominate the graph.</li>
                                            <li><strong>mentions_social_abs_sum_rel trend:</strong> idem dito.<br><br></li>

                                            <li><strong>mentions_social_rel [trend]: (XYZ):</strong> it shows the relative mentions count of every included social media platform. The average value at every interval results in the graph as shown by "mentions_social_rel_avg [trend]".<br><br></li>
                                        </ul>
                                    </div>
                                    <div class="col-sm-12">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <span><strong>Relative</strong>: in our context relative means values in range [0, 100] or [-100, 100] depending on the data.</span>
                                            </div>
                                        </div>

                                        <div class="row">
                                            <div class="col-sm-12">
                                                <p>
                                                    <strong>Trendlines</strong>:
                                                    A "trendline" over data is drawn using sub-trendlines consisting of the selected number of points (shape). The trendlines can be set to match the original data points by choosing "original".
                                                    Some graphs as explained above can show the exact same data if 'trend' is set to 'original'. When 'trend' >= 3 then you can see how the trendlines are drawn through the data points. Changing the trendline shape will automatically redraw it on the chart.
                                                </p>
                                            </div>
                                            <div class="col-sm-4 text-center">
                                                <span>Here are two partial graphs where trend is set to "original":</span>
                                                <img src="assets/images/trendOriginal.png" style="max-width: 100%;">
                                            </div>
                                            <div class="col-sm-4 text-center">
                                                <span>Here are the same two graphs with trend set to 4:</span>
                                                <img src="assets/images/trend04p.png" style="max-width: 100%;">
                                            </div>
                                        </div>

                                    </div>
                                    
                                    <div class="col-sm-12" style="border-top: 1px solid #DBDDDE;">
                                        <div class="row m-t-20" >
                                            <div class="col-sm-6">
                                                <span>At some given interval we may be interested in reading the news headlines and/or social mentions:</span><br>
                                                <img src="assets/images/clickOnPoint.png" style="max-width: 100%;"><br>
                                            </div>
                                            <div class="col-sm-6">
                                                <span>So by simply clicking on that point, it will load a subset of most interesting headlines/mentions:
                                                <img src="assets/images/clickOnPointResults.png" style="max-width: 100%;"><br>
                                            </div>
                                        </div>
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

        <!-- jQuery  -->

        <script src="assets/js/jquery.core.js"></script>
        <script src="assets/js/jquery.app.js"></script>


    </body>
</html>