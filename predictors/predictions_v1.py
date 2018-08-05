
# Artificial Intelligence (A.I.) price predictions

# this script uses tensorflow/Keras libraries, make sure they are installed properly.

import matplotlib
matplotlib.use('Agg')
import os, errno
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #  disable tensorflow error about CPU instructions

import time
import math
import numpy as np
import traceback
from numpy import concatenate
import matplotlib.pyplot as plt

import threading
import random

import json
import requests
import pprint
from collections import OrderedDict
from datetime import datetime, timedelta

import multiprocessing
import multiprocessing.pool

# mode
mode = "production"
# mode = "test"

import sys
sys.path.insert(0, '/home/cryptopredicted/')
sys.path.insert(0, '/home/cryptopredicted/presenters/')
from mysettings import dtNow, createLogger
import DAL
h5Dir = '/home/cryptopredicted/predictors/h5/'
imgDir = '/home/cryptopredicted/ui/prediction/images/'

def dtToString(dt):
    return datetime.strftime(dt, '%Y-%m-%dT%H:%M')

def create_train_dataset(dataset, look_back, n_features, seq_pred_len):
    # make sequences from 0 to len(dataset)-lookback
    sample, feature = [], []
    #print(len(dataset))
    #print(look_back)
    for i in range(0, len(dataset)-look_back-seq_pred_len):
        tmp = []
        for n in range(0, n_features):
            tmp.append( dataset[i:i+look_back, n] )
        sample.append(tmp)
        feature.append([ dataset[i+look_back:i+look_back+seq_pred_len, :n_features] ])
    # new array will be len(dataset)-1  (one size smaller)
    return np.array(sample), np.array(feature)

def create_test_dataset(dataset,look_back, n_features):
    # make sequences but make sure the end is included
    sample = []
    for i in range(0, len(dataset)-look_back+1): # +1 important! to make this function work when n_window=1
        tmp = []
        for n in range(n_features):
            tmp.append( dataset[i:i+look_back, n] )
        sample.append(tmp)
    return np.array(sample)

class MyMinMaxScaler():
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max

    def fit_transform(self, values):
        for x in range(len(values)):
            values[x] = (values[x] - self.min) / (self.max - self.min)

        return values

    def inverse_transform(self, values):
        for x in range(len(values)):
            values[x] = values[x] * (self.max - self.min) + self.min
        return values


# try different scalers
# http://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing
def prepare_trainingset(dataset, n_features, n_window, seq_pred_len):
    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    values = np.array(dataset) # make a copy
    #print(values)
    values = values.astype('float32')
    
    scalers = []
    for i in range(n_features):
        scalers.append( MinMaxScaler(feature_range=(0, 1)) )
        # scalers.append( StandardScaler() )
        # scalers.append(MyMinMaxScaler(0, 20000))

        values[:,i] = scalers[i].fit_transform(values[:,i].reshape(-1,1))[:,0]  # ##########################################

    #exit()

    #print("split into input and outputs")
    train = np.array(values)
    print(train.shape)

    train_X, train_y = create_train_dataset(train, n_window, n_features, seq_pred_len)
    print(train_X.shape, train_y.shape)

    train_X = train_X.reshape((train_X.shape[0], n_features, n_window))
    train_y = train_y.reshape(train_y.shape[0],n_features, 1*seq_pred_len) # the target data is a single array (:1) of n_features
    #print(train_X.shape, train_y.shape)
    #print()

    if train_X.shape[0] == 0:
        print(" => not enough historical data yet. aborted." )
        raise

    return (train, train_X, train_y, scalers)

def make_train_predictions(scalers, train_X, n_features, n_window, model, seq_pred_len):
    # predict training data: price
    xpolated = [()] * len(scalers)

    p_train = model.predict(train_X)
    p_train = p_train.reshape((p_train.shape[0], 1*seq_pred_len, n_features))
    future_pinv = np.array(p_train)
    for i in range(len(scalers)):
        dump = scalers[i].inverse_transform(p_train[:,:,i])[:,:]
        future_pinv[:,:,i] = dump
        
    return future_pinv

