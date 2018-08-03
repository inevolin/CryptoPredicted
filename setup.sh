#!/usr/bin/env bash
# use this setup for a brand new server

# set server timezone to UTC (required!)
echo "=========================================="
echo "================ timezone ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Etc/UTC" > /etc/timezone
    dpkg-reconfigure -f noninteractive tzdata
    timedatectl set-timezone Etc/UTC
    apt-get -y upgrade
fi

# install mongodb
echo "=========================================="
echo "================ mongodb  ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
    apt-get update
    apt-get install -y mongodb-org
    service mongod start
    systemctl enable mongod

    read -p " hit enter plz :) " -n 1 -r
fi

# make sure python and python3 are properly installed
# install python pip
echo "=========================================="
echo "================ pip      ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    apt-get install -y python-pip
    apt-get install -y python3-pip
    pip install --upgrade pip
    pip3 install --upgrade pip
fi



echo "=========================================="
echo "================ sbt      ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
    apt-get update
    apt-get install -y sbt
fi



echo "=========================================="
echo "================ JDK 8    ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    apt-get install -y software-properties-common
    apt-get install -y python-software-properties debconf-utils
    add-apt-repository -y ppa:webupd8team/java
    apt-get update
    echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | debconf-set-selections
    apt-get install -y oracle-java8-installer
    apt install -y oracle-java8-set-default
fi


echo "=========================================="
echo "=============== Kafka zK  ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    wget http://apache.belnet.be/kafka/1.0.0/kafka_2.11-1.0.0.tgz
    tar -xzf kafka_2.11-1.0.0.tgz*
    rm -dfr /etc/kafka
    mv kafka_2.11-1.0.0 /etc/kafka
    rm kafka_2.11-1.0.0.tgz
    printf "\nlog.retenetion.minutes=5" >> /etc/kafka/config/server.properties
    /etc/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 4 --topic mentionsSocial
    /etc/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 4 --topic mentionsNews

    printf "\nexport KAFKA_HOME=/etc/kafka" >> ~/.bashrc
    printf "\nexport PATH=$PATH:$KAFKA_HOME/bin" >> ~/.bashrc

fi

echo "=========================================="
echo "================ virtenv  ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    apt-get install -y python3-venv
    pyvenv ENV
    mkdir logs
fi

echo "=========================================="
echo "================ pips.sh  ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./pips.sh
fi


echo "=========================================="
echo "================ swap mem ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    fallocate -l 2G /swapfile_2g
    chmod 600 /swapfile_2g
    mkswap /swapfile_2g
    swapon /swapfile_2g
    free -lm
    printf "\nLABEL=swapfile_2g      /swapfile_2g   swap    defaults        0       0" >> /etc/fstab
    printf "\n/swapfile_2g   none    swap    sw    0   0" >> /etc/fstab
fi

echo "=========================================="
echo "================= nginx =================="
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
	printf "\ndeb http://nginx.org/packages/mainline/ubuntu/ xenial nginx" >> /etc/apt/sources.list
	printf "\ndeb-src http://nginx.org/packages/mainline/ubuntu/ xenial nginx" >> /etc/apt/sources.list
	wget http://nginx.org/keys/nginx_signing.key
	apt-key add nginx_signing.key

	apt-get -y update
	apt-get install -y nginx
	systemctl enable nginx
	systemctl start nginx
	#systemctl status nginx
fi


echo "=========================================="
echo "================= php7 =================="
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
	apt install -y php7.0-fpm php7.0-mbstring php7.0-xml php7.0-mysql php7.0-common php7.0-gd php7.0-json php7.0-cli php7.0-curl
	systemctl start php7.0-fpm
	systemctl status php7.0-fpm
	apt-get install -y php-mongodb
	printf "\nextension=mongodb.so" >> /etc/php/7.0/fpm/php.ini
	printf "\nextension=mongodb.so" >> /etc/php/7.0/cli/php.ini
fi

echo "=========================================="
echo "================ nodejs =================="
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
    sudo apt-get install -y nodejs
    mkdir -p PWA/server/
    cd PWA/server/
    npm install npm@latest -g
    npm install pm2@latest -g
    pm2 update
    pm2 startup
fi

echo "=========================================="
echo "================ .bashrc  ================"
read -p "proceed? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
#    printf "\nalias python=python3">> ~/.bashrc
    printf "\nexport JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> ~/.bashrc
    printf "\nexport PATH=$PATH:$JAVA_HOME/bin" >> ~/.bashrc
    source ~/.bashrc
    echo "
    ======
    Now run:	source ~/.bashrc
    === end
    "
fi
