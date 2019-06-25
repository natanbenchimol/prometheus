# This file contains:
#   - All data that needs to be modified/used by multiple files
#   - Consists mostly of data containers
#   - Separated by whether or not they are thread safe

# ----------- THREAD SAFE ----------- #
TC_DATA = []        # data to be written to files
PT_DATA = []
FM_DATA = []

TC_MAX_VALS = {}    # the maximum values to be read by each instrument
PT_MAX_VALS = {}    # if this value is exceeded -> abort
FM_MAX_VALS = {}    # these are initialized by a config file

LIVE_DATA = {}      # contains the most recent reading from each instrument

# ----------- NOT THREAD SAFE ----------- #

COUNTDOWN_START = None  # Saves the timestamp for start of countdown for
                        # calculating relative mission time
