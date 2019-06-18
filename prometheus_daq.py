
import time
import threading
import datetime
import csv
import os

#from .abort_sequences import Abort

# NOTE!!!!!
#
#   The daq is not yet linked to the front end!
#   Still in testing phase!
#   Currently using FAKE data to ensure data flow is solid
#
# END OF NOTE

#TODO:  PRESSING ISSUES
#       Learn debugger!!! Important for MT func.

#TODO:  FUTURE FUNCTIONALITY
#       Write data processing
#       Test try/catch block for abort
#       Reaarange global vars -> which files should they go in

TC_NAMES = ["TC1_IP", "TC2_IP", "TC1_IF", "TC_I", "TC1_IO", "TC2_IO", "TC3_IO"]
PT_NAMES = ["PT1_IP", "PT2_IP", "PT1_IF", "PT2_IF", "PT_I", "PT1_IO", "PT2_IO", "PT3_IO"]

TC_HZ = 150
PT_HZ = 150

TC_DATA = []    # to be written to file
PT_DATA = []

LIVE_DATA = {}   # contains the most recent reading

MAX_VAL = 700   # example for testing

def readPT(data_id, PT_DATA, pt_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = data_id       # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()   # float - time data point collected (unix time)
    res_list[2] = pt_id         # str   - instrument id
    res_list[3] = 1             # float - data collected from PT

    if (res_list[3] > MAX_VAL):
        PT_DATA.append(res_list)  # So we know what val caused the abort
        raise PressureAbort     # ABORT!!

    PT_DATA.append(res_list)  # Save on stack to write to file later

    LIVE_DATA[pt_id] = res_list[3]  # Send to val to display on GUI

def readTC(data_id, TC_DATA, tc_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = data_id           # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()       # float - time data point collected (unix time)
    res_list[2] = tc_id             # str   - instrument id
    res_list[3] = 1                 # float - data collected from TC

    if (res_list[3] > MAX_VAL):
        TC_DATA.append(res_list)    # So we know what val caused the abort
        raise TempAbort             # ABORT!!

    TC_DATA.append(res_list)        # Save on stack to write to file later

    LIVE_DATA[tc_id] = res_list[3]   # Send to val to display on GUI

def tcReader(hz, prom_status):
    global TC_DATA

    data_id_count = 0
    while(prom_status["isFiring"]):

        threads = []

        # Creates all the threads to be executed, adds them to a list
        for tc in TC_NAMES:
            tc_thread = threading.Thread(target=readTC, args=(data_id_count, TC_DATA, tc))
            threads.append(tc_thread)

        # Starts all the threads in the list
        for t in threads:
            t.start()

        # Joins all the threads, wait until they are done executing
        for t in threads:
            t.join()

        # We will only reach here once all the threads are completed
        data_id_count += 1
        time.sleep(1 / hz)


def ptReader(hz, prom_status):
    global PT_DATA

    data_id_count = 0
    while(prom_status["isFiring"]):

        threads = []

        # Creates all the threads to be executed, adds them to a list, runs them
        for pt in PT_NAMES:
            pt_thread = threading.Thread(target=readTC, args=(data_id_count, PT_DATA, pt))
            threads.append(pt_thread)
            pt_thread.start()

        # Joins all the threads, wait until they are done executing
        for t in threads:
            t.join()

        # We will only reach here once all the threads are completed
        data_id_count += 1
        time.sleep(1 / hz)      # SET BY USER ON FRONTEND

def writeToFile():
    global TC_DATA
    global PT_DATA

    # Sort data in case threading messed anything up
    TC_DATA.sort(key=lambda tup: tup[2])
    PT_DATA.sort(key=lambda tup: tup[2])
    TC_DATA.sort(key=lambda tup: tup[0])
    PT_DATA.sort(key=lambda tup: tup[0])

    # Directory management
    cwd = os.getcwd()
    if not os.path.exists(cwd + "/Data/"):
        os.makedirs(cwd + "/Data/")

    # General housekeeping
    currentDT = datetime.datetime.now()  # Gets current time
    print("Num of TC data points = " + str(len(TC_DATA)))
    print("Num of PT data points = " + str(len(PT_DATA)))

    # ----------- Writing Raw Data ----------- #

    # Open the file
    raw_tc_file = open("Data/promRawTC_" + currentDT.strftime("%Y-%m-%d_%H-%M-%S") +".csv", "w")
    raw_pt_file = open("Data/promRawPT_" + currentDT.strftime("%Y-%m-%d_%H-%M-%S") +".csv", "w")

    # Create the CSV writers
    tcWriter = csv.writer(raw_tc_file)
    ptWriter = csv.writer(raw_pt_file)

    # Write the raw data
    for list in TC_DATA:
        tcWriter.writerow(list)
    for list in PT_DATA:
        ptWriter.writerow(list)

    # Close raw files
    raw_tc_file.close()
    raw_pt_file.close()

    # ----------- Processing Data ----------- #

    header_row_pt = ["num","avgTime"] + PT_NAMES
    header_row_tc = ["num","avgTime"] + TC_NAMES

    clean_tc_file = open("Data/promCleanTC_" + currentDT.strftime("%Y-%m-%d_%H-%M-%S") +".csv", "w")
    tcWriter = csv.writer(clean_tc_file)
    tcWriter.writerow(header_row_tc)

    tcAvgTime = {}
    ptAvgTime = {}

    # For each tc reading
    for reading in TC_DATA:
        # Sum up all the times at the same index
        if reading[0] in tcAvgTime:
            tcAvgTime[reading[0]] += reading[1]
        else:
            tcAvgTime[reading[0]] = reading[1]
    # Use the sum of the times to calculate average time
    for total in tcAvgTime:
        tcAvgTime[total] = tcAvgTime[total]/len(TC_NAMES)


    for i in tcAvgTime:
        to_write = [None] * len(header_row_tc)
        to_write[0] = i
        to_write[1] = tcAvgTime[i]

        # This for loop is super confusing, sorry
        for j in range((i*len(TC_NAMES)) + len(TC_NAMES)):
            to_write[header_row_tc.index(TC_DATA[j][2])] = TC_DATA[j][3]

        tcWriter.writerow(to_write)

    clean_tc_file.close()
    # ----------- Writing Clean Data ----------- #

    # clean_pt_file = open("Data/promCleanPT_" + currentDT.strftime("%Y-%m-%d_%H-%M-%S") +".csv", "w")


# Function only for testing
def timeFire(timer, prom_status):
    time.sleep(timer)
    prom_status["isFiring"] = False


def main():
    global TC_DATA
    global PT_DATA

    prom_status = {}
    prom_status["isFiring"] = False

    STATUS = "PREFIRE"
    firingTime = 3

    while(STATUS.upper() != "FIRE"):
        STATUS = input("> ")

    prom_status["isFiring"] = True
    stopFireThread = threading.Thread(target=timeFire, args=(firingTime, prom_status))

    ptThread = threading.Thread(target=ptReader, args=(PT_HZ, prom_status))
    tcThread = threading.Thread(target=tcReader, args=(TC_HZ, prom_status))

    try:
        ptThread.start()
        tcThread.start()
        stopFireThread.start()

        ptThread.join()
        tcThread.join()
        stopFireThread.join()

    except Abort:
        print("Handle Abort")

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

class TempAbort(Abort):
    pass