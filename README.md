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

### env.sh
We are using virtual environments for Python, this is necessary for managing dependencies without altering the default Python installation.
So whenever we run Python scripts, make sure you are inside a virtual environment like:
```
cd -P ~/cryptopredicted # navigate to the working directory
. env.sh # enter the virtual environment ; only once
(... doing python work ... )
deactivate # exit the virtual environment ; whenever no longer needed
```


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
