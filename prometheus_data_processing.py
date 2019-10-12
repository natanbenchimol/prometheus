
import datetime
import os
import csv
import multiprocessing

import prometheus_consts as CONST
import prometheus_shared as shared


#TODO : Data Processing Edition
#   - SAFETY!!! Put everything in a try/catch in case exception thrown
#   - Keep iterating/refactoring


def unix_to_24h(unix) -> str:
    return datetime.datetime.fromtimestamp(
        float(unix)
    ).strftime('%H:%M:%S.%f')


def unix_to_mission_time(unix) -> float:
    return unix - shared.COUNTDOWN_START


# This sorts the raw data primarily by batch number
# but each batch is also sorted by instrument ID
# possible because Python uses a STABLE sort algorithm
def sort_raw(DATA):
    DATA.sort(key=lambda tup: tup[2])   # Sorting by instrument ID
    DATA.sort(key=lambda tup: tup[0])   # Sorting by batch number


def write_clean(csv_writer, header, RAW_DATA, INSTRUMENT_NAMES):

    batch_avg_time = {}                 # KEY: batch_number - VALUE: avg time of that batch number

    for reading in RAW_DATA:            # For each instrument reading
        if reading[0] in batch_avg_time:                  # Sum up all the times at the same index
            batch_avg_time[reading[0]] += reading[1]
        else:
            batch_avg_time[reading[0]] = reading[1]

    for total in batch_avg_time:                          # Use the sum of the times to calculate average time
        batch_avg_time[total] = batch_avg_time[total] / len(INSTRUMENT_NAMES)

    # Loops one batch at a time, creating a list for the batch, and writing it to the file
    for i in batch_avg_time:
        to_write = [None] * len(header)             # This is the list that will be written to file
        to_write[0] = i                             # Thread batch number
        to_write[1] = unix_to_24h(batch_avg_time[i])             # Avg time of batch
        to_write[2] = unix_to_mission_time(batch_avg_time[i])     # Mission time

        # I know this for loop is super confusing... sorry
        # Essentially it takes the sorted DATA, moves all of the points of a single
        # batch into the 'to_write' list. Uses .index() to find which index
        # in 'to_write' corresponds to each instrument ID and puts it there
        for j in range((i * len(INSTRUMENT_NAMES)) + len(INSTRUMENT_NAMES)):
            to_write[header.index(RAW_DATA[j][2])] = RAW_DATA[j][3]

        csv_writer.writerow(to_write)               # Write the list of data to the csv
        
        if i%1000 is 0:
            print("Processing batch num: " + str(i))


def writeToFile(COUNTDOWN_START, TC_DATA, PT_DATA, FM_DATA):
    
    print("Begin data processing")
    print(datetime.datetime.now().time())

    # ----------- General Housekeeping ----------- #

    did_throw = False                                       # True if we have an issue doing file stuff
    cwd = os.getcwd()                                       # Get current working directory
    currentDT = datetime.datetime.now()                     # Get current time

    formatted_date = currentDT.strftime("%Y-%m-%d_%H-%M-%S") # Format time
    base_file_path = cwd + "/Data/" + formatted_date         # Directory where we will save our data

    print("Num of TC data points = " + str(len(TC_DATA)))   # Printing for sanity check
    print("Num of PT data points = " + str(len(PT_DATA)))
    print("Num of FM data points = " + str(len(FM_DATA)))

    try:
        if not os.path.exists(cwd + "/Data/"):                  # Directory management
            os.makedirs(cwd + "/Data/")
        if not os.path.exists(base_file_path):
            os.makedirs(base_file_path)

    except OSError as e:
        print("ERROR: Issue making dirs in data processing, emergency save")
        print(e)
        did_throw = True
        base_file_path = cwd

    sort_raw(TC_DATA)                                    # Sort data in case threading messed up order
    sort_raw(PT_DATA)
    sort_raw(FM_DATA)

    # ----------- Writing Raw Data ----------- #
    print("Writing raw data")

    # Open the file
    raw_tc_file = open(base_file_path + "/promRawTC_" + formatted_date +".csv", "w")
    raw_pt_file = open(base_file_path + "/promRawPT_" + formatted_date +".csv", "w")
    raw_fm_file = open(base_file_path + "/promRawFM_" + formatted_date +".csv", "w")

    # Create the CSV writers
    tcWriter = csv.writer(raw_tc_file)
    ptWriter = csv.writer(raw_pt_file)
    fmWriter = csv.writer(raw_fm_file)

    # Write the raw data
    for data_point in TC_DATA:
        tcWriter.writerow(data_point)
    for data_point in PT_DATA:
        ptWriter.writerow(data_point)
    for data_point in FM_DATA:
        fmWriter.writerow(data_point)

    # Close raw files
    raw_tc_file.close()
    raw_pt_file.close()
    raw_fm_file.close()

    # ----------- Processing Data, Write to Clean Files ----------- #

    if did_throw:   # We don't want to write the clean files if we almost crashed creating dirs
        return

    header_row_pt = ["Batch Num","Avg. Time", "Mission Time"] + CONST.PT_NAMES
    header_row_tc = ["Batch Num","Avg. Time", "Mission Time"] + CONST.TC_NAMES
    header_row_fm = ["Batch Num","Avg. Time", "Mission Time"] + CONST.FM_NAMES

    clean_tc_file = open(base_file_path + "/promCleanTC_" + formatted_date +".csv", "w")
    tcWriter = csv.writer(clean_tc_file)
    tcWriter.writerow(header_row_tc)

    clean_pt_file = open(base_file_path + "/promCleanPT_" + formatted_date +".csv", "w")
    ptWriter = csv.writer(clean_pt_file)
    ptWriter.writerow(header_row_pt)

    clean_fm_file = open(base_file_path + "/promCleanFM_" + formatted_date +".csv", "w")
    fmWriter = csv.writer(clean_fm_file)
    fmWriter.writerow(header_row_fm)

    print("Writing clean data")
    print(datetime.datetime.now().time())

    # Multi-processing functionality cuts our crunch time in half
    p1 = multiprocessing.Process(target=write_clean, args=((tcWriter, header_row_tc, TC_DATA, CONST.TC_NAMES)))
    p2 = multiprocessing.Process(target=write_clean, args=((ptWriter, header_row_pt, PT_DATA, CONST.PT_NAMES)))
    p3 = multiprocessing.Process(target=write_clean, args=((fmWriter, header_row_fm, FM_DATA, CONST.FM_NAMES)))
    
    p1.start()  # Write clean TC data to file
    p2.start()  # Write clean PT data to file
    p3.start()  # Write clean FM data to file
    
    p1.join()
    p2.join()
    p3.join()
    
    print(datetime.datetime.now().time())
    
    # ----------- Finishing ----------- #

    clean_tc_file.close()
    clean_pt_file.close()
    clean_fm_file.close()
