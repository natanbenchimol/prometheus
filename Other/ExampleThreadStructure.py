
import time
import threading
import datetime
import csv

from queue import Queue
from .abort_sequences import Abort

#TODO:  PRESSING ISSUES
#       Learn debugger!!! Important for MT func.
#       Infnite loop(?)
#       pass results using res_list not working (deep/shallow issue?)

#TODO:  FUTURE FUNCTIONALITY
#       Test try/catch block for abort
#       Move the checks and saving into the single Read thread?!?!?
#       Get csv working
#       Are there potentially different aborts?

STATUS = "PREFIRE"

TC_NAMES = ["TC1_IP", "TC2_IP", "TC1_IF", "TC_I", "TC1_IO", "TC2_IO", "TC3_IO"]
PT_NAMES = ["PT1_IP", "PT2_IP", "PT1_IF", "PT2_IF", "PT_I", "PT1_IO", "PT2_IO", "PT3_IO"]

TC_DATA = []    # to be written to file
PT_DATA = []

liveData = {}   # contains the most recent reading

MAX_VAL = 700

def readPT(id, res_list):
    # get result from id from PT protocol
    res_list[0] = time.time()
    res_list[1] = id
    res_list[2] = 1

def readTC(id, res_list):
    # get result from id from TC protocol
    res_list[0] = time.time()
    res_list[1] = id
    res_list[2] = 1

def tcReader(hz, fireQ):
    global STATUS
    global TC_DATA

    while(fireQ.get() == "FIRE"):
        #time.sleep(1 / hz)  # Mimic protocol latency
        print("IN LOOP: " + STATUS)
        #for i in range(8):
        res_list = [-1,-1,-1]
        t1 = threading.Thread(target=readPT, args=[1, res_list])
        t1.start()  # Gets the data
        t1.join()

        if(res_list[2] > MAX_VAL):  # Check for abort
            # ABORT!!!
            raise PressureAbort

        TC_DATA.append(res_list)    # Save on stack to write to file later

        #liveData[i] = res_list[2]   # Send to val to display on GUI

def ptReader(hz):
    global STATUS
    global PT_DATA

    while(STATUS == "FIRE"):
        time.sleep(1 / hz)  # Mimic protocol latency

        for i in range(8):
            res_list = [0.1, -1, -1]
            t1 = threading.Thread(target=readPT, args=[i, res_list])
            t1.start()  # Gets the data
            t1.join()
            if(res_list[2] > MAX_VAL):  # Check for abort
                # ABORT!!!
                raise PressureAbort

            PT_DATA.append(res_list)    # Save on stack to write to file later

            liveData[i] = res_list[2]   # Send to val to display on GUI

def writeToFile():
    global TC_DATA
    global PT_DATA

    TC_DATA.sort(key=lambda tup: tup[2])    # Sort data in case threading messed anything up
    PT_DATA.sort(key=lambda tup: tup[2])

    print(len(TC_DATA))
    print(len(PT_DATA))

    currentDT = datetime.datetime.now()  # Gets current time

    # Open the files
    tcFile = open("prometheusFireTC_" + currentDT.strftime("%Y-%m-%d_%H-%M-%S") +".csv", "w")
    ptFile = open("prometheusFirePT_" + currentDT.strftime("%Y-%m-%d_%H-%M-%S") +".csv", "w")

    # Create the CSV writers
    tcWriter = csv.writer(tcFile)
    ptWriter = csv.writer(ptFile)

    # Write the data
    for tup in TC_DATA:
        print(tup)
        tcWriter.writerow(tup)
    for tup in PT_DATA:
        print(tup)
        ptWriter.writerow(tup)

    tcFile.close()
    ptFile.close()

def timeFire(timer, fireQ):
    print("Enter time fire")
    time.sleep(timer)
    fireQ.put("POSTFIRE")
    print("Sleep complete")

def main():
    global STATUS
    global TC_DATA
    global PT_DATA

    fireQ = Queue()

    STATUS = "PREFIRE"
    firingTime = 1

    while(STATUS.upper() != "FIRE"):
        STATUS = input("> ")

    fireQ.put("FIRE")
    stopFireThread = threading.Thread(target=timeFire, args=(firingTime, fireQ))
    ptThread = threading.Thread(target=ptReader, args=(2, fireQ))
    tcThread = threading.Thread(target=tcReader, args=(100, fireQ))

    try:
        #ptThread.start()
        tcThread.start()
        stopFireThread.start()

        #ptThread.join()
        tcThread.join()
        stopFireThread.join()

    except Abort:
        print("Handle Abort")

    if len(TC_DATA) > 0:        # FOR TESTING ONLY
        writeToFile()


main()


# Base abort class, pure virtual
class Abort(Exception):
    # Basic abort
    pass


# Example of how we could make a different exception
# for each abort scenario and handle it automatically using OOP
class PressureAbort(Abort):
    pass
