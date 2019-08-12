
import time
import threading
import os
import datetime

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

#TODO:  LETS GET IT
#       Write firing function
#       Draw out an import structure tree
#       TC/PT Read code
#       FM code

#TODO:  FUTURE FUNCTIONALITY
#       Soleniod actuation to actually launch system
#       Import tree structure documentation


MAX_VAL = 700   # example for testing


def readPT(batch_id, PT_DATA, pt_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = batch_id       # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()   # float - time data point collected (unix time)
    res_list[2] = pt_id         # str   - instrument id
    res_list[3] = 4005             # float - data collected from PT

    if (res_list[3] > MAX_VAL):
        PT_DATA.append(res_list)  # So we know what val caused the abort
        raise aborts.PressureAbort       # ABORT!!

    PT_DATA.append(res_list)  # Save on stack to write to file later

    shared.LIVE_DATA[pt_id] = res_list[3]  # Send to val to display on GUI


def readTC(batch_id, TC_DATA, tc_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = batch_id          # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()       # float - time data point collected (unix time)
    res_list[2] = tc_id             # str   - instrument id
    res_list[3] = 224                  # float - data collected from TC

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
    res_list[3] = 6.02              # float - data collected from FM

    if (res_list[3] > MAX_VAL):
        FM_DATA.append(res_list)    # So we know what val caused the abort
        raise aborts.TempAbort             # ABORT!!

    FM_DATA.append(res_list)        # Save on stack to write to file later

    shared.LIVE_DATA[fm_id] = res_list[3]   # Send to val to display on GUI


def batch_reader(hz, prom_status, DATA, INSTRUMENT_NAMES, reader_func):

    data_id_count = 0
    while(prom_status["shouldRecordData"]):

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


# Function creates the list of pairs + orders them for firing
def fire_timings():
    # need to parse through shared
    pass


# Called as a part of pre fire checklist
def prefire_checks_and_setup():

    # ---------------- AUTOMATIC PRE-FIRE CHECKS ---------------- #

    # Checks that all our abort gates are populated and they make sense
    for gate in shared.FM_ABORT_GATES + shared.TC_ABORT_GATES + shared.PT_ABORT_GATES:
        if not gate.is_valid_gate():
            print("Prematurely Aborting Fire")
            return

    if (CONST.TC_HZ):

        pass

    # Initialize the LIVE_VALS dictionary with values: int, will be filled in during fire
    shared.init_live_data()

    # Create fire sequence
    for key in shared.FRONT_END_TIMINGS:
        pass # Do soemthing idk holy shit


# Fire function
def fire():

    prom_status = {}
    prom_status["should_record_data"] = True
    prom_status["did_abort"] = False
    prom_status["countdown_start"] = time.time()

    cwd = os.getcwd()                                           # Get current working directory
    current_dt = datetime.datetime.now()                        # Get current time
    formatted_date = current_dt.strftime("%Y-%m-%d_%H-%M-%S")   # Format time
    prom_status["base_file_path"] = cwd + "/Data/" + formatted_date         # Directory where we will save our data

    logfile = open("logfile_"+formatted_date)
    write_log_header(logfile, prom_status)

    pt_thread = threading.Thread(target=batch_reader, args=(CONST.PT_HZ, prom_status, shared.PT_DATA, CONST.PT_NAMES, readPT))
    tc_thread = threading.Thread(target=batch_reader, args=(CONST.TC_HZ, prom_status, shared.TC_DATA, CONST.TC_NAMES, readTC))
    fm_thread = threading.Thread(target=batch_reader, args=(CONST.FM_HZ, prom_status, shared.FM_DATA, CONST.FM_NAMES, readFM))

    # Maybe a list of pairs with (timings, functions/actions)
    # sorted by timings, go through array executing functions after waiting for their times
    # fire_procedure = [] <- create_proc()

    shared.COUNTDOWN_START = time.time()

    try:
        pt_thread.start()
        tc_thread.start()
        fm_thread.start()
        print("Proceed with fire")

        # Here's where all our shit goes DOWN

        pt_thread.join()
        tc_thread.join()
        fm_thread.join()

    except aborts.Abort:
        print("Handle Abort")
        # Some solenoid state change
        prom_status["shouldRecordData"] = False # stop spawning the reader threads

    data.writeToFile(prom_status, shared.TC_DATA, shared.PT_DATA, shared.FM_DATA)
    write_log_footer(logfile, prom_status)

    # notify that firing is complete
    # begin data processing
    # notify that data processing is complete


def purge(time):
    pass

def write_log_header(logfile, prom_status):
    pass

def write_log_event(logfile):
    pass

def write_log_footer(logfile, prom_status):
    pass

def main():

    prom_status = {}
    prom_status["isFiring"] = False

    STATUS = "PREFIRE"
    firingTime = 15

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
        prom_status["isFiring"] = False

    data.writeToFile(shared.COUNTDOWN_START, shared.TC_DATA, shared.PT_DATA, shared.FM_DATA)


main()
