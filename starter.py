import subprocess
import sys
import os, signal
from os import listdir
from os.path import isfile, join
import time

import sys
import os
sys.path.insert(0, '/home/cryptopredicted/')
from mysettings import kafkaTopic_mentionsSocial, kafkaTopic_mentionsNews

rootDir = '/home/cryptopredicted/'
logsDir = '/home/cryptopredicted/logs/'
producersDir = '/home/cryptopredicted/producers/'
consumersDir = '/home/cryptopredicted/consumers/'

myProducers = [f for f in listdir(producersDir) if isfile(join(producersDir, f)) and f.endswith(".py") ]
myConsumers = [f for f in listdir(consumersDir) if isfile(join(consumersDir, f)) and f.endswith(".py") ]

def prompt(msg):
    print("")
    print(msg + "  (no)")
    yes = {'yes','y', 'ye'}

    choice = input().lower()
    if choice in yes:
       return True
    return False

def startProc(inp, out=subprocess.DEVNULL, err=subprocess.DEVNULL):
    print(inp)
    if len(sys.argv) == 2 and sys.argv[1] == 'f':
        print('  '+"   starting...")
        subprocess.Popen(inp, shell=True, stdout=out, stderr=err) # PIPE / DEVNULL / STDOUT


def check_kill_process(pstring):
    if prompt("execute kill "+pstring+" ?"):
        for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)

if len(sys.argv) == 2 and sys.argv[1] == 'close':
    for script in myProducers:
        check_kill_process(script)
    for script in myConsumers:
        check_kill_process(script)
    check_kill_process('zookeeper')
    check_kill_process('kafka')
    print("all shutdown")


if len(sys.argv) == 2 and sys.argv[1] == 'f':
    print("--- swap memory ---")
    if prompt("execute?"):
        startProc(rootDir+"swapmem.sh")




print("--- zookeeper ---")
p = subprocess.Popen(['pgrep', '-f', 'config/zookeeper.properties'], stdout=subprocess.PIPE)
out, err = p.communicate()
if len(out.strip()) == 0:
    print('  zookeeper: OFFLINE')
    if len(sys.argv) == 2 and sys.argv[1] == 'f':
        if prompt("execute?"):
            print("starting zookeeper ...")
            startProc("$KAFKA_HOME/bin/zookeeper-server-start.sh -daemon $KAFKA_HOME/config/zookeeper.properties")
            print(" ... 5 sec timeout ... ")
            time.sleep(5)
else:
    print('  zookeeper: OK')




print("--- kafka ---")
p = subprocess.Popen(['pgrep', '-f', 'config/server.properties'], stdout=subprocess.PIPE)
out, err = p.communicate()
if len(out.strip()) == 0:
    print('  kafka: OFFLINE')
    if len(sys.argv) == 2 and sys.argv[1] == 'f':
        if prompt("execute?"):
            print("starting kafka and creating topics ...")
            startProc("$KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties")
            print(" ... 5 sec timeout ... ")
            time.sleep(5)
            startProc("/etc/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 4 --topic " + kafkaTopic_mentionsSocial)
            startProc("/etc/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 4 --topic " + kafkaTopic_mentionsNews)
            print(" ... 3 sec timeout ... ")
            time.sleep(3)
else:
    print('  kafka: OK')




# starting kafka takes some time and happens async; so all other processes will need to wait somehow...
print()
print("=== producers ===")
for script in myProducers:
    p = subprocess.Popen(['pgrep', '-f', script], stdout=subprocess.PIPE)
    out, err = p.communicate()
    if len(out.strip()) == 0:
        print('  '+script+": OFFLINE")
        if len(sys.argv) == 2 and sys.argv[1] == 'f':
            if prompt("execute "+script+" ?"):
                startProc('python3 ' + producersDir+script + " 1>/dev/null 2> "+logsDir+script+".stderr.log") #nohup here to prevent it from going to sleep
    else:
        print('  '+script+": OK")

print()
print("=== consumers ===")
for script in myConsumers:
    p = subprocess.Popen(['pgrep', '-f', script], stdout=subprocess.PIPE)
    out, err = p.communicate()
    if len(out.strip()) == 0:
        print('  '+script+": OFFLINE")
        if len(sys.argv) == 2 and sys.argv[1] == 'f':
            if prompt("execute "+script+" ?"):
                startProc('python3 ' + consumersDir+script + " 1>/dev/null 2> "+logsDir+script+".stderr.log") #nohup here to prevent it from going to sleep
    else:
        print('  '+script+": OK")