def make_future_predictions(scalers, train, n_window, n_features, predict_n_intervals, model, seq_pred_len):
    # !ici
    #########################################
    # here we predict future values (predictions)
    # notice that we create multiple predictions by using the latest prediction as new input data (shifting the input values)

    xpolated = [()] * len(scalers)

    future = np.array(train[-n_window:, :n_features]) # get a portion of historic data (size of window, because everything before is already predicted)
    for z in range( int(predict_n_intervals/seq_pred_len) ): 
        # we don't need every sequence, we let it predict all sequences; each iteration we keep only the latest one.
        future_p = create_test_dataset(future, n_window, n_features)
        # print("it: "+str(z))
        #print(" input: " + str(future_p.shape))
        # print()
        future_p = model.predict(future_p)
        future_p = future_p.reshape((future_p.shape[0], 1*seq_pred_len, n_features)) # 2D to 3D
        
        #print("output: " + str(future_p.shape))
        # print()
        future_pinv = np.array(future_p) # make deep copy
        for i in range(len(scalers)):
            dump = scalers[i].inverse_transform( np.array(future_p[:,:,i]) )[:,:]
            future_pinv[:,:,i] = dump
            if len(xpolated[i]) == 0:
                xpolated[i] = future_pinv[:,:,i].reshape(1*seq_pred_len) # -1 -1
            else:
                xpolated[i] = concatenate([ xpolated[i], future_pinv[:,:,i].reshape(1*seq_pred_len) ])
        
        #print("output': \n", str(future_pinv))
        #print()        
        xy_p = np.array(future_p[-1*seq_pred_len:,:,:]) # get most recent prediction
        xy_p = xy_p.reshape(1*seq_pred_len, n_features)

        future = np.array(future[1*seq_pred_len:, :n_features]) # remove oldest rows
        future = np.append(future, xy_p, axis=0)

        #print("---------------")
    # ! == feedback loop !
    #########################################
    
    return xpolated
    
def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def f_historymins(interval, n_window, multiplier):
    return interval*(n_window+1)*multiplier

def obtainDataset(exchange ,symbol, interval, historymins, currentDateTime, dataset_func, sync_dict_json):
    # get data from our API and process it given our dataset_func
    jsout = getJson(exchange, symbol['base_cur'], symbol['quote_cur'], interval, historymins, currentDateTime, sync_dict_json)
    try:
        dataset = dataset_func(jsout, symbol)
    except KeyboardInterrupt:
        raise
    except:
        jsout = getJson(exchange, symbol['base_cur'], symbol['quote_cur'], interval, historymins, currentDateTime, sync_dict_json)
        dataset = dataset_func(jsout, symbol)

    #######
    ####### removing rows where price is zero
    for row,_ in enumerate(dataset):
        if dataset[row][0] == 0: # zero price detected
            for col,_ in enumerate(dataset[row]):
                dataset[row][col] = 0 # set every column to zero because price is zero
    dataset = dataset[(dataset > 0).any(axis=1)] # delete entire row if all '0' value present
    #######

    return dataset

