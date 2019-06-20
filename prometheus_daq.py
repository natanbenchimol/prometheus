
import time
import threading

import prometheus_consts as CONST
import prometheus_data_processing as data
import prometheus_shared as shared
import abort_sequences as aborts

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
#       Test try/catch block for abort
#       Soleniod actuation to actually launch system


MAX_VAL = 700   # example for testing


def readPT(batch_id, PT_DATA, pt_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = batch_id       # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()   # float - time data point collected (unix time)
    res_list[2] = pt_id         # str   - instrument id
    res_list[3] = 1             # float - data collected from PT

    if (res_list[3] > MAX_VAL):
        PT_DATA.append(res_list)  # So we know what val caused the abort
        raise aborts.PressureAbort       # ABORT!!

    PT_DATA.append(res_list)  # Save on stack to write to file later

    shared.LIVE_DATA[pt_id] = res_list[3]  # Send to val to display on GUI


def readTC(batch_id, TC_DATA, tc_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = batch_id           # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()       # float - time data point collected (unix time)
    res_list[2] = tc_id             # str   - instrument id
    res_list[3] = 1                 # float - data collected from TC

    if (res_list[3] > MAX_VAL):
        TC_DATA.append(res_list)    # So we know what val caused the abort
        raise aborts.TempAbort             # ABORT!!

    TC_DATA.append(res_list)        # Save on stack to write to file later

    shared.LIVE_DATA[tc_id] = res_list[3]   # Send to val to display on GUI


def readFM(batch_id, FM_DATA, fm_id):
    res_list = [None] * 4

    # get result from id from FM protocol

    res_list[0] = batch_id          # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()       # float - time data point collected (unix time)
    res_list[2] = fm_id             # str   - instrument id
    res_list[3] = 1                 # float - data collected from TC

    if (res_list[3] > MAX_VAL):
        FM_DATA.append(res_list)    # So we know what val caused the abort
        raise aborts.TempAbort             # ABORT!!

    FM_DATA.append(res_list)        # Save on stack to write to file later

    shared.LIVE_DATA[fm_id] = res_list[3]   # Send to val to display on GUI


def batch_reader(hz, prom_status, DATA, INSTRUMENT_NAMES, reader_func):

    data_id_count = 0
    while(prom_status["isFiring"]):

        threads = []

        # Creates all the threads to be executed, starts them, adds them to a list
        for instrument_name in INSTRUMENT_NAMES:
            inst_thread = threading.Thread(target=reader_func, args=(data_id_count, DATA, instrument_name))
            inst_thread.start()             # Start the thread
            threads.append(inst_thread)     # Add to list

        # Joins all the threads, wait until they are done executing
        for t in threads:
            t.join()

        # We will only reach here once all the threads are completed
        data_id_count += 1
        time.sleep(1 / hz)


# Function only for testing
def timeFire(timer, prom_status):
    print("START TIMER")
    time.sleep(timer)
    prom_status["isFiring"] = False
    print("END FIRE")


def main():
    global TC_DATA
    global PT_DATA

    prom_status = {}
    prom_status["isFiring"] = False

    STATUS = "PREFIRE"
    firingTime = 3

    while(STATUS.upper() != "FIRE"):
        STATUS = input("> ")

    shared.COUNTDOWN_START = time.time()
    prom_status["isFiring"] = True
    stopFireThread = threading.Thread(target=timeFire, args=(firingTime, prom_status))

    ptThread = threading.Thread(target=batch_reader, args=(CONST.PT_HZ, prom_status, shared.PT_DATA, CONST.PT_NAMES, readPT))
    tcThread = threading.Thread(target=batch_reader, args=(CONST.TC_HZ, prom_status, shared.TC_DATA, CONST.TC_NAMES, readTC))
    fmThread = threading.Thread(target=batch_reader, args=(CONST.FM_HZ, prom_status, shared.FM_DATA, CONST.FM_NAMES, readFM))

    try:
        ptThread.start()
        tcThread.start()
        fmThread.start()
        stopFireThread.start()

        ptThread.join()
        tcThread.join()
        fmThread.join()
        stopFireThread.join()

    except aborts.Abort:
        print("Handle Abort")

    data.writeToFile(shared.COUNTDOWN_START, shared.TC_DATA, shared.PT_DATA, shared.FM_DATA)


main()

#
# # Base abort class, pure virtual
# class Abort(Exception):
#     # Basic abort
#     pass
#
#
# # Example of how we could make a different exception
# # for each abort scenario and handle it automatically using OOP
# class PressureAbort(Abort):
#     pass
#
# class TempAbort(Abort):
#     pass
#

