

console.log("start: telegram bot")

const functions         = require('./functions.js')();
const bot = functions.init_telegram_bot_1({polling: true});

const mongo         = require('mongodb');
const MongoClient   = mongo.MongoClient;
const dbCfg         = require('../db.js');
const mailer         = require('../mail')();

MongoClient.connect(dbCfg.url, dbCfg.settings, async (err, database) => {
  if (err) {
    console.log("ici");
    return console.log(err)
  }
  cryptoDB = database.db('crypto');
  const auth = require('../auth.js')(cryptoDB, mailer);
  const payments = require('../payments.js')(cryptoDB);

  bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "Hi there! This CryptoPredicted Bot can send you trade signals. To learn more sign up here http://cryptopredicted.com/ and you'll find futher instructions inside.");
  });

  bot.onText(/\/enable_signals (.+)/, async (msg, match) => {
    try {
      const chatId = msg.chat.id;
      const resp = match[1].trim().split(':'); // email:id
      const email = resp[0];
      const id = resp[1];

      var user = await findUserByID(id)
      if (user != null && 'email' in user && email == user.email) {
        if (await canNotifyUser(email)) {
          var upsert = await cryptoDB.collection('telegramChatIds').update({'email':email}, {'$set':{'chatId':chatId}}, {'upsert':true});
          console.log(upsert.result)
          if (upsert.result.ok && upsert.result.n && 'upserted' in upsert.result) {
            bot.sendMessage(chatId, "Perfect! You can now receive live trade signals in this chat.")  
          } else if (upsert.result.ok && upsert.result.n) {
            bot.sendMessage(chatId, "You are already good to go.")  
          } else {
            bot.sendMessage(chatId, "Oops... something went wrong, you should reach out to our support team. (error: 'TG#43' )")
          }
          
        } else {
          bot.sendMessage(chatId, 'Your subscription (or trial period) has expired, please subscribe here https://cryptopredicted.com/billing ');  
        }
      } else {
        bot.sendMessage(chatId, 'Incorrect ID, correct the typo and try again.');  
      }
    }
    catch (ex) {
      console.log(ex);
      bot.sendMessage(chatId, 'Incorrect ID, correct the typo and try again.');  
    }
    
  });

  /*bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, 'Received your message');
  });*/

  //bot.sendMessage('518520420', "test notif")

  async function findUserByID(id) {
    try {
      var o_id = new mongo.ObjectID(id);
      var cursor =  cryptoDB.collection('users').find({_id: o_id});
      var user = null;
      if(await cursor.hasNext()) {
        user = await cursor.next();
      }
      return user;
    } catch (ex) {
      console.log(ex)
    }
    return null;
  }

  async function canNotifyUser(email) {
    var user = await auth.findUser(email);
    if (!user) {
        console.log("core: " + email + " user not found");
        return false;
    }
    else if (!auth.isEmailVerified(user)) {
        console.log("core: " + email + " not verified");
        return false;   
    }
    return await payments.hasExclusiveAccess(user, function() {
        console.log("core: " + email + " ok!");
        return true;
    }, function() {
        console.log("core: " + email + " has no exclusive access");
        return false;
    });
  }

});