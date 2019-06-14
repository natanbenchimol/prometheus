
import time
import threading
import datetime
import csv


#TODO:  Write try/catch block for abort
#       STATUS update not read inside threads -> while loop condition always false
#       Move the checks and saving into the single Read thread?!?!?
#       Get csv working


STATUS = ""
TC_DATA = []    # to be written to file
PT_DATA = []

liveData = {}   # contains the most recent reading

MAX_VAL = 700

def readPT(id):
    # get result from id from PT protocol
    return (time.time(), id, 1)

def readTC(id):
    # get id from TC protocol
    return (time.time(), id, 0)

def tcReader(hz):
    print("in TC")
    while(STATUS == "FIRE"):
        time.sleep(1 / hz)  # Mimic protocol latency

        for i in range(8):
            t1 = threading.Thread(target=readTC, args=[i])
            resTuple = t1.start()   # Gets the data

            if(resTuple[2] > MAX_VAL):  # Check for abort
                # ABORT!!!
                pass

            TC_DATA.append(resTuple)    # Save on stack to write to file later

            liveData[i] = resTuple[2]   # Send to val to display on GUI

def ptReader(hz):
    print("in PT")
    print(STATUS == "FIRE")
    while(STATUS == "FIRE"):
        print(";")
        time.sleep(1 / hz)  # Mimic protocol latency

        for i in range(8):
            t1 = threading.Thread(target=readPT, args=[i])
            resTuple = t1.start()   # Gets the data

            if(resTuple[2] > MAX_VAL):  # Check for abort
                # ABORT!!!
                pass

            print(resTuple[2])

            PT_DATA.append(resTuple)    # Save on stack to write to file later

            liveData[i] = resTuple[2]   # Send to val to display on GUI

def writeToFile():
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
    STATUS = ""

def main():
    STATUS = ""
    firingTime = 3

    while(STATUS.upper() != "FIRE"):
        STATUS = input("> ")


    # try catch
    stopFireThread = threading.Thread(target=timeFire, args=[firingTime])
    ptThread = threading.Thread(target=ptReader, args=[2])
    tcThread = threading.Thread(target=tcReader, args=[100])
    ptThread.start()
    tcThread.start()
    stopFireThread.start()

    ptThread.join()
    tcThread.join()
    stopFireThread.join()

    writeToFile()


main()