def fitAndPredict_trainAlways(h5fn, featuresID, exchange, symbol, n_window, interval, currentDateTime, predict_n_intervals, n_neuron, n_hiddenlay, n_epoch, n_batch_size, dataset_func,  sync_dict_json, sync_list_output, seq_pred_len):
    # this is the core A.I. training and predictions part.

    import random
    from keras import backend as K
    from keras.callbacks import EarlyStopping
    try:
        # if no model exists: prepare data, create model, train it, save it and clear it.
        if not modelExists(h5fn):
            historymins = f_historymins(interval, n_window, 70) # 1000
            dataset = obtainDataset(exchange ,symbol, interval, historymins, currentDateTime - timedelta(minutes=interval-1), dataset_func, sync_dict_json)
            n_features = len(dataset[0])
            (train, train_X, train_y, scalers) = prepare_trainingset(dataset, n_features, n_window, seq_pred_len)

            print("creating new model: " + h5fn)
            model = createModel(h5fn, n_neuron, n_hiddenlay, n_features, n_window, seq_pred_len)
            early_stopping_monitor = EarlyStopping(monitor='loss', patience=30, verbose=1)
            history = model.fit(train_X, train_y, epochs=n_epoch, batch_size=n_batch_size,  verbose=1, shuffle=False, callbacks=[early_stopping_monitor]) # validation_data=(test_X, test_y),
            saveModel(h5fn, model)
            saveWeights(h5fn, model)
            # saving scaler -- https://stackoverflow.com/questions/41993565/save-scaler-model-in-sklearn
            K.clear_session()
            del model

        # by now a model (already) exists; so we prepare data, load model, train it, make predictions and save the new weights.
        # notice that it's also possible to train the model once (step above), and then omit the "model.fit(...)" function, whereby we don't re-train the model each new generation.
        # if you omit continuous training, you will increase performance, but whether you accuracy is retained (through time) is not documented.

        # let us train once, and then just load model
        historymins = f_historymins(interval, n_window, 3)
        dataset = obtainDataset(exchange ,symbol, interval, historymins, currentDateTime, dataset_func, sync_dict_json)
        n_features = len(dataset[0])
        (train, train_X, train_y, scalers) = prepare_trainingset(dataset, n_features, n_window, seq_pred_len)

        model = loadModelAndWeights(h5fn)
        early_stopping_monitor = EarlyStopping(monitor='loss', patience=20, verbose=1)
        history = model.fit(train_X, train_y, epochs=n_epoch, batch_size=n_batch_size,  verbose=1, shuffle=False, callbacks=[early_stopping_monitor]) # validation_data=(test_X, test_y),
        saveWeights(h5fn, model)
        xpolated = make_future_predictions(scalers, train, n_window, n_features, predict_n_intervals, model, seq_pred_len)
        
        # let's prepare data to be stored into the database:

        currentDateTime = adjustDatetime(interval, currentDateTime)# we use real-time datetime to make predictions, but when we persist we'll floor the datetime according to the interval
        tmpdt = currentDateTime + timedelta(minutes=interval)
        maxdt = currentDateTime + timedelta(minutes=seq_pred_len*predict_n_intervals*interval)
        j = 0
        sendobj = { 'data': [],
                    'base_cur':symbol['base_cur'],
                    'quote_cur':symbol['quote_cur'],
                    'interval':interval,
                    'timestamp':currentDateTime,
                    'exchange':exchange,
                    'n_fid':featuresID,
                    'n_batch_size':n_batch_size,
                    'n_neuron':n_neuron,
                    'n_window':n_window,
                    'n_epoch':n_epoch,
                    'n_predict_intervals':predict_n_intervals,
                    'n_hiddenlay':n_hiddenlay,
                    'mode': mode}

        while (tmpdt <= maxdt and j < len(xpolated[0])):
            sendobj['data'].append(
                {
                    'timestamp': tmpdt,
                    'open': float(xpolated[0][j]),
                    'close': float(xpolated[1][j]),
                    'low': float(xpolated[2][j]),
                    'high': float(xpolated[3][j]),
                    'volume': float(xpolated[4][j]),
                    # 'signal': float(xpolated[5][j]),
                }
            )
            tmpdt += timedelta(minutes=interval)
            j += 1
        K.clear_session()
        del model

        # instead of writing each prediction individually, we use another shared dict variable, which we process at the very end.
        # this was implemented for several reasons (we want all predictions to be updated/stored at the same time, and not with a minute delay).
        # DAL.store_predictions_v1(DAL.openConnection(), sendobj)
        sync_list_output.append(sendobj)

        print(currentDateTime)

    except KeyboardInterrupt:
        raise
    except Exception as ex:
        traceback.print_exc()
        logErr = createLogger("predictions_v1_error", "predictions_v1_error")
        logErr.critical(str(ex), exc_info=True)

