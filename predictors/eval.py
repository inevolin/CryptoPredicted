import json
import urllib.request
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/home/nevolin/public_html/cryptoproto/')
from mysettings import dtNow, createLogger
from collections import OrderedDict

from numpy import array, zeros, argmin, inf, equal, ndim
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import manhattan_distances

def dtw(x, y, dist):
    """
    Computes Dynamic Time Warping (DTW) of two sequences.
    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure
    Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
    """
    assert len(x)
    assert len(y)
    r, c = len(x), len(y)
    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:] # view
    for i in range(r):
        for j in range(c):
            D1[i, j] = dist(x[i], y[j])
    C = D1.copy()
    for i in range(r):
        for j in range(c):
            D1[i, j] += min(D0[i, j], D0[i, j+1], D0[i+1, j])
    if len(x)==1:
        path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), zeros(len(x))
    else:
        path = _traceback(D0)
    return D1[-1, -1] / sum(D1.shape), C, D1, path

def _traceback(D):
    i, j = array(D.shape) - 2
    p, q = [i], [j]
    while ((i > 0) or (j > 0)):
        tb = argmin((D[i, j], D[i, j+1], D[i+1, j]))
        if (tb == 0):
            i -= 1
            j -= 1
        elif (tb == 1):
            i -= 1
        else: # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return array(p), array(q)


def eval(currentDateTime):
	currentDateTime = currentDateTime.replace(minute=currentDateTime.minute-(currentDateTime.minute % interval))
	currentDateTime_T = datetime.strftime(currentDateTime, '%Y-%m-%dT%H:%M')
	print(str(currentDateTime_T))
	url = "http://cryptopredicted.com/api.php?type=predictionChart3&coin="+coin+"&interval="+str(interval)+"&historymins=360&currentDateTime="+currentDateTime_T+"&featuresID=-1&batchsize=-1&neurons=-1&windowsize=-1&epochs=-1&hiddenlayers=-1&predicted_feature=price3"
	print(url)
	out = urllib.request.urlopen(url)
	js = json.loads(out.read().decode(out.info().get_param('charset') or 'utf-8'), object_pairs_hook=OrderedDict)

	arrA = list(js['history_extended'].values())[:8]
	print(arrA)
	buckets = {}
	for uid, vals in js['predictions'].items():
		it = 0
		arrP = list(vals.values())[:8]

		dist_fun = manhattan_distances
		dist, cost, acc, path = dtw(arrA, arrP, dist_fun)
		print(uid +"\t==>\t"+str(dist)) # the smaller the dist the better. dist==0 if both A and B are equal
		if not uid in buckets: buckets[uid]=[]
		buckets[uid].append(dist)

	return buckets


import threading
class evalProcessor (threading.Thread):
	def __init__(self, currentDateTime, evals):
		threading.Thread.__init__(self)
		self.currentDateTime = currentDateTime
		self.evals = evals

	def run(self):
		bucket = eval(self.currentDateTime)
		for uid, arr in bucket.items():
			if uid not in self.evals:
				self.evals[uid] = []
			for a in arr:
				self.evals[uid].append(a)



coin = "BTC"
interval=10
#currentDateTime = dtNow().replace(second=0,microsecond=0) - timedelta(minutes=interval*8)
dtstart = datetime.strptime('2018-02-20 00:00', '%Y-%m-%d %H:%M')
dtend = datetime.strptime('2018-02-28 23:50', '%Y-%m-%d %H:%M')
dtit = dtstart


evals = {}
threads = []
while(dtit <= dtend):
	th = evalProcessor(dtit, evals)
	th.start()
	threads.append(th)
	if len(threads) == 8:
		for t in threads:
			try:
				t.join(timeout=30) # 30 sec per article
			except Exception as ex:
				print(ex)
		threads=[]

	dtit += timedelta(minutes=interval)

for t in threads:
	try:
		t.join(timeout=30) # 30 sec per article
	except Exception as ex:
		print(ex)

print("==================")
print("==================")
print(json.dumps(evals))
print("==================")
print("==================")
min_avg = None
min_uid = None
for uid, arr in evals.items():
	avg = sum(arr)/len(arr)
	print(uid +"\t==avg==>\t"+ str(avg))
	if min_avg == None or avg < min_avg:
		min_avg = avg
		min_uid=uid

print("---")
print("min_avg = " + str(min_avg))
print("min_uid = " + min_uid)
