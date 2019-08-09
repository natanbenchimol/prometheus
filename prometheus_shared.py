import prometheus_consts as const
from AbortGateClass import AbortGate

# This file contains:
#   - All data structures that needs to be modified/used by multiple files
#   - Functions for setting up the structures
#   - Structures separated by whether or not they are thread safe


# ----------- THREAD SAFE ----------- #

TC_DATA = []        # data to be written to files
PT_DATA = []
FM_DATA = []

TC_ABORT_GATES = {}    # the maximum values to be read by each instrument
PT_ABORT_GATES = {}    # if this value is exceeded -> abort
FM_ABORT_GATES = {}    # these are initialized by a config file

LIVE_DATA = {}      # contains the most recent reading from each instrument

FRONT_END_TIMINGS = {}  # Contains solenoid/spark plug timings inputted on front end
PARSED_TIMINGS = []


# ----------- NOT THREAD SAFE ----------- #

COUNTDOWN_START = None  # Saves the timestamp for start of countdown for
                        # calculating relative mission time


# ---------------------- START OF CONFIG FILE SETUP FUNCTIONS ---------------------- #

# Function is called at program start to load the max val dictionaries from
# our config file
def read_config():
    config = open("config.txt", "r")
    for line in config:
        line = line.strip()                 # Just cleans up a single line for processing
        arr = line.split(",")

        if arr[0][0] is "T":                # Decide which dictionary to put it in
            TC_ABORT_GATES[arr[0]] = AbortGate(arr)
        elif arr[0][0] is "P":
            PT_ABORT_GATES[arr[0]] = AbortGate(arr)
        elif arr[0][0] is "F":
            FM_ABORT_GATES[arr[0]] = AbortGate(arr)
        else:
            print("Error: Config file parse error")

    config.close()


# Function called after launch/just before GUI termination to update config file
# and save data for next time
# Since we will only be changing these before launch we can use a slow file operation
def update_config(name, t1, t2, gate_max, gate_min, std_max, std_min):

    new_gate_params = [name, t1, t2, gate_max, gate_min, std_max, std_min]

    if name[0] is "T":                                          # First we save the new info to local data structs
        if name not in const.TC_NAMES:
            print("Error: Instrument not present in TC name consts")
            return
        TC_ABORT_GATES[name] = AbortGate(new_gate_params)

    if name[0] is "P":
        if name not in const.PT_NAMES:                          # Checks that the instrument name exists
            print("Error: Instrument not present in PT name consts")
            return
        PT_ABORT_GATES[name] = AbortGate(new_gate_params)          # Saves the new gate object into our dictionary

    if name[0] is "F":
        if name not in const.FM_NAMES:
            print("Error: Instrument not present in FM name consts")
            return
        FM_ABORT_GATES[name] = AbortGate(new_gate_params)

    new_line_str = ""
    for val in new_gate_params:         # Turn the list into a string formatted for config file
        new_line_str += str(val) + ","
    new_line_str = new_line_str[:-1]    # Remove the comma at the end of this string
    print(new_line_str)

    configR = open("config.txt", "r")    # Next we propagate the change within the config file
    prev_data = configR.readlines()      # Save whole file locally inside prev_data
    for i in range(len(prev_data)):
        if name in prev_data[i]:                    # Find the line we want to change
            prev_data[i] = new_line_str + "\n"      # Change the line in prev_data
            break
    configR.close()

    config = open("config.txt", "w")    # Write new_data to file
    for line in prev_data:
        print(line, file=config, end="")
    config.close()


def gen_config():

    # After running read_config(), any config file that we already have will populate the
    # local structs being stored in volatile memory
    try:
        read_config()
    except FileNotFoundError:
        print("No config file exists, generating now...")

    config = open("config.txt", "a")    # Append mode so as not to overwrite existing values

    # Go through the INSTRUMENT NAMES, adding any missing instruments to both config file
    # and to our local dictionaries. This code will only be useful if we already have a config
    # and we are adding another instrument, scalability.
    for val in const.TC_NAMES:
        if val not in TC_ABORT_GATES:
            print(val + ",,,,,,", file=config)
            TC_ABORT_GATES[val] = None
    for val in const.PT_NAMES:
        if val not in PT_ABORT_GATES:
            print(val + ",,,,,,", file=config)
            PT_ABORT_GATES[val] = None
    for val in const.FM_NAMES:
        if val in FM_ABORT_GATES:
            print(val + ",,,,,,", file=config)
            FM_ABORT_GATES[val] = None

    config.close()

# ---------------------- END OF CONFIG FILE SETUP FUNCTIONS ---------------------- #


# ONLY FOR TESTING PURPOSES
# This function should not be called anywhere during actual experimentation
def populate_live_data():

    print("Overwriting LIVE_DATA with fake data!!!")

    count = 1
    for instrument in const.TC_NAMES:
        LIVE_DATA[instrument] = count
        count += 1
    for instrument in const.PT_NAMES:
        LIVE_DATA[instrument] = count
        count += 1
    for instrument in const.FM_NAMES:
        LIVE_DATA[instrument] = count
        count += 1


# Initialize the live dictionary, values empty
def init_live_data():
    for instrument in const.TC_NAMES + const.PT_NAMES + const.FM_NAMES:
        LIVE_DATA[instrument] = int


# Initializing the FRONT END TIMINGS dict to avoid key errors
def init_timings_dict():
    global FRONT_END_TIMINGS

    FRONT_END_TIMINGS = {
        "NCIO_START" : int,
        "NCIO_STOP"  : int,
        "SPARK_START": int,
        "SPARK_STOP" : int,
        "NCIF_START" : int,
        "NCIF_STOP"  : int
    }


# Sets values in the timings dictionary
def set_timing(time_post_countdown, key):

    if key in FRONT_END_TIMINGS:
        FRONT_END_TIMINGS[key] = time_post_countdown
    else:
        print("Key: " + key + " not found" )

def load_timings():
    pass


# Uncomment the following 4 lines if this is the first time you are
# running the GUI on a device and run THIS file. This will allow you
# to generate and then populate the config file

def main():
    gen_config()

main()
