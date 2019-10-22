# Contains the data structure responsible for maintaining
# the state of the solenoids in the system

import prometheus_shared as shared
import prometheus_consts as CONST
from datetime import time
# import RPi.GPIO as gpio


class SolenoidManager:

    def __init__(self):
        # Note that 1/0 doesn't refer to open/closed
        # it refers to energized or not energized
        # look at the solenoid name to see what that translates to
        self.curr_state = {}

        for name in CONST.SOL_NAMES:    # Initialize dict
            self.curr_state[name] = 0   # All sols in their default state

        self.pin_mapping = {    # Mapping the solenoid to the pins so we know which address to signal
            "NC3O": int,
            "NCOP": int,
            "NC3N": int,
            "NCIF": int,
            "NOIP": int,
            "NCIP": int,
            "NCIO": int,
            "NCFP": int,
            "SPRK": int     # All ints need to be replaced with pin numbers
        }


    # Changes the state of solenoid 'name' to 'state'
    # if sol already in that state then do nothing
    # DOES NOT RECORD STATE CHANGE IN LOG FILE
    def solenoid_to_state(self, name, state):
        shared.log_event("SOL", name + " transitioning to state " + str(state))

        # gpio.output(self.pin_mapping[name], gpio.HIGH) # This code is taken from swapnils snippet


    # Makes large change to entire system state
    # Used during abort scenarios
    def state_change(self, new_state):
        # Loops thru both dicts (easy because keys are the same)
        for name in CONST.SOL_NAMES:
            if new_state[name] != self.curr_state[name]:
                # Actuate
                pass

        # Write this info to logfile later, this has to be fast because of abort


def main():

    sols = SolenoidManager()
    sols.solenoid_to_state("NCIO", 1)

main()