#########################################################
#
#
#   SETTING UP THE DAQ ON SITE FOR A FIRING
#           FOLLOW THESE STEPS
#
#
#########################################################

# SET ALL HYPERPARAMS
# pre fire wait
# post fire wait
# daq frequency
# sensor names
# firing actions


# FILL OUT THE FOLLOWING INFORMATION FOR LOGFILE

                # Name         role     phyiscal location
TEAM_MEMBERS = {"Buzz Aldrin - Fire Lead - Bunker",
                "Michael Collins - DAQ Lead - Bunker",
                "Niel Armstrong - Cameras Lead - Secondary Bunker"}

FIRING_LOCATION = "Cape Canaveral"

IGNITER_INFO = {"Name": "Saturn V",
                "Nom. Thrust": 31324.4,
                "Nom. Chamber Pressure": 2343.3,
                "Nom. Ox Flow Rate": 23423.32,
                "Nom. Fuel Flow Rate": 3242.2,
                "Desired Fire Duration": 5,
                "Propellants": "Kerosene/Ox",
                "Num. Working Sensors": 18
                }

# Sensors in the P&ID that aren't being used for this fire (if any)
FAILED_SENSORS = []

# Put down as much info about cameras, helps with retrospective analysis
# For location: compass directions relative to firing direction being North
CAMERAS = ["""Matt's DSLR - LENS: 40mil
                            EXPOSURE: 25
                            SHUTTER: 100
                            FPS: 30
                            LOCATION: East""",
           """LPL GoProHero4 - LENS: NA
                            EXPOSURE: 25
                            SHUTTER: 100
                            FPS: 30
                            LOCATION: On stand"""
           ]
