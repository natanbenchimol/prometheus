
import time
import threading
import datetime
import csv

import abort_sequences

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

def tcReader(hz):
    global STATUS
    global TC_DATA

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

            TC_DATA.append(res_list)    # Save on stack to write to file later

            liveData[i] = res_list[2]   # Send to val to display on GUI

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

def timeFire(timer):
    time.sleep(timer)
    STATUS = "POSTFIRE"

def main():
    global STATUS

    STATUS = "PREFIRE"
    firingTime = 1

    while(STATUS.upper() != "FIRE"):
        STATUS = input("> ")


    # try catch
    stopFireThread = threading.Thread(target=timeFire, args=[firingTime])
    ptThread = threading.Thread(target=ptReader, args=[2])
    tcThread = threading.Thread(target=tcReader, args=[100])

    try:
        ptThread.start()
        tcThread.start()
        stopFireThread.start()

        ptThread.join()
        tcThread.join()
        stopFireThread.join()
    except Abort:
        print("Handle Abort")
        pass

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