def getJson(exchange, base_cur, quote_cur, interval, historymins, currentDateTime, sync_dict_json):
    # getting data from our API (OHLC, volume, sentiments, ...) depending on the type parameter in query.

    # url = 'https://cryptopredicted.com/api.php?type=exchangeChart&exchange='+exchange+'&base_cur='+base_cur+'&quote_cur='+quote_cur+'&historymins='+str(historymins)+'&currentDateTime='+dtToString(currentDateTime)+'&interval='+str(interval)
    url = 'https://cryptopredicted.com/PWA/api/?type=exchange&exchange='+exchange+'&base_cur='+base_cur+'&quote_cur='+quote_cur+'&interval='+str(interval)+'&historymins='+str(historymins)+'&currentDateTime=' + dtToString(currentDateTime)
    
    log = createLogger("predictions_v1_info", "predictions_v1_info")
    log.info(url)

    i = 0
    force = False
    while url in sync_dict_json and sync_dict_json[url] == 0:
        time.sleep(0.25)
        i += 1
        if i*4 > 60: # wait 60seconds for the json (from other process), if it fails then force proceed yourself
            force = True

    # sync_dict_json is a dictionary shared among the other processes
    # it prevents making the same calls to the API, if the results are already obtained by some other process
    # we don't want to make unnecessary API calls, one is enough given the same parameters.
    if force or not url in sync_dict_json:
        print(url)
        sync_dict_json[url] = 0
        #print(url)
        response = requests.get(url)
        js = json.loads(response.text , object_pairs_hook=OrderedDict)
        sync_dict_json[url] = js
    #return js      
    return sync_dict_json[url]
    
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def func_ai_a(js, symbol):
    # preparing data to be trained, servers as input to the Neural Net (NN)

    dataset = [] #[()] * len(js)
    i=0
    for key in js: # DO NOT USE RELATIVE VALUES FROM API !!! only absolute ones
        if 'open' in js[key] and 'close' in js[key] and 'low' in js[key] and 'high' in js[key] and 'volume' in js[key]:
            dataset.append([
                    js[key]['open'],
                    js[key]['close'],
                    js[key]['low'],
                    js[key]['high'],
                    js[key]['volume'],
                ])
            i += 1
        else:
            # most likely some missing interval
            print("missing data at interval:")
            print(key)
            #print(js[key])
            logErr = createLogger("predictions_v1_error", "predictions_v1_error")
            logErr.critical("missing data at interval:")
            logErr.critical(key)
            #logErr.critical(js[key])
            # raise

    dataset= np.array(dataset)
    return dataset


def func_ai_b(js, symbol):
    # another type of input format, whereby we also make it predict buy/sell positions.
    # this is highly experimental and yielded bad results
    # but it may illustrate how such a thing is done in caee you need to extend your own version.

    dataset = [] #[()] * len(js)
    i=0
    for key in js: # DO NOT USE RELATIVE VALUES FROM API !!! only absolute ones
        if 'open' in js[key] and 'close' in js[key] and 'low' in js[key] and 'high' in js[key] and 'volume' in js[key]:
            dataset.append([
                    js[key]['open'],
                    js[key]['close'],
                    js[key]['low'],
                    js[key]['high'],
                    js[key]['volume'],
                ])
            i += 1
        else:
            # most likely some missing interval
            print("missing data at interval:")
            print(key)
            #print(js[key])
            logErr = createLogger("predictions_v1_error", "predictions_v1_error")
            logErr.critical("missing data at interval:")
            logErr.critical(key)
            #logErr.critical(js[key])
            # raise

    # in this 
    L = len(dataset)
    Lentry = len(dataset[0])
    for i, x in enumerate(dataset):
        #print(i)
        price = (x[0]+x[1])/2 # avg(open ; close)
        j = i+1
        jarr = []
        while j < L and j < 20:
            futurePrice = (dataset[j][0]+dataset[j][1])/2
            if futurePrice >= price * 1.005: # if price in near future increases by 0.5%
                jarr.append(j) # if we can make a profit by buying 'now' and selling at some interval 'j', then record this
            j += 1
        if len(x) == Lentry: # if we haven't added the signal yet
            if len(jarr) >= 1: # if we have at least X intervals in the future where we can sell (are we looking for a new plateau or temporary spike?)
                x.append(1) # buy
                for j in jarr:
                    if len(dataset[j]) == Lentry:
                        dataset[j].append(2) # sell

                for j in range(i+1, max(jarr)):
                    if len(dataset[j]) == Lentry:
                        dataset[j].append(0) # hold -- fill all gaps between first buy and possible future sells
                
            else:
                x.append(0) # hold

    # pprint.pprint(dataset[i:20])
    # exit()
            

    dataset= np.array(dataset)
    return dataset


