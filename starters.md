# Starter's guide

In this document you'll find various commands, shortcuts and crucial instructions. The "how's and why's" are not documented here, so if you need a detailed explanation please consult the other README.md files, if your question still remains unanswered please reach out to ilja@nevolin.be .

## Web server
The  NodeJS nodes are managed by the "pm2" tool, a few important commands:
```
pm2 help
pm2 status
pm2 logs
pm2 restart all
pm2 restart [node name or id]
```

## MongoDB
To login as root into MongoDB (must be done on machine where MongoDB runs):
```
cd /home/cryptopredicted
./mongo_admin.sh

# this will print the login commands which you have to copy&paste into the shell.
```


To login as admin into MongoDB to access the CryptoPredicted collections:
```
cd /home/cryptopredicted
./mongo_user.sh
```

### MongoDB example usage
```
use crypto
show collections

db.users.findOne()
db.users.find({email:"ilja@nevolin.be"})

db.users.update({email:"ilja@nevolin.be"}, {$set:{name: "Ilja"}})

db.users.remove({email:"ilja_fake@nevolin_fake.be"})
```

# Slave server (worker node)
```
cd /home/cryptopredicted
. env.sh

python starter.py
python starter.py f
python starter.py close

tail -f logs/twitter*
tail -f logs/reddit*
tail -f logs/*

ps aux | grep Producer.py
kill -9 $(ps aux | grep facebookProducer)

htop
```

# Misc.

View status of different modules (as used by "status.py"):
https://cryptopredicted.com/PWA/api/status

