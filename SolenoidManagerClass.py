# Contains the data structure responsible for maintaining
# the state of the solenoids in the system

import prometheus_consts as CONST
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

    # Changes a state of a single solenoid
    # called by state_change and by user on GUI
    def toggle(self, name):
        # gpio.output(self.pin_mapping[name], gpio.HIGH) # This code is taken from swapnils snippet
        self.write_to_log()

    # Changes the state of solenoid 'name' to 'state'
    # if sol already in that state then do nothing
    def solenoid_to_state(self, name, state):
        pass

    # Makes large change to entire system state
    def state_change(self, new_state):
        # Loops thru both dicts (easy because keys are the same)
        for name in CONST.SOL_NAMES:
            if new_state[name] != self.curr_state[name]:
                # gpio.output(self.pin_mapping[name], gpio.HIGH) # This code is taken from swapnils snippet
                pass
        self.write_to_log()

    # Function actually responsible for sending electric signal
    # called by toggle and state change, not user facing
    def toggle_from_address(self, address):
        # POTENTIALLY REDUNDANT FUNCTION?
        pass

    # Writes current state to logfile, called every time state changes
    def write_to_log(self):
        pass
