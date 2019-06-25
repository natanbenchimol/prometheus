# This file contains:
#   - hard coded values/constants (stuff that can't be changed by GUI)
#   - read only constants used in calculations
#   - general calibration constants

# NOTHING IN THIS FILE SHOULD EVER BE CHANGED BY RUNNING THE GUI

# Names of all the instruments we are using to COLLECT data
TC_NAMES = ["TC1_IP", "TC2_IP", "TC1_IF", "TC_I", "TC1_IO", "TC2_IO", "TC3_IO"]
PT_NAMES = ["PT1_IP", "PT2_IP", "PT1_IF", "PT2_IF", "PT_I", "PT1_IO", "PT2_IO", "PT3_IO"]
FM_NAMES = ["FM_IF", "FM_IO"]

SOL_NAMES = ["NC_IF", "NC_IP", "NC_IP", "NO_IP", "NC3_OP", "NC_IO"]

# Frequencies at which data needs to be collected (Hz)
TC_HZ = 150
PT_HZ = 150
FM_HZ = 200
