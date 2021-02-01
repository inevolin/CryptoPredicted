# CryptoPredicted

## Installation
This is a step by step guide for installing the CryptoPredicted PWA (progressive web application) as of 03 August 2018. The system architecture will look like this:

![Image of Yaktocat](https://i.imgur.com/gHKTPDJ.png)

You may notice that the setup consists of two servers. This is recommended to spread the CPU and memory load, such that one server is more or less dedicated to serving web content to the end-user. In theory you can put everything on one server, doing so is your own risk.

### Server info
Make sure each server has at least 2GB RAM and a dual-core CPU.
Server B (which runs the A.I. computations) is very resource intensive, thus the more CPU and RAM you can add the better (up to a certain limit).
Server A is the web server, thus it also requires CPU and RAM, depending on your traffic volume, and/or any additional computations.

Both servers must be Ubuntu v16 -- any other Linux distribution or version hasn't been tested, use it at your own risk.
Make sure Python 2.7 and Python 3.5.2 are installed and working.

### Basics
Make sure you are logged in as root throughout the entire setup.
Run the following on all servers:
```
mkdir -p /home/cryptopredicted/
ln -s /home/cryptopredicted/ ~/cryptopredicted
cd /home/cryptopredicted/
```
This will create a symbolic soft-link, so whenever you open a new shell prompt, you can quickly navigate to the core location, like this:
```
cd -P cryptopredicted
# assuming you are in the /root/ directory (~)
```

### setup.sh
Let's run the setup.sh (on both servers) -- this will install the many dependencies which the various components require.
```
cd /home/cryptopredicted/
./setup.sh
```
##### make sure all files with .sh exetension have exec privileges, if not then run: chmod u+x setup.sh  (replace setup.sh by the necessary file)

The setup.sh will prompt you for (y/n) questions, answering them by typing y or n (without pressing enter).
If you're unsure which modules to install on which server, you can install everything on both servers. It might actually be better doing so.
The following list summarizes each dependency which the setup will prompt:
- timezone configuration (required): this will set the server timezone to UTC.
- mongodb: Primary database. Install on server A (optional on server B).
- pip: Python package manager. Install on server B (optional on server A).
- sbt: Dependency for JDK/Kafka. Install on server B (optional on server A) (not sure whether really required).
- JDK 8: Java development kit required for Kafka. Install on server B (optional on server A).
- Kafka zK: Apache Kafka with Zookeeper for message management. Install on server B (optional on server A).
- virtenv: Virtual environment for Python. Install on server B (optional on server A).
- pips.sh: Installs a list of Python libraries required by various Python scripts. Install on server B (optional on server A).
- swap mem: Creates and activates swap memory which supplements main memory (2Gb default). Optional for both servers, recommended if less than 4Gb working memory.
- nginx: Web server. Install on server A (optional on server B).
- php7: Php v7 module for nginx (optional).
- nodejs: Install on server A (optional on server B).
- .bashrc: Configures JAVA variables for root user. Required on server B (optional on server A).

### Nginx configuration
Let's configure the web server (server A).
Make sure your NS records of the domain are properly configured, whereby you have two A records (host: @ and host: www) pointing to the public IP address of server A. You can validate this by running "ping cryptopredicted.com" -- if the NS records are correct you will receive positive response messages from your server.

Then create the directories (if not yet exist) and create the domain configuration file:
```
mkdir /etc/nginx/sites-available
mkdir /etc/nginx/sites-enabled
touch /etc/nginx/sites-available/cryptopredicted.com
ln -s /etc/nginx/sites-available/cryptopredicted.com /etc/nginx/sites-enabled/cryptopredicted.com
```

Paste the following code into "/etc/nginx/sites-available/cryptopredicted.com":
```

server {
        listen 80;
        server_name cryptopredicted.com;
        return 301 https://cryptopredicted.com$request_uri;
}

server {
        listen 80;
        server_name www.cryptopredicted.com;
        return 301 https://cryptopredicted.com$request_uri;
}

server {
        listen 443 ssl http2;
        server_name www.cryptopredicted.com;

        ssl_certificate /home/cryptopredicted/PWA/ssl/server-bundle.crt;
        ssl_certificate_key /home/cryptopredicted/PWA/ssl/server.key;

        return 301 https://cryptopredicted.com$request_uri;

}

server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name cryptopredicted.com;

        ssl_certificate /home/cryptopredicted/PWA/ssl/server-bundle.crt;
        ssl_certificate_key /home/cryptopredicted/PWA/ssl/server.key;

        location / {
                proxy_pass https://localhost:9443/;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
        location /socket.io/ {
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $http_host;
                proxy_set_header Connection "upgrade";
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header X-NginX-Proxy true;
                proxy_set_header X-Forwarded-Proto https;

                proxy_pass https://localhost:9443/socket.io/;
                proxy_redirect off;

                proxy_http_version 1.1;
        }

        location /PWA/ {
                proxy_pass https://localhost:8443/;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
        location /PWA/socket.io/ {
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $http_host;
                proxy_set_header Connection "upgrade";
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header X-NginX-Proxy true;
                proxy_set_header X-Forwarded-Proto https;

                proxy_pass https://localhost:8443/socket.io/;
                proxy_redirect off;

                proxy_http_version 1.1;
        }



        location ~ \.php$ {
                return 301 http://cryptanal.com$request_uri;
        }


}
```

Finally add the following line of code into "/etc/nginx/nginx.conf" (unless it's already there):
```
include /etc/nginx/sites-enabled/*;
```
Make sure Nginx is not throwing any errors by executing "nginx -t" it should say all is successful.
And then run "service nginx restart" to restart the web server (which should execute without any output/error).

### MongoDB

Run the following commands to create two MongoDB users:
```
mongo
use admin
db.createUser({user:"root",pwd:"1561_AEI_qzef26_GRZ_ez65",roles:[{ role: "root", db: "admin" }]})
use crypto
db.createUser({user:"cryptopredicted",pwd:"1561_AEI_qzef26_GRZ_ez65_fezo_fze6",roles:[{ role: "readWrite", db: "crypto" }]})
```
The first user is root and can do everything (feel free to change its password).
The second user is "public", whereby we can use its credentials to connect and authenticate with the "crypto" database from anywhere in the world. So make sure its password is pretty darn secure.

Let's configure MongoDB to make it available from the outside and add required secure authentication.
Edit the "/etc/mongod.conf" file.

First, find the "net:" line and add your server A's public IP to the bindIp line:
```
net:
  port: 27017
  bindIp: localhost,159.69.94.65
```

Find the "security:" line and add authorization ; or add it manually:
```
security:
  authorization: 'enabled'
```

Now restart MongoDB by running "service mongod restart" -- it should restart fine without throwing any errors.
To test the connection to the database use the "./mongo_user.sh" script, which should allow you to connect from any server. You can also use the "./mongo_admin.sh" script on server A to login as user (this will only print commands which you need to execute manually).

There are various files which use the IP address of the server where MongoDB runs. So make sure to edit the following files and change the IP address to that of your server A:
- PWA/server/db.js
- DAL.py
- mongo_user.sh
Note: use localhost or 127.0.0.1 instead of the public IP address if you know for certain whether the module(s) will run on the same server as the MongoDB instance.

### Collections
Let's quickly go over the various collections in our database, so you know what they are used for.
To see all collections in MongoDb use the commands:
```
use crypto
show collections
```

- algoSubs: Storing notification types for the various users (refer to "Trade Signals" page). When a user wants to receive buy/sell signals from a specific strategy, they can enable it and this information is stored right here. The notifications module which sends out the signals uses this collection to know which user should be notified.
- algo_portfolios: The ROIs.js Node worker, which computes the ROI of buy/sell signals, for all strategies, stores the entire portfolio with the signals in this collection (including the price of the cryptocurrency, this eliminates the need to consult the collection for retrieving OHLC data).
- algo_signals: Whenever a new signal is generated by one of our algorithms/strategies, it is recorded here.
- exchanges: This collection stores OHLC and Volume data from the exchanges (currently only for Binance exchange).
- liveness: This collection stores heartbeat messages from our consumers, producers (and if any other workers) to be monitored by the "status.py" cron job. It records the timestamp of the last heartbeat, which the "status.py" uses to identify whether some component is offline or not working properly. But it may in some cases give false positives (for more info consult status.py itself).
- mentionsExtendedSocial and mentionsExtendedNews: these collections store raw data (tweets, news articles, facebook posts) -- the idea is to record the relevant information for later analysis or displaying tweets/posts to users on the front-end. These collections can grow really big in size (and already are); if you don't need this data it is better to disable usage of this in the consumerK.py script.
- mentionsNews and mentionsSocial: these collections store the flux of news and social mentions for the various cryptocurrencies from all the channels ; they display how many mentions there were regarding some crypto within a minute-window.
- sentimentsnews and sentimentsSocial: idem dito as the above, except here we store the sentiment scores of the analyzed raw posts/tweets/mentions.
- newsbuilds: this records the timestamp when a news site was lastly fully analyzed/scraped by the newsProducer. For more information refer to the code of this producer.
- payments: storing/recording user payments from paypal/stripe. Having a payment with an expiry data, for a given user, will grant them Premium status and membership.
- paymentsMetaData: storing meta data associated with payments. For more information refer to the payments node module.
- predictions_v1: storing A.I. predictions, generated by our predictor python script.
- telegramChatIds: this stores the chatId of a given user, which has synced its Telegram account with our Telegram bot. This user-to-bot conversation has a chatId. Given the chatId we can send messages to the user directly (through the bot), thus notifying them of any buy/sell signals.
- trials: storing trial users and their expiry date, default 7 day trial period. Trial users are granted Premium status for the limited period. Extending the trial period is as simple as extending the expiry field.
- users: storing user accounts with their sessionId and  encrypted password; The type field can be either "normal" or "affiliate", in the latter case affiliate users have access to their affiliate dashboard and automatically have Premium membership rights.


### Query optimization
To optimize search query performace you can create Indexes for the various collections.
Right now not every collection has indexes, but most relevant ones do.
And depending on the amount of data stored in a collection, Indexes can greatly improve performance; they make the difference of a search query running for 20 seconds or only 2 seconds.

For instance, the "exchanges" collection; which is an intensively used collection for retrieving OHLC and Volume data (currently only for Binance) -- for this collection we created an additional index based on 4 fields: base_cur, quote_cur, timestamp and exchange. The reason is that most API calls utilize this collection, and use those 4 fields to aggregate/search for. This Index has greatly improved the performance of lookups.
![](https://i.imgur.com/rfn7kjM.png)

Another collection "mentionsExtendedSocial", this one isn't used on the latest CryptoPredicted website and belongs to our deprecated Sentiment Analysis system. Here we have not (yet) created any index to improve the query performance, and you'll notice this effect once you start searching for data in this collection (it may take up to a minute to get some results). But after creating a meaningful Index based on the fields you filter on, the performance will greatly improve.
![](https://i.imgur.com/QNn4KqA.png)

You'll notice that some collections has unique indexes ; this means the fields in the index must be unique in value throughout the entire collection. By default the "_id" index is unique, because that's how MongoDB generates its unique identifiers. But in some collections we also have custom unique indexes, to prevent duplicates.

### Apache Kafka
Kafka is a message broker, not a long-term database. It's a scalable framework for receiving/sending messages from producers to consumers. It does temporarily store its messages as log files, however the default settings are too aggressive for us.

Edit the file "/etc/kafka/config/server.properties" and find the line which says "log.retention.hours". By default it's set to 168 hours, however, in our case we don't need it to store log files that long, because we process everything in an almost real-time fashion.

So we are going to add a new line like this:
```
log.retention.minutes=5
```
For more information please refer to the official doc: https://kafka.apache.org/documentation/

### env.sh
We are using virtual environments for Python, this is necessary for managing dependencies without altering the default Python installation.
So whenever we run Python scripts, make sure you are inside a virtual environment like:
```
cd -P ~/cryptopredicted # navigate to the working directory
. env.sh # enter the virtual environment ; only once
(... doing python work ... )
deactivate # exit the virtual environment ; whenever no longer needed
```
Note: for all our modules we solely use Python 3.5.2 -- since we don't use any other version, we've changed added the alias "python" to execute "python3". So by using "python" command you are actually executing the version 3.5.2.

### starter.py
This script is used for starting long-term jobs on server B (Kafka, consumers and producers).
To prompt (y/n) starting modules run:
```
python starter.py f
```
In our case we will answer y to every question.
This will start the Kafka + Zookeeper processes ; the consumer (sentiment analysis) and producers (fb, tw, ...).

To prompt stopping modules run:
```
python starter.py close
```
To show modules:
```
python starter.py
```

#### producers
The various producers are located in the producers/ directory (all having .py extension).
Each producer will write log files (info and error) which are located in the logs/ directory.

When a producer crashes it may (or may not) write an additional log file with ".stderr.log" extension.
If you are having trouble getting a producer to work, then manually debug it:
- make sure the process is stopped: kill -9 $(ps aux | grep facebookProducer)
- enter virtual env.: . env.sh
- run the producer: python producers/facebookProducer.py
- debug using the output/errors.

Note: the exchangeProducer.py (for OHLCV data from Binance) does not publish to Kafka, but immediately inserts into the MongoDB database.

#### consumer(s)
Right now there is only one consumer, called consumerK. This consumer takes the live output of each producer and processes it in real-time.
In the consumers/ directory there is an additional directory "tools" which cointains helpful scripts if you need to debug/analyze the Kafka stream.

Debugging the consumer is done through a similar approach as the producers.

#### mysettings.py
This file is very important and is used by most of the python scripts.
It contains several functions for logging and dates, but more importantly many static variables.

It has a mapping of crypto acronyms to real-life names. For instance, we want to associate BTC with all names people give to Bitcoin, which are: BTC, btc, btc#, bitcoin and #bitcoin. These phrases/words are used on social media, and they specify whether the conent/context is associated with BTC.

This association is a type of standardization and an important component for the entire system.

We also specify the tweets, groups and channels for various producers to scrape from (facebook, reddit, twitter, ...), each mapped by the crypto acronym (e.g. BTC). We also specify a list of news websites/channels for the news producer.

You'll also find some deprecated variables such as "CRYPTO_currencyProducer" and "SITES_forumProducer" which are no longer used, and were part of deleted components.

### NodeJS
For several reasons we use Nginx as an additional layer (to optionally support php7 with nodejs). You could also refactor the code to remove Nginx and use NodeJS as sole web server. But for now just play along.

On server A we are going to launch the necessary node workers.
Navigate to PWA/server/ and run "start.sh".

In our case we use the module "pm2" for running and managing our node workers. You can use commands such as "pm2 status" to see which node modules are running and which stopped/crashed. To debug you can run "pm2 logs" or "pm2 logs NAME_OF_NODE" to follow its info and error logs in real-time.

Once you have started our node workers, we have to tell pm2 to remember these -- so whenever the server is restarted (for whatever reason) it will automatically re-start our node workers. To do this run the "save.sh" script.

### Crontab: A.I. predictions
On server B we have to enable our A.I. predictions which are updated/generated every two minutes using a Python script.
Use the command "crontab -e" to open an editor, and at the end of the file add the following two lines:
```
# predictions v1
*/2 * * * * /home/cryptopredicted/ENV/bin/python3 /home/cryptopredicted/predictors/predictions_v1.py 10
*/2 * * * * /home/cryptopredicted/ENV/bin/python3 /home/cryptopredicted/predictors/predictions_v1.py 60
```
As you can see, every two minutes (*/2) two cron jobs will be started of the same file (predictions_v1.py) with different parameters (10 and 60 : referring to minutes). 

This is a dangerous system, because it can make your server crash. Lets say we run these cron jobs every 10 seconds, and given the fact that each one needs 30 seconds to finish, then the system will be overloaded with processes which start but never finish -- thus the server will crash/stall. Solving this is tricky and requires careful engineering. Make sure that each job has enough time to finish executing before a new one is started. Usually one minute per job is enough, with an additional one minute margin just in case (summing up to two minutes per job).

So if you decide to add more input data into the A.I. system, make the models more complex (deeper & more layers), or adding more cryptocurrencies -- keep in mind that this might reduce performance and increase execution time. As a result you may enter dangerous territory, so always have a plan B.

### Crontab: status.py
For the system admin there's an extra feature (highly recommended) which will attempt notifying you (in most cases) when a certain module is offline/crashed. 
Add the following line into crontab:
```
# notifying offline modules by mail
*/20 * * * * /home/cryptopredicted/ENV/bin/python3 /home/cryptopredicted/status.py liveness mailer
```
This status.py script is run every twenty minutes to check for offline modules -- and if any is offline for odd amount of time then an email will be sent. Make sure to have a look inside status.py to see/edit the thresholds for various components. But also change the admin's email address in "smtp.py", more specifically the "TO" variable; which is an array that contains one (or more) emails.

### Email configuration
Some modules will need SMTP access to send emails to the end-user(s) and/or the system admin.
By default it uses a regular Gmail account: cryptopredicted@gmail.com and uses its plain text password for auth.
If you need to change the account then do so in the following files:
- PWA/server/mail/index.js
- smtp.py

Note: regular Gmail accounts have a daily smtp sending limit. It's more recommended to use a Gsuite (paid Gmail) account which has much higher smtp sending limits.
If you use Google's service make sure to enable less secure apps - https://www.google.com/settings/security/lesssecureapps but also disable Captcha temporarily so you can connect - https://accounts.google.com/b/0/displayunlockcaptcha .



## Database migration
If you ever need to migrate the database from one server to another, you will need do this quickly and efficiently.

1. Shut down all producers, consumers and node workers (on all servers). Otherwise we may end up with duplicate key exceptions during import phase.
2. run on "source" database:
```
mongodump --username "root" --password "....." --authenticationDatabase "admin" --out mongodumpOut --db=crypto
```
3. copy the mongodumpOut directory from "source" server to destination "server". You can use scp for this:
```
scp -r mongodumpOut root@159.69.94.65:/home/cryptopredicted/
```
4. Enter mongo shell as root user on "destination" server and run:
```
use crypto
db.dropDatabase()
```
this will remove the entire crypto database, so whenever we import data (next), we don't have to deal with duplicate key exceptions.

5. On destination server run (make sure mongodumpOut dir is within scope):
```
mongorestore --username "root" --password "......" --authenticationDatabase "admin" mongodumpOut/
```
6. Restart all producers, consumers and node workers.

Note: depending on how quick you execute this process, you might experience data loss. So try to execute everything as quickly as possible to minimize its effects. It's also not clearly documented how mongorestore handles duplicate key exceptions, it "may" not even be necessary to shut down all modules (and/or dropping the database in step 4) prior to migrating the data.

## Contact

For enquiries or issues get in touch with me:

Name: [Ilya Nevolin](https://www.linkedin.com/in/iljanevolin/)

Email: ilja.nevolin@gmail.com
