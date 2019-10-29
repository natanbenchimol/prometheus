
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
#       TC/PT Read code
#       FM code
#       Soleniod actuation to actually launch system


MAX_VAL = 700   # example for testing


# ---------------------- START OF DATA ACQUISITION FUNCTIONS ---------------------- #

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


def pt_protocol():
    pass


def readTC(batch_id, TC_DATA, tc_id):
    res_list = [None] * 4

    # get result from id from TC protocol

    res_list[0] = batch_id          # int   - this is the nth time we are collecting data from here
    res_list[1] = time.time()       # float - time data point collected (unix time)
    res_list[2] = tc_id             # str   - instrument id
    res_list[3] = 224                  # float - data collected from TC

    # TODO: Find best way to measure time
    # TODO: How are we passing time into our abort gate?
    if (res_list[3] > MAX_VAL):
        TC_DATA.append(res_list)    # So we know what val caused the abort
        raise aborts.TempAbort             # ABORT!!

    TC_DATA.append(res_list)        # Save on stack to write to file later

    shared.LIVE_DATA[tc_id] = res_list[3]   # Send to val to display on GUI


def tc_protocol():
    pass


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


def fm_protocol():
    pass


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

        # If we are pre/post fire, don't need max DAQ rate
        if(prom_status["overdrive"] == False):
            time.sleep(1 / hz)


# ---------------------- END OF DATA ACQUISITION FUNCTIONS ---------------------- #


# Function only for testing
def timeFire(timer, prom_status):
    print("START TIMER")
    time.sleep(timer)
    prom_status["isFiring"] = False
    print("END FIRE")


#TODO: Revisit this function
def prefire_checks_and_setup():

    # AUTOMATIC PRE-FIRE CHECKS

    # Checks that all our abort gates are populated and they make sense
    for gate in shared.FM_ABORT_GATES + shared.TC_ABORT_GATES + shared.PT_ABORT_GATES:
        if not gate.is_valid_gate():
            print("Prematurely Aborting Fire")
            return

    if (CONST.TC_HZ):

        pass

    # Initialize the LIVE_VALS dictionary with values: int, will be filled in during fire
    shared.init_live_data()


# Fire function
def fire(sol):

    prom_status = {
        "should_record_data": True,
        "overdrive": False,
        "did_abort": False,
        "countdown_start": time.time()
    }

    pt_thread = threading.Thread(target=batch_reader, args=(CONST.PT_HZ, prom_status, shared.PT_DATA, CONST.PT_NAMES, readPT))
    tc_thread = threading.Thread(target=batch_reader, args=(CONST.TC_HZ, prom_status, shared.TC_DATA, CONST.TC_NAMES, readTC))
    fm_thread = threading.Thread(target=batch_reader, args=(CONST.FM_HZ, prom_status, shared.FM_DATA, CONST.FM_NAMES, readFM))

    # Sequence is a data structure with all of the actions and timings required for the firing
    # see the load_timings() func for information about its structure
    sequence = shared.load_timings()

    shared.log_event("FIRE", "Countdown start")
    shared.COUNTDOWN_START = time.time()

    try:
        # Start the DAQ threads
        shared.log_event("DATA", "Start data collection")
        shared.log_event("DATA", "DAQ rate: REDUCED")
        pt_thread.start()
        tc_thread.start()
        fm_thread.start()

        time.sleep(CONST.PRE_FIRE_WAIT)          # Recording nominal data pre-fire at reduced rate

        shared.log_event("DATA", "DAQ rate: OVERDRIVE") # Up the DAQ rate
        prom_status["overdrive"] = True

        shared.log_event("FIRE", "Fire sequence start")
        for action in sequence:                     # All our firing sequence
            time.sleep(action[2])
            sol.solenoid_to_state(action[0], action[1])

        shared.log_event("FIRE", "Purge operations start")
        purge(sol, 3)                               # Purge
        shared.log_event("FIRE", "Purge operations complete")

        shared.log_event("DATA", "DAQ rate: REDUCED")
        prom_status["overdrive"] = False

        time.sleep(CONST.POST_FIRE_WAIT)            # Give system a few seconds to stabilize post purge

        prom_status["should_record_data"] = False   # This stops data recording and begins processing
        shared.log_event("FIRE", "End data collection")

        pt_thread.join()    # Wait for our threads to finish
        tc_thread.join()
        fm_thread.join()

    # Handle any aborts that are thrown
    except aborts.Abort:
        print("Handle Abort")
        # Some solenoid state change
        prom_status["shouldRecordData"] = False # stop spawning the reader threads
        prom_status["did_abort"] = True         # Info for logfile

    # Data processing
    file_path = data.writeToFile(prom_status, shared.TC_DATA, shared.PT_DATA, shared.FM_DATA)

    # Log file generation
    data.generate_logfile(file_path + "logfile.txt", sequence)


# Purge ops will remain almost entirely unchanged from firing to firing
# if something here need to be placed
def purge(sol, purge_duration):

    # Post fire procedure, setup for purge
    sol.solenoid_to_state("NC30", 0)            # Close ox by bottle
    # time.sleep(0.1)                           # Might need a quick sleep right here
    sol.solenoid_to_state("NC3P", 1)            # Open N2 by bottle

    # Now Purging
    time.sleep(purge_duration)
    sol.solenoid_to_state("NC3P", 0)            # Close N2 by bottle
    sol.solenoid_to_state("NCIO", 0)            # Close ox valve


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
