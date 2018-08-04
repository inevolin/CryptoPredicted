# PWA (progressive web app)

This section contains the entire (latest) CryptoPredicted web app, completley built in NodeJS and HTML/CSS/jQuery.

The ssl/ dir contains SSL certificates, keys and more.
The server/ dir contains all NodeJS and web app specific files. Let's explore this in more detail.

## pm2
As explained in the intro install guide, we use pm2 to manage the node workers.

### start.sh explained
Notice that the PWA/server/start.sh script contains commands to launch these node workers, and notice that server_live.js is not being watched by pm2 for changes.
This is important because whenever we edit dependencies (js files) we don't want them to be visible on the live website just like that.
Basically all javascript files (which are managed by node) are being monitored/watched for changes, and if anything changes the node is automatically restarted (unless it's not being watched).

When developing new modules or bug fixing, we don't want to cause conflicts with end-users or otherwise they'll see errors/404/500 pages. That's why the server_live node (and its dependencies) aren't monitored for changes.
The server_dev.js file on the other hand is, and this is accessible through https://cryptopredicted.com/PWA/ (the /PWA path can be renamed to anything you want e.g. /DEV ).
So whenever you edit some file, which is used in the app (at some level), it will automatically restart this node so you'll be able to see the changes.

Let's say you made some changes, and you verified them as a developed (through the /PWA/ location), how do you persist them into the official website? Just run "pm2 restart all" or "pm2 restart server_live", now the live node will start using the new files/dependencies.

## algos/
Algorithms are initially developed in Python on your laptop/desktop (see the /backtest git directory), and once you're satisfied with the results you can re-write the Python logic into NodeJS logic. Doing so easy because the framework is already in place, and you only have to re-write the necessary logic. That's why it's important to use existing scripts as a starting point, making re-writing easier.

The "algos.js" file is the main node which runs stand-alone, and its task is to periodically execute the variously defined algo strategies to generate buy/sell signals. It does so every 10 seconds using scheduling jobs.

Each inidividual algorithm is very similar as to the Python based algorithms. At the end of every algorithm there are two functions "processSignals" and "processSignals_all". The first one (processSignals) is used to basically monitor only the latest signal (if any), and if there is a new signal generated it will notify the users accordingly. The other one "processSignals_all" is used whenever you have a brand new algorithm which has no signals recorded yet. In this case we can make it generate historical siganls, basically simulating real-life behavior. This is necessary so we can quickly assign an estimated ROI for the new strategy.
Whenever you add a new strategy into "algos.js", make sure to set the "FIRST_RUN" variable to true, to let it generate historical signals, and once it has done that (after 1 minute usually) you should set it back to "false", otherwise it will not notify the users of new signals!

## api/
This contains functions for MongoDB access and (private) API calls to access the data.
The specific endpoint URLs are found in the "index.js" file.

The API is primarily used by different components, such as the AI system, trade algorithms and more.
It's important to illustrate how to access and use it to get price data and sentiments.

Given the following URL which access our API:
https://cryptopredicted.com/PWA/api/?type=exchange,socialMentions,newsMentions,socialSentiments,newsSentiments&exchange=binance&base_cur=BTC&quote_cur=USDT&interval=60&historymins=2880&currentDateTime=2018-08-04T11:08
The above obtains:
- exchange data (OHLC and Volume data)
- social mentions, aggregated totals of social platforms which mentioned the base currency = {BTC, btc, bitcoin, ...}
- news mentions, idem dito but for news channels
- social sentiments, sentiment analysis for social channels which mentioned the base currency
- news sentiments, idem dito but for news channels
You also see that in this case we will data from exchange=binance (the only exchange currently in our database)
The above returns a JSON array with objects that look like this:
![](https://i.imgur.com/vXltBq1.png)

Note: not every object will have all the fields, in case they are missing these fields will not be included. So when writing code that parses these objects make sure to verify and check if the field you're accessing really exists on the object.

## mail/
This contains smtp/email specific code, and email templates, used for notifying the users by email (new user, password reset, signals, ...).

## notifiers/
This contains telegram specific bot notifications. So users can receive signal notifications directly to their telegram app. But they must complete the instructions as explained here https://cryptopredicted.com/notifications

## operations/
This is a directory for various/misc node workers.
At tis point it only contains one worker named "ops.js", which is used to notify users whose trial membership has just expired. This again is a scheduled job which runs every minute.

## views/
We use EJS templating for NodeJS front-end, because of its simplicity and easy of use.
The views dir contains various front-end templates and code logic.

## websocks/
Instead of doing ajax calls to get our trade signals and predictions (on the web app), we use web sockets. This makes sense in the case of the predictions, whereby users can leave their browser window open and it will automatically refresh/update the graph. This is possible with ajax as will (in a polling manner), but with websockets we instead "push" data to the users.
Whether this was necessary for the trade signals is a different question, but it may yield several benefits. Once again we can push data, less full-cycle HTTP requests which improve overall performance.

## various .js files
In the root of server/ you'll find several nodejs (.js) files which contain important server logic for, from processing payments to authentication.
These are pretty much self-explanatory and should be handled with care.



