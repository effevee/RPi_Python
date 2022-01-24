from multiprocessing import Process
import time
import os

def newProcess(processNum, pauze):
    while True:
        print("ik ben proces {} met PID {}: ".format(processNum, os.getpid()))
        time.sleep(pauze)
        
def otherProcess():
    while True:
        print("ik ben ander proces met PID {}".format(os.getpid()))
        time.sleep(0.5)
        
print("parent PID {}".format(os.getpid()))

p0 = Process(target=otherProcess, args=())   # maken proces p0
p1 = Process(target=newProcess, args=(1,2,))  # maken proces p1
p2 = Process(target=newProcess, args=(2,5,))  # maken proces p2

# starten van processen p0, p1 en p2
p0.start()
p1.start()
p2.start()

print("de processen zijn gestart")