def makeDatasets():
    datasets = {}
    datasets['func_ai_a']= func_ai_a
    return datasets

def modelExists(h5fn):
    return os.path.isfile(h5fn+'.h5')

def loadModelAndWeights(h5fn):
    from keras.models import load_model
    model = load_model(h5fn+'.h5', compile=True)
    model.load_weights(h5fn+' weights.h5')
    return model

def saveModel(h5fn, model):
    model.save(h5fn+'.h5')
    
def saveWeights(h5fn, model):
    model.save_weights(h5fn+' weights.h5')

def createModel(h5fn, n_neuron, n_hiddenlay, n_features, n_window, seq_pred_len):
    # call this function only in a new process, not in separate threads !!!
    from keras.models import Sequential
    from keras.layers.core import Dense, Activation, Dropout, Flatten
    from keras.layers.normalization import BatchNormalization
    from keras.layers import Dense, LSTM, Masking

    model = Sequential()
    #model.add(Masking(mask_value=0, input_shape=(n_features, n_window)  )) # this  could messup our signals '0-1-2' , since 0 means hold
    
    # model.add(LSTM(n_neuron, return_sequences=True,  ))
    # for i in range(n_hiddenlay):
    #     model.add(LSTM(n_neuron, return_sequences=True,  ))

    if n_hiddenlay == 2:
        model.add(LSTM(5, return_sequences=True,  input_shape=(n_features, n_window)))
        model.add(Dropout(0.3))
        model.add(LSTM(3, return_sequences=True,  ))
        model.add(Dropout(0.2))
        model.add(LSTM(3, return_sequences=True,  ))
        model.add(Dropout(0.2))
        model.add(LSTM(5, return_sequences=True,  ))
        model.add(Dropout(0.2))

    if n_hiddenlay == 1: # default: recommended single layer with multiple neurons
        model.add(LSTM(5, return_sequences=True,  input_shape=(n_features, n_window)))
        model.add(Dropout(0.2))
    
    
    
    model.add(Dense(1*seq_pred_len)) # number of outputs
    model.add(Activation("linear"))
    model.compile(loss='mae', optimizer='adam') #accuracy not relevant for regression of timeseries
    
    #print(h5fn)
    return model

def adjustDatetime(interval, currentDateTime):
    # if the datetime is not rounded to the given interval parameter, we'll do it here.
    if interval <= 60:
        return currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % interval), second=0, microsecond=0) #"2018-01-26T12:00"
    else: 
        return currentDateTime.replace(hour=currentDateTime.hour-(currentDateTime.hour % int(interval/60)), minute=currentDateTime.minute-(currentDateTime.minute % 60), second=0, microsecond=0) #"2018-01-26T12:00"

def adjustDatetime_realtime(interval, currentDateTime):
    return currentDateTime

