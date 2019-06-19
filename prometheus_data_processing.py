
import datetime
import os
import csv

from prometheus_daq import CONST_PT_NAMES
from prometheus_daq import CONST_TC_NAMES

#TODO : Data Processing Edition
#   - SAFETY!!! Put everything in a try/catch in case exception thrown
#   - Break up writeToFile function
#   - Add launch-relative time to clean data
#   - Write function for unix->24hr

# This sorts the raw data primarily by batch number
# but each batch is also sorted by instrument ID
# possible because Python uses a STABLE sort algorithm
def sort_raw(DATA):

    DATA.sort(key=lambda tup: tup[2])   # Sorting by instrument ID
    DATA.sort(key=lambda tup: tup[0])   # Sorting by batch number

def write_clean(csv_writer, header, RAW_DATA):

    batch_avg_time = {}                 # KEY: batch_number - VALUE: avg time of that batch number
    for reading in RAW_DATA:            # For each instrument reading

        if reading[0] in batch_avg_time:                  # Sum up all the times at the same index
            batch_avg_time[reading[0]] += reading[1]
        else:
            batch_avg_time[reading[0]] = reading[1]

    for total in batch_avg_time:                          # Use the sum of the times to calculate average time
        batch_avg_time[total] = batch_avg_time[total] / len(CONST_PT_NAMES)

    # Loops one batch at a time, creating a list for the batch, and writing it to the file
    for i in batch_avg_time:
        to_write = [None] * len(header)             # This is the list that will be written to file
        to_write[0] = i                             # Thread batch number
        to_write[1] = batch_avg_time[i]             # Avg time of batch

        # This for loop is super confusing, sorry
        # Essentially it takes the sorted DATA, compresses all of a single
        # batch into the 'to_write' list. Using .index() to find which index
        # in 'to_write' corresponds to each instrument ID
        for j in range((i * len(CONST_PT_NAMES)) + len(CONST_PT_NAMES)):
            to_write[header.index(RAW_DATA[j][2])] = RAW_DATA[j][3]    # I think this is wrong

        csv_writer.writerow(to_write)               # Write the list of data to the csv

def writeToFile(TC_DATA, PT_DATA):

    # ----------- General Housekeeping ----------- #

    cwd = os.getcwd()                                       # Get current working directory
    currentDT = datetime.datetime.now()                     # Get current time

    dateFormatted = currentDT.strftime("%Y-%m-%d_%H-%M-%S") # Format time
    base_file_path = cwd + "/Data/" + dateFormatted         # Directory where we will save our data

    print("Num of TC data points = " + str(len(TC_DATA)))   # Printing for sanity check
    print("Num of PT data points = " + str(len(PT_DATA)))

    if not os.path.exists(cwd + "/Data/"):                  # Directory management
        os.makedirs(cwd + "/Data/")

    if not os.path.exists(base_file_path):
        os.makedirs(base_file_path)

    sort_raw(TC_DATA)                                    # Sort data in case threading messed up order
    sort_raw(PT_DATA)

    # ----------- Writing Raw Data ----------- #

    # Open the file
    raw_tc_file = open(base_file_path + "/promRawTC_" + dateFormatted +".csv", "w")
    raw_pt_file = open(base_file_path + "/promRawPT_" + dateFormatted +".csv", "w")

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

    # ----------- Processing Data, Write to Clean Files ----------- #

    header_row_pt = ["num","avgTime"] + CONST_PT_NAMES
    header_row_tc = ["num","avgTime"] + CONST_TC_NAMES

    clean_tc_file = open(base_file_path + "/promCleanTC_" + dateFormatted +".csv", "w")
    tcWriter = csv.writer(clean_tc_file)
    tcWriter.writerow(header_row_tc)

    clean_pt_file = open(base_file_path + "/promCleanPT_" + dateFormatted +".csv", "w")
    ptWriter = csv.writer(clean_pt_file)
    ptWriter.writerow(header_row_pt)

    write_clean(tcWriter, header_row_tc, TC_DATA)   # Write clean TC data to file
    write_clean(ptWriter, header_row_pt, PT_DATA)   # Write clean PT data to file

    # ----------- Finishing ----------- #

    clean_tc_file.close()
    clean_pt_file.close()
