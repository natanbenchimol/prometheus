# This file contains:
#   - hard coded values/constants (stuff that can't be changed by GUI)
#   - read only constants used in calculations
#   - general calibration constants

# NOTHING IN THIS FILE SHOULD EVER BE CHANGED BY RUNNING THE GUI

# Names of all the instruments we are using to COLLECT data
TC_NAMES = ["TC1_IP", "TC2_IP", "TC1_IF", "TC_I", "TC1_IO", "TC2_IO", "TC3_IO"]
PT_NAMES = ["PT1_IP", "PT2_IP", "PT1_IF", "PT2_IF", "PT_I", "PT1_IO", "PT2_IO", "PT3_IO"]
FM_NAMES = ["FM_IF", "FM_IO", "FM2_IO"]

SOL_NAMES = ["NC3O", "NCOP", "NC3N", "NCIF", "NOIP", "NCIP", "NCIO", "NCFP", "SPRK"]

# Firing actions
FIRING_ACTIONS = ["NCIO_1",
                 "SPRK_1",
                 "NCIF_1", "SPRK_0", "NCIF_0", "NC30_0", "NC3P_1", "NC3P_0", "NCIO_0"]

FIRING_ACTIONSa = [""]

# STANDARD TORCH FIRE PROCEDURE:

# combustion ox valve open (NCIO)
# spark plug begin
# fuel valve open (NCIF)
#   IGNITION HERE
#   WE FIRING
# spark plug stops
# fuel valve closed (NCIF) FIRING FINISHED

# ox by bottle closes (NC3O)    PURGE OPS
# nitrogen purge opens (NC3P)
# nitrogen purge closes (NC3P)
# ox valve closes (NCIO)


# Frequencies at which data needs to be collected (Hz)
TC_HZ = 150
PT_HZ = 150
FM_HZ = 200