def train_predict(args = sys.argv):

    # we need to generate every possible combination of our configuration, let's pre-process it.
    # we basically create and store tuples in an array.
    # the array will be processed in a multi-processing fashion.
    # we don't want to parallellize every possible combination, 
    # but instead we want to have max 6 to 9 processes running at the same time.
    # that's why at the deepest level we have a "uid" which acts as separator.

    # this is an important part, because if you have many different combinations you want to try out (e.g. different epochs and neuron counts),
    # then you want to make sure the processes don't take too long or make the server crash due to too many processes (or memory consumption).

    for HH in range(HH_max):
        for exchange in sorted(exchanges):
            for symbol in sorted(symbols, key=lambda x: x['base_cur']):
                for featuresID, dataset_func in datasets.items():
                    for n_window in n_windows:
                        for interval in intervals:
                            for n_epoch in n_epochs:
                                for n_neuron in n_neurons:
                                    for n_hiddenlay in n_hiddenlayers:
                                        for n_batch_size in n_batch_sizes:
                                            for predict_n_intervals in predict_n_intervals_arr:
                                    
                                                h5fn =  h5Dir + 'predictions_v1' + ' base_cur='+symbol['base_cur']+ ' base_cur='+symbol['quote_cur'] + ' fid='+featuresID + ' interval='+str(interval) + ' n_window='+str(n_window) + ' n_epoch='+str(n_epoch) + ' n_batch_size='+str(n_batch_size) + ' n_neuron='+str(n_neuron) + ' predict_n_intervals='+str(predict_n_intervals) + ' n_hiddenlay='+str(n_hiddenlay)
                                                _dtime = adjustDatetime_realtime(interval,  dtstart + timedelta(minutes=HH*interval) )

                                                uid = symbol['base_cur']#+"_"+symbol['quote_cur']+"_"+str(n_neuron)+"_"+str(n_window) # way to parallellize processing
                                                if not uid in arrParams:
                                                    arrParams[uid] = []
                                                arrParams[uid].append( (h5fn, featuresID, exchange, symbol, n_window, interval, _dtime, predict_n_intervals, n_neuron, n_hiddenlay, n_epoch, n_batch_size, dataset_func, sync_dict_json, sync_list_output, seq_pred_len) )

    # now that we have our magical array of jobs/tasks,
    # let's create a processing pool and execute all jobs accordingly.

    tasks = {}
    pools = {}
    for idf, arr in arrParams.items():
        tasks[idf] = [];
        if not idf in pools:
        	pools[idf] = multiprocessing.Pool( 1 )
        for tup in arr:
            tasks[idf].append( pools[idf].apply_async(fitAndPredict_trainAlways, tup) )

    client = DAL.openConnection()
    DAL.liveness_IAmAlive(client, "producer: predictions")

    for idf, arr in tasks.items():
        for task in arr:
            try:
                task.get(timeout=60*20)
            except KeyboardInterrupt:
                raise
            except:
                traceback.print_exc()
                
        pools[idf].close()
    
    for sendobj in sync_list_output:
        DAL.store_predictions_v1(client, sendobj)

    print("/performance/")
    print("started:")
    print(_dtnow)
    print("ended:")
    print(dtNow())
    print("/exited/")
    print("")

    log = createLogger("predictions_v1_info", "predictions_v1_info")
    log.info("/performance/")
    log.info("started:")
    log.info(str(_dtnow))
    log.info("ended:")
    log.info(str(dtNow()))
    log.info("/exited/")
    log.info("")

if __name__ == '__main__':
    args = sys.argv
    # we need to know the interval (10 minutes or 60 minutes): {10,60}
    if len(args) < 2:
        print("missing interval param")
        exit()

    # parameters:
    exchanges = ['binance']
    # crypto currencies: (as defined by the exchange, and accessible through our API)
    symbols = [
        {'base_cur':'BTC', 'quote_cur':'USDT'},
        {'base_cur':'ETH', 'quote_cur':'USDT'},
        {'base_cur':'LTC', 'quote_cur':'USDT'},

        {'base_cur':'BCC', 'quote_cur':'USDT'}, # bitcoin cash (bcc ~ bch)
        {'base_cur':'NEO', 'quote_cur':'USDT'}, 
    ] # testing
    seq_pred_len = 1
    predict_n_intervals_arr = [12]
    n_windows = [32] 
    n_neurons= [2] 
    n_hiddenlayers = [1]
    n_epochs= [1000]
    intervals = [  int(args[1]), ]
    n_batch_sizes = [512,]
    datasets = makeDatasets() 
    _dtnow = dtNow()
    pmanager = multiprocessing.Manager()
    sync_dict_json = pmanager.dict()
    sync_list_output = pmanager.list()
    arrParams = {}
    threads = []

    HH_max = 1
    dtstart = dtNow()

    #dtstart = datetime.strptime('2018-04-07 15:00', '%Y-%m-%d %H:%M')
    #HH_max = 20 # --> dtstart + ( i in HH_max) * interval

    train_predict()
        
