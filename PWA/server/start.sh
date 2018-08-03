pm2 start server_dev.js --watch
pm2 start server_live.js # don't watch

pm2 start operations/ops.js --watch

pm2 start algos/ROIs.js --watch
pm2 start algos/algos.js --watch

pm2 start notifiers/telegram.js --watch